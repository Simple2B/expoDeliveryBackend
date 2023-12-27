from datetime import datetime
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import orm

from app.database import db
from app import schema as s
from .utils import ModelMixin, generate_uuid
from .restaurant_category import restaurant_categories

if TYPE_CHECKING:
    from .category import Category

DEFAULT_IMAGE = "../images/restaurants/default.png"


class Restaurant(db.Model, ModelMixin):
    __tablename__ = "restaurants"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    uuid: orm.Mapped[str] = orm.mapped_column(sa.String(36), default=generate_uuid)
    name: orm.Mapped[str] = orm.mapped_column(
        sa.String(64), unique=True, nullable=False
    )
    image: orm.Mapped[str] = orm.mapped_column(sa.String(256), default=DEFAULT_IMAGE)
    created_at: orm.Mapped[datetime] = orm.mapped_column(
        sa.DateTime,
        default=datetime.utcnow,
    )

    description: orm.Mapped[str] = orm.mapped_column(sa.String(512), nullable=False)

    is_deleted: orm.Mapped[bool] = orm.mapped_column(
        sa.Boolean, server_default=sa.false()
    )

    duration: orm.Mapped[str] = orm.mapped_column(sa.String(256), nullable=False)

    location: orm.Mapped[str] = orm.mapped_column(sa.String(256), nullable=False)

    categories: orm.Mapped[list["Category"]] = orm.relationship(
        "Category",
        secondary=restaurant_categories,
        viewonly=True,
    )

    @property
    def distance(self):
        pass

    @property
    def rating(self):
        pass

    @property
    def rates(self):
        pass

    def __repr__(self):
        return f"<{self.id}: {self.name}, {self.location}>"

    @property
    def json(self):
        restaurant = s.Restaurant.model_validate(self)
        return restaurant.model_dump_json()
