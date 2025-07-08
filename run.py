import os
from app import create_app

# Load config from environment variable or use DevelopmentConfig as default
config_name = os.getenv('FLASK_CONFIG', 'development')
app = create_app(config_name)

if __name__ == '__main__':
    app.run()