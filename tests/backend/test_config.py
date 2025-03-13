import os
import pytest
from backend.config import Settings

def test_settings_load():
    """Test that settings can be loaded from environment variables."""
    # Set test environment variables
    os.environ["TRIVIA_API"] = "https://test-api.com"
    os.environ["TRIVIA_TOKEN_API"] = "https://test-token-api.com"
    os.environ["TRIVIA_CATEGORY_API"] = "https://test-category-api.com"
    os.environ["DATABASE_URL"] = "sqlite:///test.db"
    os.environ["SECRET_KEY"] = "test-secret-key"
    
    # Create settings object
    settings = Settings()
    
    # Verify settings loaded correctly
    assert settings.TRIVIA_API == "https://test-api.com"
    assert settings.DATABASE_URL == "sqlite:///test.db"
    assert settings.SECRET_KEY == "test-secret-key"
    assert settings.SERVER_PORT == 8000  # Default value