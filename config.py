import os

class Config:
    # Use a secure secret key from environment, fallback for local dev
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key-for-demo'
    
    # Use database URL from environment (Render/Postgres) or fallback to persistent/local SQLite
    _db_url = os.environ.get('DATABASE_URL')
    if not _db_url:
        # Check if Render persistent disk is configured
        disk_path = os.environ.get('RENDER_DISK_PATH')
        if disk_path:
            _db_url = f'sqlite:///{os.path.join(disk_path, "hostelkart.db")}'
        else:
            _db_url = 'sqlite:///hostelkart.db'
            
    # Fix for SQLAlchemy 1.4+ with Heroku/Render Postgres URIs
    if _db_url and _db_url.startswith("postgres://"):
        _db_url = _db_url.replace("postgres://", "postgresql://", 1)
        
    SQLALCHEMY_DATABASE_URI = _db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Secure Cookies in Production (HTTPS)
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
