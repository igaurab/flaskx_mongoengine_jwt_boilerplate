import os
import unittest
import click

from app.main import create_app
from flask_script import Manager
from app import blueprint

app = create_app(os.getenv("APP_ENVIRONMENT") or "dev")
app.register_blueprint(blueprint)
app.app_context().push()

manager = Manager(app)


@manager.command
def run():
    app.run()


@manager.command
def test():
    """Runs unit test"""
    tests = unittest.TestLoader().discover("app/test", pattern="test*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == "__main__":
    manager.run()
