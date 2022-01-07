from .. import models
from sqlalchemy import func, desc
from typing import Optional


def get_generic_post_query(db):
    post_query = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id)
    return post_query


def get_all_posts(db, limit: int = 10, skip: int = 0, sortBy :str = 'date', user_id: int = None, search: Optional[str] = None):
    post_query = get_generic_post_query(db)
    if user_id:
        post_query = post_query.filter(models.Post.user_id == user_id)

    if search:
        post_query = post_query.filter(func.lower(models.Post.title).like(f"%{search.lower()}%"))
    total_results = post_query.count()
    post_query = post_query.order_by(None)
    if sortBy == 'title':
        post_query = post_query.order_by(models.Post.title)
    else:
        post_query = post_query.order_by(desc(models.Post.created_at))
    posts = post_query.offset(skip).limit(limit).all()
    return {"data": posts, "foundResults": total_results, "numResults": len(posts)}


