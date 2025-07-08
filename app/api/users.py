from flask import jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import recently_viewed
from app.models import Article, User

class RecentlyViewedView(MethodView):
    decorators = [jwt_required()]

    def get(self):
        current_username = get_jwt_identity()
        user = User.query.filter_by(username=current_username).first_or_404()
        article_ids = recently_viewed.get_viewed_articles(user.id)
        
        # Fetch article details for the IDs
        articles = Article.query.filter(Article.id.in_(article_ids)).all()
        # Preserve the order from the recently viewed list
        article_map = {article.id: article for article in articles}
        ordered_articles = [article_map[id] for id in article_ids if id in article_map]

        return jsonify([
            {"id": a.id, "title": a.title} for a in ordered_articles
        ]), 200