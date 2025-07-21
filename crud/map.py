from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Viewer
from collections import defaultdict
import re


# def get_category_task_summary(db: Session, region: str = None):
#     # [1] Top10 분야 조회
#     category_query = db.query(Viewer.category, func.count().label("count"))
#     if region:
#         category_query = category_query.filter(Viewer.state.contains(region))
#     category_query = (
#         category_query.filter(Viewer.category.isnot(None))
#         .group_by(Viewer.category)
#         .order_by(func.count().desc())
#         .limit(10)
#     )
#     top10_categories_result = category_query.all()

#     # → JSON용 변환 (id 포함)
#     top10_categories = [
#         {"id": idx + 1, "category": category, "count": count}
#         for idx, (category, count) in enumerate(top10_categories_result)
#     ]

#     # [2] 분야별 업무 Top10 조회 (id 포함)
#     tasks_by_category = {}

#     for category_idx, (category, _) in enumerate(top10_categories_result):
#         task_query = db.query(Viewer.task, func.count().label("count")).filter(
#             Viewer.category == category,
#             Viewer.task.isnot(None)
#         )
#         if region:
#             task_query = task_query.filter(Viewer.state.contains(region))

#         task_query = (
#             task_query.group_by(Viewer.task)
#             .order_by(func.count().desc())
#             .limit(10)
#         )
#         tasks = task_query.all()

#         tasks_by_category[category] = [
#             {"id": idx + 1, "task": task, "count": count}
#             for idx, (task, count) in enumerate(tasks)
#         ]

#     return {
#         "region": region if region else "전국",
#         "top10_categories": top10_categories,
#         "tasks_by_category": tasks_by_category
#     }


def get_category_task_summary(db: Session, region: str = None):
    # [1] Top10 분야 조회
    category_query = db.query(Viewer.category, func.count().label("count"))
    if region:
        category_query = category_query.filter(Viewer.state.contains(region))
    category_query = (  
        category_query.filter(Viewer.category.isnot(None))
        .group_by(Viewer.category)
        .order_by(func.count().desc())
        .limit(10)
    )
    top10_categories_result = category_query.all()

    categories_output = []

    task_global_id = 1  # 전체 task에 대해 id 연속 증가

    # [2] 각 분야별 task 포함
    for cat_idx, (category_full, category_count) in enumerate(top10_categories_result):
        # ✅ 앞 숫자 제거 (예: "04 계약" → "계약")
        if " " in category_full:
            _, category_name = category_full.split(" ", 1)
        else:
            category_name = category_full
            
        # 분야별 업무 top10 조회
        task_query = db.query(Viewer.task, func.count().label("count")).filter(
            Viewer.category == category_full,
            Viewer.task.isnot(None)
        )
        if region:
            task_query = task_query.filter(Viewer.state.contains(region))
        task_query = (
            task_query.group_by(Viewer.task)
            .order_by(func.count().desc())
            .limit(10)
        )
        tasks_result = task_query.all()

        # 업무 리스트에 ID 포함
        tasks_output = []
        for task, count in tasks_result:
            tasks_output.append({
                "id": task_global_id,
                "task": task,
                "count": count
            })
            task_global_id += 1

        # 하나의 카테고리 블록
        categories_output.append({
            "id": cat_idx + 1,
            "category": category_name,
            "count": category_count,
            "tasks": tasks_output
        })

    return {
        "region": region if region else "전국",
        "categories": categories_output
    }
