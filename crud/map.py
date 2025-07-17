from sqlalchemy.orm import Session
from models import Viewer
from schemas import MapStat
from sqlalchemy import func
from typing import List

def get_top10_categories_with_task_count(db: Session, region: str = None):
    query = db.query(Viewer.category, func.count().label("count"))

    if region:
        query = query.filter(Viewer.state.contains(region))

    query = (
        query.filter(Viewer.category.isnot(None))
        .group_by(Viewer.category)
        .order_by(func.count().desc())
        .limit(10)
    )

    category_counts = query.all()

    result = []
    for category, count in category_counts:
        task_count_query = db.query(func.count(func.distinct(Viewer.task))).filter(Viewer.category == category)
        if region:
            task_count_query = task_count_query.filter(Viewer.state.contains(region))
        task_count = task_count_query.scalar()

        result.append({
            "category": category,
            "count": count,
            "task_count": task_count
        })

    return result


def get_sunburst_data(db: Session, region: str = None):
    query = db.query(Viewer.category, Viewer.task)

    if region:
        query = query.filter(Viewer.state.contains(region))

    query = query.filter(
        Viewer.category.isnot(None),
        Viewer.task.isnot(None)
    )

    rows = query.all()

    from collections import defaultdict

    tree = defaultdict(lambda: defaultdict(int))

    for category, task in rows:
        tree[category][task] += 1  # task를 그대로 key로 사용
    return tree




def get_top10_tasks_by_category(db: Session, region: str = None, category: str = None):
    if not category:
        return []

    query = db.query(Viewer.task, func.count().label("count")).filter(
        Viewer.task.isnot(None),
        Viewer.category == category
    )

    if region:
        query = query.filter(Viewer.state.contains(region))

    result = (
        query.group_by(Viewer.task)
        .order_by(func.count().desc())
        .limit(10)
        .all()
    )

    return [{"task": task, "count": count} for task, count in result]
