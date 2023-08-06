from sqlalchemy.orm import Session
from fastapi import HTTPException


def paginate(db: Session, model: object, order_by: object, page: int, size: int):
    objects = get_objects(db, model, order_by, page, size)

    if len(objects) == 0:
        raise HTTPException(status_code=404, detail="Page not found")

    return create_page(objects, page, size)


def get_objects(db: Session, model: object, order_by: object, page: int, size: int):

    query = db.query(*model) if isinstance(model, list) else db.query(model)
    return query.order_by(order_by).offset(page * size).limit(size).all()


def get_objects_cursor(db: Session, model: object, cursor, order_by: object, size: int):

    if isinstance(model, list):
        return db.query(*model).filter(order_by > cursor).order_by(order_by).limit(size).all()
    else:
        return db.query(model).filter(order_by > cursor).order_by(order_by).limit(size).all()


def create_page(items, page: int, size: int):
    return {
        "items": list(items),
        "total": len(items)//size,
        "page": page,
        "size": size
    }
