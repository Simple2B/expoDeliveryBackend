from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import orm

from app.database import db

from .utils import generate_uuid
from .food_tags import food_tags

if TYPE_CHECKING:
    from .category import Category
    from .restaurant import Restaurant


class Food(db.Model):
    __tablename__ = "foods"

    id: orm.Mapped[int] = orm.mapped_column(sa.Integer, primary_key=True)
    uuid: orm.Mapped[str] = orm.mapped_column(
        sa.String(36),
        unique=True,
        default=generate_uuid,
    )
    name: orm.Mapped[str] = orm.mapped_column(sa.String(255), nullable=False)
    price: orm.Mapped[float] = orm.mapped_column(sa.Float, nullable=False)
    image: orm.Mapped[str] = orm.mapped_column(sa.String(255), nullable=False)
    info: orm.Mapped[str] = orm.mapped_column(sa.Text, nullable=False)

    calories: orm.Mapped[int] = orm.mapped_column(sa.Integer, nullable=True)

    restaurant_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("restaurants.id"), nullable=False)

    restaurant: orm.Mapped["Restaurant"] = orm.relationship(
        "Restaurant",
        foreign_keys=[restaurant_id],
        viewonly=True,
        backref="foods",
    )

    tags: orm.Mapped[list["Category"]] = orm.relationship(
        "Category",
        secondary=food_tags,
        viewonly=True,
    )

    def __repr__(self):
        return f"<{self.id}: {self.name} - {self.price}>"
