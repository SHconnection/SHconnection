import os
import sys
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from shapp import db, create_app
from shapp.models import Teacher, Theclass

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(
            app = app,
            db = db
            )


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
