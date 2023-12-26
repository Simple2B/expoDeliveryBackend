import sqlalchemy as sa

from app.database import db

restaurant_categories = sa.Table(
    "restaurant_categories",
    db.Model.metadata,
    sa.Column(
        "restaurant_id", sa.ForeignKey("restaurants.id"), primary_key=True
    ),  # noqa E501
    sa.Column(
        "category_id", sa.ForeignKey("category_id.id"), primary_key=True
    ),  # noqa E501
)
