from db_extensions import database

class Tests(database.Model):
    __tablename__ = 'tests'
    __table_args__ = {'schema': 'tests_schema'}
    id = database.Column(database.Integer, primary_key=True)
    profession = database.Column(database.String(64), nullable=False)
    course = database.Column(database.Integer, nullable=False)
    question = database.Column(database.String(256), nullable=False)
    first_answer = database.Column(database.String(256), nullable=False)
    second_answer = database.Column(database.String(256), nullable=False)
    third_answer = database.Column(database.String(256), nullable=False)
    fourth_answer = database.Column(database.String(256), nullable=False)
    right_answer = database.Column(database.Integer, nullable=False)
    test_title = database.Column(database.String(128), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'profession': self.profession,
            'course': self.course,
            'question': self.question,
            'first_answer': self.first_answer,
            'second_answer': self.second_answer,
            'third_answer': self.third_answer,
            'fourth_answer': self.fourth_answer,
            'right_answer': self.right_answer,
            'test_title': self.test_title
        }

class TestCards(database.Model):
    __tablename__ = 'test_cards'
    __table_args__ = {'schema': 'tests_schema'}
    id = database.Column(database.Integer, primary_key=True)
    profession = database.Column(database.String(64), nullable=False)
    course = database.Column(database.Integer, nullable=False)
    test_title = database.Column(database.String(128), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'profession': self.profession,
            'course': self.course,
            'test_title': self.test_title,
        }