import json

def get_auth_token(client, username="testuser", password="password"):
    """Helper function to register and login a user to get a token."""
    client.post('/api/auth/register', data=json.dumps({
        'username': username,
        'password': password
    }), content_type='application/json')
    
    res = client.post('/api/auth/login', data=json.dumps({
        'username': username,
        'password': password
    }), content_type='application/json')
    
    return json.loads(res.data)['access_token']

def test_create_article(test_client):
    """Test creating an article successfully."""
    token = get_auth_token(test_client)
    headers = {'Authorization': f'Bearer {token}'}
    
    article_data = {
        'title': 'My First Article',
        'content': 'This is the content of the article.'
    }
    
    res = test_client.post('/api/articles', data=json.dumps(article_data), headers=headers, content_type='application/json')
    
    assert res.status_code == 201
    assert 'Article created' in str(res.data)

def test_get_article(test_client):
    """Test getting an article and tracking its view."""
    token = get_auth_token(test_client, "viewer", "password")
    headers = {'Authorization': f'Bearer {token}'}

    # Create an article first
    article_data = {'title': 'View Test', 'content': 'Content'}
    res = test_client.post('/api/articles', data=json.dumps(article_data), headers=headers, content_type='application/json')
    article_id = json.loads(res.data)['id']

    # Now, view the article
    res = test_client.get(f'/api/articles/{article_id}', headers=headers)
    assert res.status_code == 200
    assert 'View Test' in str(res.data)

    # Check if it was added to recently viewed
    res = test_client.get('/api/users/me/recently-viewed', headers=headers)
    assert res.status_code == 200
    recently_viewed_list = json.loads(res.data)
    assert len(recently_viewed_list) == 1
    assert recently_viewed_list[0]['id'] == article_id