from neut.core.app import NeutApp

def test_neut_app_creation(test_settings):
    app = NeutApp(title=test_settings.PROJECT_NAME)
    assert app.title == test_settings.PROJECT_NAME

def test_middleware_setup(test_app):
    assert len(test_app.user_middleware) > 0
