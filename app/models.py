from app import db

class Yesterday(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    yesterday = db.Column(db.Float, nullable= False)
    name = db.Column(db.String, nullable= False)
