from collections import deque, defaultdict

# This constant defines how many recent articles to track per user
RECENT_CAPACITY = 5

# We use a defaultdict. If a user is accessed for the first time,
# it will automatically create a deque with a maxlen for them.
# This is a global in-memory store and will be reset if the app restarts.
# This meets the requirement of not persisting this data in a DB.
# Structure: { user_id: deque([article_id_3, article_id_2, article_id_1]) }
_recently_viewed_store = defaultdict(lambda: deque(maxlen=RECENT_CAPACITY))

def add_viewed_article(user_id: int, article_id: int):
    """Adds an article to a user's recently viewed list."""
    user_deque = _recently_viewed_store[user_id]
    
    # If article is already in the list, remove it to re-add it at the front
    if article_id in user_deque:
        user_deque.remove(article_id)
        
    # Add the new article to the front (left side) of the deque
    user_deque.appendleft(article_id)

def get_viewed_articles(user_id: int) -> list[int]:
    """Retrieves the list of recently viewed article IDs for a user."""
    return list(_recently_viewed_store[user_id])