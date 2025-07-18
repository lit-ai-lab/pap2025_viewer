from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Viewer
from collections import defaultdict

# ✅ [1] 지역 기반: 분야 Top10 + 분야별 count만 sunburst1
def get_top10_categories(db: Session, region: str = None):
    query = db.query(Viewer.category, func.count().label("count"))

    if region:
        query = query.filter(Viewer.state.contains(region))

    query = (
        query.filter(Viewer.category.isnot(None))
        .group_by(Viewer.category)
        .order_by(func.count().desc())
        .limit(10)
    )

    results = query.all()

    return [
        {"id": idx + 1, "category": category, "count": count}
        for idx, (category, count) in enumerate(results)
    ]


def get_sunburst_categories_only(db: Session, region: str = None):
    """
    분야 Top10만 포함된 sunburst용 데이터
    """
    query = db.query(Viewer.category, func.count().label("count"))

    if region:
        query = query.filter(Viewer.state.contains(region))

    query = (
        query.filter(Viewer.category.isnot(None))
        .group_by(Viewer.category)
        .order_by(func.count().desc())
        .limit(10)
    )

    results = query.all()

    labels = ["전국"]
    parents = [""]
    values = [0]  # root node (전국)

    for category, count in results:
        labels.append(category)
        parents.append("전국")
        values.append(count)

    return {
        "labels": labels,
        "parents": parents,
        "values": values
    }


# ✅ [2] 분야 선택 시: 업무 Top10 + sunburst(task 포함)
def get_top10_tasks_by_category(db: Session, region: str = None, category: str = None):
    if not category:
        return []

    query = db.query(Viewer.task, func.count().label("count")).filter(
        Viewer.task.isnot(None),
        Viewer.category == category
    )

    if region:
        query = query.filter(Viewer.state.contains(region))

    query = (
        query.group_by(Viewer.task)
        .order_by(func.count().desc())
        .limit(10)
    )
    results = query.all()

    return [
        {"id": idx + 1, "task": task, "count": count}
        for idx, (task, count) in enumerate(results)
    ]



def get_sunburst_task_detail(db: Session, region: str = None, category: str = None):
    """
    선택된 분야에 대해: 분야(root) → 업무(task) Top10 → count
    """
    if not category:
        return {"labels": [], "parents": [], "values": []}

    query = db.query(Viewer.task, func.count().label("count")).filter(
        Viewer.category == category,
        Viewer.task.isnot(None)
    )

    if region:
        query = query.filter(Viewer.state.contains(region))

    results = (
        query.group_by(Viewer.task)
        .order_by(func.count().desc())
        .limit(10)
        .all()
    )

    labels = [category]
    parents = [""]
    values = [0]  # root 노드 (category)

    for task, count in results:
        labels.append(task)
        parents.append(category)
        values.append(count)

    return {
        "labels": labels,
        "parents": parents,
        "values": values
    }
