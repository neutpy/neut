from neut.core.settings import NeutSettings

def test_settings_default_values():
    settings = NeutSettings()
    assert settings.PROJECT_NAME == "Neut Project"
    assert settings.DEBUG is False
    assert settings.DATABASE_URL == "sqlite:///./neut.db"

def test_settings_override():
    settings = NeutSettings(PROJECT_NAME="Custom Project", DEBUG=True)
    assert settings.PROJECT_NAME == "Custom Project"
    assert settings.DEBUG is True