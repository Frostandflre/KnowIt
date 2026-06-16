from db_schema.db_extensions import database

class Users(database.Model):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'users_schema'}
    user_id = database.Column(database.Integer,primary_key=True)
    nickname = database.Column(database.String(64), unique=True, index=True)
    password = database.Column(database.String(512))
    email = database.Column(database.String(120), unique=True, index=True)
    group = database.Column(database.String(64), index=True)
    average_score = database.Column(database.Float(), index=True)
    is_teacher = database.Column(database.Boolean, default=False)
    created_at = database.Column(database.DateTime, server_default=database.func.now(), nullable=False)

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "nickname": self.nickname,
            "email": self.email,
            "group": self.group,
            "average_score": self.average_score if self.average_score is not None else 0.00,
            "is_teacher": self.is_teacher,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }