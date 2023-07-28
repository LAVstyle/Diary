from flask_restx import Api, Resource, fields
import jwt
from .models import db, Users
from requests import request

rest_api = Api(version="1.0", title="Users API") # Инициализация API
# Инициализация валидатора для проверки данных из формы регистарции
signup_model = rest_api.model(
    'SignUpmodel', {
        "username": fields.String(required=True, min_length=2, max_length=32),
        "email": fields.String(required=True, min_length=4, max_length=64),
        "password": fields.String(required=True, min_length=4, max_length=16)
    }
)
# Обработчик данных при регистрации нового пользователя
@rest_api.route('/api/users/register')
class Register(Resource):
    """
        Регистрация нового пользователя в БД с использованием модели 'signup_model'
    """
    @rest_api.expect(signup_model, validate=True)
    def post(self):

        req_data = request.get_json()

        _username = req_data.get("username")
        _email = req_data.get("email")
        _password = req_data.get("password")

        user_exists = Users.get_by_email(_email)
        if user_exists:
            return {"success": False,
                "msg": "Email already taken"}, 400
        new_user = Users(username=_username, email=_email)

        new_user.set_password(_password)
        new_user.save()

        return {
            "success":True,
            "userID":new_user.id,
            "msg": "The user is redistered successully"
        }, 200
