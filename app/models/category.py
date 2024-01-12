from typing import TYPE_CHECKING
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import orm

from app.database import db
from .utils import ModelMixin, generate_uuid
from .restaurant_category import restaurant_categories
from .food_tags import food_tags
from app import schema as s

if TYPE_CHECKING:
    from .restaurant import Restaurant
    from .food import Food


DEFAULT_IMAGE = "../images/categories/default.png"


class Category(db.Model, ModelMixin):
    __tablename__ = "categories"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    uuid: orm.Mapped[str] = orm.mapped_column(sa.String(36), default=generate_uuid)
    name: orm.Mapped[str] = orm.mapped_column(sa.String(64), unique=True, nullable=False)
    image: orm.Mapped[str] = orm.mapped_column(sa.String(256), default=DEFAULT_IMAGE)
    created_at: orm.Mapped[datetime] = orm.mapped_column(
        sa.DateTime,
        default=datetime.utcnow,
    )

    is_deleted: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, server_default=sa.false())

    restaurants: orm.Mapped[list["Restaurant"]] = orm.relationship(
        "Restaurant",
        secondary=restaurant_categories,
        viewonly=True,
    )

    foods: orm.Mapped[list["Food"]] = orm.relationship(
        "Food",
        secondary=food_tags,
        viewonly=True,
    )

    def __repr__(self):
        return f"<{self.id}: {self.username},{self.email}>"

    @property
    def count(self):
        return len(self.restaurants)

    @property
    def json(self):
        u = s.Category.model_validate(self)
        return u.model_dump_json()
