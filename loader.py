# loader.py
import json
from pathlib import Path
from sqlalchemy.orm import Session
from database import SessionLocal
from datetime import datetime
from models import (
    Agency, Region, Field, Task, AuditType, SpecialCase, Viewer
)

def get_or_create(session: Session, model, **kwargs):
    """간단한 upsert 헬퍼"""
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    instance = model(**kwargs)
    session.add(instance)
    session.flush()  # id 채워지도록
    return instance

def load_json_to_db(json_path: Path):
    # 1) JSON 파일 읽기
    with json_path.open(encoding="utf-8") as f:
        data = json.load(f)  # 리스트 형태를 가정

    session = SessionLocal()
    try:
        for item in data:
            agency         = get_or_create(session, Agency, name=item["감사실시기관"])
            related_agency = (get_or_create(session, Agency, name=item["관련기관"])
                            if item.get("관련기관") else None)
            audit_type     = get_or_create(session, AuditType, name=item["감사종류"])
            field          = get_or_create(session, Field, name=item["auto_분야"].split(" ",1)[1])
            task           = get_or_create(session, Task,  name=item["auto_업무"])

            # 날짜 파싱 (감사기간의 시작일자 사용)
            date_str       = item.get("감사기간", "").split("~")[0].strip()
            date_val       = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None

            case = GamsaCase(
                case_uuid         = item["case_uuid"],
                agency_id         = agency.id,
                related_agency_id = related_agency.id if related_agency else None,
                audit_type_id     = audit_type.id,
                field_id          = field.id,
                task_id           = task.id,
                date              = date_val,
                result            = item.get("감사결과종류"),
                summary           = item.get("auto_요약"),
                original_text     = item.get("preprocessed_text"),
                analysis_text     = item.get("auto_판단이유"),
                hwp_path          = item.get("downloaded_file_path")
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
