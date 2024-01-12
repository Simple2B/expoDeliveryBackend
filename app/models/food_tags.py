import sqlalchemy as sa

from app.database import db

food_tags = sa.Table(
    "food_tags",
    db.Model.metadata,
    sa.Column("food_id", sa.ForeignKey("foods.id"), primary_key=True),
    sa.Column("category_id", sa.ForeignKey("categories.id"), primary_key=True),
)


class FoodTags(db.Model):
    __tablename__ = "food_tags" 
