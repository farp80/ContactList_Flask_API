from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(80), unique=True, nullable=False)
    phone = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    agenda_slug = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return '<Contact %r>' % self.full_name

    def serialize(self):
        return{
            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            "agenda_slug": self.agenda_slug,
            "id": self.id
        }
