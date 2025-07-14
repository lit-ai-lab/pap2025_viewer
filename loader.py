# loader.py
import json
from pathlib import Path
from datetime import datetime
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import (
    Agency, Region, Field, Task, AuditType, Viewer
)

# 테이블 생성(테스트용)
Base.metadata.create_all(bind=engine)

# 필드 매핑 설정: JSON 키 -> (속성 접두사, 기본값)
FIELD_MAPPING = {
    "auto_구분":    ("audit_type",   "기타"),
    "auto_분야":    ("field",        "기타"),
    "auto_업무":    ("task",         "기타"),
    "auto_요약":    ("summary",      ""),
    "auto_판단이유":("analysis_text",""),
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


def load_json_to_db(json_path: Path):
    # JSON 파일 읽기
    with json_path.open(encoding="utf-8") as f:
        data = json.load(f)

    session = SessionLocal()
    try:
        for item in data:
            # 기관, 관련기관, 지역 upsert
            agency_name   = safe_get(item, "감사실시기관", "알수없음")
            agency        = get_or_create(session, Agency, name=agency_name)
            related_name  = safe_get(item, "관련기관")
            related_agency = (
                get_or_create(session, Agency, name=related_name)
                if related_name else None
            )
            region_name   = safe_get(item, "지역")
            region        = (
                get_or_create(session, Region, name=region_name)
                if region_name else None
            )

            # 필드 매핑 처리
            kwargs = {}
            for json_key, (attr, default) in FIELD_MAPPING.items():
                raw = safe_get(item, json_key, default)
                # "번호 + 값" 포맷에서 번호 제거
                if json_key in ("auto_구분", "auto_분야") and isinstance(raw, str):
                    parts = raw.split(" ", 1)
                    raw = parts[-1] if len(parts) > 1 else raw

                if attr in ("field", "task", "audit_type"):
                    model = {"field": Field, "task": Task, "audit_type": AuditType}[attr]
                    inst = get_or_create(session, model, name=raw or default)
                    kwargs[f"{attr}_id"] = inst.id
                else:
                    kwargs[attr] = raw or default

            # special_case는 아직 데이터 미포함이므로 항상 NULL
            kwargs['special_case_id'] = None

            # 날짜 파싱
            date_str = safe_get(item, "감사기간", "").split("~")[0].strip()
            date_val = (
                datetime.strptime(date_str, "%Y-%m-%d").date()
                if date_str else None
            )

            # 중복 삽입 방지
            if session.query(Viewer).filter_by(case_uuid=item.get("file_uuid")).first():
                continue

            # Viewer 객체 생성
            case = Viewer(
                case_uuid         = item.get("file_uuid"),
                agency_id         = agency.id,
                related_agency_id = related_agency.id if related_agency else None,
                region_id         = region.id         if region else None,
                date              = date_val,
                result            = safe_get(item, "감사결과종류"),
                hwp_path          = safe_get(item, "downloaded_file_path"),
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
    load_json_to_db(Path(__file__).parent / "sampledata.json")
