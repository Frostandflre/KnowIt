from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, SubmitField
from wtforms.validators import DataRequired, Email,ValidationError

class RegistrationForm(FlaskForm):
    nickname = StringField('Имя', [DataRequired()])
    email = StringField('Электронная почта', [DataRequired(), Email()])
    password = StringField('Пароль', [DataRequired()])
    group = StringField('Группа')
    teacher_code = StringField('Специальный код доступа')
    submit = SubmitField('Зарегистрироваться')

    def validate_group(self, field):
        if field.data:
            allowed_groups = ["121/125/137","122/124","123/138","131/135","132/134","133/136","141","142/144","143/146","145","151","152","153","155","221/225","222/228","223","224/226","231/242","232/236","233/238","234","235","241","242/247","243/248","244/249","245","246","251","252","253","254","255","256","257","321/322/333","331/332","341/342","351","421/422","431/433","432","441/443","442","451","452","453","521/524","522/534","531","532","533","551","552","553","541","542","543"]

            if field.data not in allowed_groups:
                raise ValidationError('Выбранной группы не существует. Пожалуйста, выберите из списка.')

class AuthorizationForm(FlaskForm):
    email = StringField('Электронная почта', [DataRequired(), Email()])
    password = StringField('Пароль', [DataRequired()])
    submit = SubmitField('Войти')