from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from website import create_app, db

app = create_app()
migrate = Migrate(app, db)
