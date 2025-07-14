import json
from pathlib import Path
from datetime import datetime
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import (
    Agency, Region, Category, Task, AuditType, Viewer
)

# 테이블 생성(테스트용)
# Base.metadata.create_all(bind=engine)

# 필드 매핑 설정: JSON 키 -> (속성 접두사, 기본값)
FIELD_MAPPING = {
    "auto_구분":    ("auditType",     "기타"),
    "auto_분야":    ("category",         "기타"),
    "auto_업무":    ("task",          "기타"),
    "auto_요약":    ("summary",       ""),
    "auto_판단이유":("analysisText",  ""),
}


def get_or_create(session: Session, model, **kwargs):
    """간단한 upsert 헬퍼"""
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    instance = model(**kwargs)
    session.add(instance)
    session.flush()
    return instance


def safe_get(item: dict, key: str, default=None):
    """키가 없거나 빈 문자열인 경우 default 반환"""
    val = item.get(key, default)
    if isinstance(val, str) and not val.strip():
        return default
    return val


def load_json_to_db(jsonPath: Path):
    # JSON 파일 읽기
    with jsonPath.open(encoding="utf-8") as f:
        data = json.load(f)

    session = SessionLocal()
    try:
        for item in data:
            # 기관, 관련기관, 지역 upsert
            agencyName     = safe_get(item, "감사실시기관", "알수없음")
            agency         = get_or_create(session, Agency, name=agencyName)
            relatedName    = safe_get(item, "관련기관")
            relatedAgency  = (
                get_or_create(session, Agency, name=relatedName)
                if relatedName else None
            )
            regionName     = safe_get(item, "지역")
            region         = (
                get_or_create(session, Region, name=regionName)
                if regionName else None
            )
            keywords = item.get("auto_특성", [])
            if isinstance(keywords, list):
                keyword = ", ".join(str(x) for x in keywords)
            else:
                keyword = str(keywords)
            typesl = item.get("감사종류", [])
            types = (
                ", ".join(str(x) for x in typesl) 
                if isinstance(typesl, list)
                else str(typesl)
            )

            # 필드 매핑 처리
            kwargs = {}
            for jsonKey, (attr, default) in FIELD_MAPPING.items():
                raw = safe_get(item, jsonKey, default)
                # "번호 + 값" 포맷에서 번호 제거
                if jsonKey in ("auto_구분", "auto_분야") and isinstance(raw, str):
                    parts = raw.split(" ", 1)
                    raw = parts[-1] if len(parts) > 1 else raw

                if attr in ("category", "task", "auditType"):
                    model = {"category": Category, "task": Task, "auditType": AuditType}[attr]
                    inst  = get_or_create(session, model, name=raw or default)
                    kwargs[f"{attr}Id"] = inst.id
                else:
                    kwargs[attr] = raw or default

            # specialCase는 아직 데이터 미포함이므로 항상 NULL
            kwargs['specialCaseId'] = None

            # 날짜 파싱
            dateStr = safe_get(item, "감사기간", "").split("~")[0].strip()
            dateVal = (
                datetime.strptime(dateStr, "%Y-%m-%d").date()
                if dateStr else None
            )

            # 중복 삽입 방지
            if session.query(Viewer).filter_by(caseUuid=item.get("file_uuid")).first():
                continue

            # Viewer 객체 생성
            case = Viewer(
                caseUuid         = item.get("file_uuid"),
                agencyId         = agency.id,
                relatedAgencyId  = relatedAgency.id if relatedAgency else None,
                regionId         = region.id if region else None,
                date              = dateVal,
                result            = safe_get(item, "감사결과종류"),
                hwpPath           = safe_get(item, "downloaded_file_path"),
                keyword           = keyword,
                types             = types,
                **kwargs
            )
            session.add(case)

        session.commit()
        print(f"✅ 전체 {len(data)}건 삽입 완료")
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    load_json_to_db(Path(__file__).parent / "sample_data.json")
