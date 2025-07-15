import json
from pathlib import Path
from datetime import datetime
from sqlalchemy import inspect
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import (
    Base,
    Viewer,
    Agency,
    Region,
    Category,
    Task,
    AuditType,
    SpecialCase,
    MapStatistic,
)

# ① DB 연결 확인 & 테이블 리셋
print("▶ Using SQLite URL:", engine.url)
print("→ Actual tables before drop:", inspect(engine).get_table_names())

Base.metadata.drop_all(bind=engine)
print("→ Actual tables after drop:", inspect(engine).get_table_names())

Base.metadata.create_all(bind=engine)
print("→ Actual tables after create:", inspect(engine).get_table_names())

# ② JSON 필드 → 모델 속성 매핑
FIELD_MAPPING = {
    "auto_구분":    ("auditType",    "기타"),
    "auto_분야":    ("category",     "기타"),
    "auto_업무":    ("task",         "기타"),
    "auto_요약":    ("summary",      ""),
    "auto_판단이유":("analysisText", ""),
}

def get_or_create(session: Session, model, **kwargs):
    """간단 upsert 헬퍼: 이미 있으면 가져오고, 없으면 새로 추가."""
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    instance = model(**kwargs)
    session.add(instance)
    session.flush()   # 바로 INSERT 날려서 ID 가져오기
    return instance

def safe_get(item: dict, key: str, default=None):
    """키가 없거나 빈 문자열이면 default 반환."""
    val = item.get(key, default)
    if isinstance(val, str) and not val.strip():
        return default
    return val

def load_json_to_db(json_path: Path):
    with json_path.open(encoding="utf-8") as f:
        data = json.load(f)

    session = SessionLocal()
    inserted = 0
    seen = set()  # 이미 처리한 case_uuid 추적

    try:
        for item in data:
            # 1) case_uuid 결정 (case_uuid 우선, 없으면 file_uuid)
            case_uuid = safe_get(item, "case_uuid") or safe_get(item, "file_uuid")
            if not case_uuid:
                print("⚠️ UUID 누락, 스킵:", item)
                continue

            # 2) 중복 스킵 (파이썬 레벨 + DB 레벨)
            if case_uuid in seen:
                print("🔄 이미 처리한 UUID, 스킵:", case_uuid)
                continue
            if session.query(Viewer).filter_by(caseUuid=case_uuid).first():
                print("🔄 이미 DB에 있는 UUID, 스킵:", case_uuid)
                continue
            seen.add(case_uuid)

            # 3) FK 관계 upsert
            agency  = get_or_create(session, Agency, name=safe_get(item, "감사실시기관", "알수없음"))
            related = safe_get(item, "관련기관") and get_or_create(session, Agency, name=item["관련기관"])
            region  = safe_get(item, "지역")    and get_or_create(session, Region, name=item["지역"])

            # 4) 키워드·타입 가공
            keywords = item.get("auto_특성", [])
            keyword  = ", ".join(keywords) if isinstance(keywords, list) else str(keywords)
            typesl   = item.get("감사종류", [])
            types    = ", ".join(typesl)    if isinstance(typesl, list)   else str(typesl)

            # 5) FIELD_MAPPING 반영 → kwargs
            kwargs = {}
            for jsonKey, (attr, default) in FIELD_MAPPING.items():
                raw = safe_get(item, jsonKey, default)
                # 'auto_구분', 'auto_분야'는 문자열 뒤 부분만
                if jsonKey in ("auto_구분", "auto_분야") and isinstance(raw, str):
                    raw = raw.split(" ", 1)[-1]
                # category, task, auditType은 FK upsert
                if attr in ("category", "task", "auditType"):
                    Model = {"category": Category, "task": Task, "auditType": AuditType}[attr]
                    inst  = get_or_create(session, Model, name=raw or default)
                    kwargs[f"{attr}Id"] = inst.id
                else:
                    kwargs[attr] = raw or default

            # 6) 날짜 파싱 (감사기간의 시작일)
            date_str  = safe_get(item, "감사기간", "")
            start_str = date_str.split("~")[0].strip()
            date_val  = datetime.strptime(start_str, "%Y-%m-%d").date() if start_str else None

            # 7) Viewer 객체 생성
            case = Viewer(
                caseUuid        = case_uuid,
                agencyId        = agency.id,
                relatedAgencyId = related.id  if related else None,
                regionId        = region.id   if region else None,
                date            = date_val,
                result          = safe_get(item, "감사결과종류"),
                hwpPath         = safe_get(item, "downloaded_file_path"),
                keyword         = keyword,
                types           = types,
                **kwargs
            )
            session.add(case)
            inserted += 1

        session.commit()
        print(f"✅ 총 {len(data)}건 중 {inserted}건 삽입 완료")
    except Exception as e:
        session.rollback()
        print("❌ 오류 발생:", e)
        raise
    finally:
        session.close()

if __name__ == "__main__":
    load_json_to_db(Path(__file__).parent / "pap2025_41989_false_auto_v2.json")
