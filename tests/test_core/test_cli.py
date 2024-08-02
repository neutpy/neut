from typer.testing import CliRunner
from neut.core.cli import app

runner = CliRunner()

def test_create_project():
    result = runner.invoke(app, ["create-project", "test_project"])
    assert result.exit_code == 0
    assert "Creating new Neut project: test_project" in result.output

def test_create_app():
    result = runner.invoke(app, ["create-app", "test_app"])
    assert result.exit_code == 0
    assert "Creating new Neut app: test_app" in result.output