from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
app.config.from_object(Config)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)

from app import routes, models
from app.routes import start, stop

scheduler = BackgroundScheduler()
scheduler.add_job(start, 'cron', day_of_week= 'mon-fri', hour = 9, minute = 15, id = 'start_data')
scheduler.add_job(stop, 'cron', day_of_week= 'mon-fri', hour = 16, minute = 30, id = 'stop_data')