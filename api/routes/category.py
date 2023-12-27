from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

import app.models as m
import app.schema as s
from api.dependency import get_db
from app.logger import log

category_router = APIRouter(prefix="/categories", tags=["Categories"])


@category_router.get(
    "/{category_id}", status_code=status.HTTP_200_OK, response_model=s.Category
)
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
):
    log(log.INFO, f"get_category: {category_id}")

    category: m.Category | None = db.scalar(
        select(m.Category).where(m.Category.id == category_id)
    )
    if not category:
        log(log.INFO, "Category [%s] wasn`t found", category_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    return category


@category_router.get("", status_code=status.HTTP_200_OK, response_model=s.CategoryList)
def get_categories(
    db: Session = Depends(get_db),
):
    log(log.INFO, "Get all categories")

    categories: Sequence[m.Category] = db.scalars(select(m.Category)).all()

    return categories


@category_router.get(
    "/filters", status_code=status.HTTP_200_OK, response_model=s.FilterList
)
def get_filters(
    db: Session = Depends(get_db),
):
    log(log.INFO, "Get all filters")

    filters: Sequence[m.Category] = db.scalars(select(m.Category)).all()

    return filters
