from app import db


class Input_Results(db.Model):
    __tablename__ = 'input_results'

    id = db.Column(db.Integer, primary_key=True)
    user_input = db.Column(db.String(64))
    results = db.Column(db.String)

    def __repr__(self):
        return '<Input_Results %r>' % (self.user_input)
