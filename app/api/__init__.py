from flask import Blueprint
from app.api.auth import RegisterView, LoginView
from app.api.articles import ArticleListView, ArticleView
from app.api.users import RecentlyViewedView

api_bp = Blueprint('api', __name__)

# Authentication routes
api_bp.add_url_rule('/auth/register', view_func=RegisterView.as_view('register'))
api_bp.add_url_rule('/auth/login', view_func=LoginView.as_view('login'))

# Article routes
api_bp.add_url_rule('/articles', view_func=ArticleListView.as_view('article_list'))
api_bp.add_url_rule('/articles/<int:article_id>', view_func=ArticleView.as_view('article_detail'))

# User-specific routes
api_bp.add_url_rule('/users/me/recently-viewed', view_func=RecentlyViewedView.as_view('recently_viewed'))