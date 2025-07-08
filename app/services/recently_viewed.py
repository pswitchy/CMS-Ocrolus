from collections import deque, defaultdict

RECENT_CAPACITY = 5

# { user_id: deque([article_id_3, article_id_2, article_id_1]) }
_recently_viewed_store = defaultdict(lambda: deque(maxlen=RECENT_CAPACITY))

def add_viewed_article(user_id: int, article_id: int):
    """Adds an article to a user's recently viewed list."""
    user_deque = _recently_viewed_store[user_id]
    
    if article_id in user_deque:
        user_deque.remove(article_id)
        
    user_deque.appendleft(article_id)

def get_viewed_articles(user_id: int) -> list[int]:
    """Retrieves the list of recently viewed article IDs for a user."""
    return list(_recently_viewed_store[user_id])