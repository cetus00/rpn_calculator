from flask_sqlalchemy import SQLAlchemy

from calculator.models import Base

db = SQLAlchemy(model_class=Base)