import os
import shutil
from typer.testing import CliRunner
from neut.core.cli import app

runner = CliRunner()

def test_project_creation_and_structure():
    with runner.isolated_filesystem():
        result = runner.invoke(app, ["create-project", "test_project"])
        assert result.exit_code == 0
        
        assert os.path.exists("test_project")
        assert os.path.exists("test_project/main.py")
        assert os.path.exists("test_project/core/settings.py")
        assert os.path.exists("test_project/apps")

def test_app_creation_in_project():
    with runner.isolated_filesystem():
        runner.invoke(app, ["create-project", "test_project"])
        os.chdir("test_project")
        
        result = runner.invoke(app, ["create-app", "test_app"])
        assert result.exit_code == 0
        
        assert os.path.exists("apps/test_app")
        assert os.path.exists("apps/test_app/__init__.py")
        assert os.path.exists("apps/test_app/models.py")
        assert os.path.exists("apps/test_app/routes.py")