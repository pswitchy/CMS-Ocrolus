from flask import request, jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Article, User
from app.extensions import db
from app.services import recently_viewed

class ArticleListView(MethodView):
    decorators = [jwt_required()]

    def get(self):
        """List all articles with pagination."""
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        paginated_articles = Article.query.order_by(Article.date_created.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        articles = [
            {"id": a.id, "title": a.title, "author": a.author.username, "date_created": a.date_created.isoformat()}
            for a in paginated_articles.items
        ]

        return jsonify({
            "articles": articles,
            "total": paginated_articles.total,
            "pages": paginated_articles.pages,
            "current_page": paginated_articles.page
        }), 200

    def post(self):
        """Create a new article."""
        data = request.get_json()
        if not data:
            return jsonify({"msg": "Request body is missing or not JSON"}), 400
        title = data.get('title')
        content = data.get('content')

        if not title or not isinstance(title, str):
            return jsonify({"msg": "Missing or invalid 'title' field"}), 400

        if not content or not isinstance(content, str):
            return jsonify({"msg": "Missing or invalid 'content' field"}), 400
        
        current_username = get_jwt_identity()
        user = User.query.filter_by(username=current_username).first_or_404()
        
        new_article = Article(
            title=data['title'],
            content=data['content'],
            user_id=user.id
        )
        db.session.add(new_article)
        db.session.commit()
        return jsonify({"msg": "Article created", "id": new_article.id}), 201

class ArticleView(MethodView):
    decorators = [jwt_required()]

    def get(self, article_id):
        """Get a single article."""
        article = Article.query.get_or_404(article_id)

        current_username = get_jwt_identity()
        user = User.query.filter_by(username=current_username).first_or_404()

        recently_viewed.add_viewed_article(user_id=user.id, article_id=article_id)

        return jsonify({
            "id": article.id,
            "title": article.title,
            "content": article.content,
            "author": article.author.username,
            "date_created": article.date_created.isoformat()
        }), 200

    def put(self, article_id):
        """Update an article."""
        article = Article.query.get_or_404(article_id)
        current_username = get_jwt_identity()
        user = User.query.filter_by(username=current_username).first_or_404()
        
        if article.user_id != user.id:
            return jsonify({"msg": "Forbidden: You are not the author"}), 403

        data = request.get_json()
        article.title = data.get('title', article.title)
        article.content = data.get('content', article.content)
        db.session.commit()
        return jsonify({"msg": "Article updated"}), 200

    def delete(self, article_id):
        """Delete an article."""
        article = Article.query.get_or_404(article_id)
        current_username = get_jwt_identity()
        user = User.query.filter_by(username=current_username).first_or_404()
        
        if article.user_id != user.id:
            return jsonify({"msg": "Forbidden: You are not the author"}), 403

        db.session.delete(article)
        db.session.commit()
        return jsonify({"msg": "Article deleted"}), 200