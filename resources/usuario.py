from flask_restful import Resource, reqparse
from models.usuario import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from secrets import compare_digest
from blacklist import BLACKLIST
import traceback
from flask import make_response, render_template



atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help="The field 'login' cannot be left blank")
atributos.add_argument('senha', type=str, required=True, help="The field 'senha' cannot be left blank")
atributos.add_argument('ativado', type=bool)
atributos.add_argument('email', type=str,)


class User(Resource): 
    
    def get(self, id):
        user = UserModel.find_user(id)
        if user:
            return user.json()
        return {'message': 'User not found.'}, 404
    
    #@jwt_required()
    def delete(self, id):
        user = UserModel.find_user(id)
        if user:
            try:
                user.delete_user()
            except:
                return {'message': 'An internal erro ocurred to delete user.'}, 500
            return {'message': 'User deleted.'}, 200
        return {'message': 'User not found.'}, 404
    
class UserRegister(Resource):
    def post(self):
        dados = atributos.parse_args()
        if not dados['email'] or dados['email'] is None:
            return {"message": "The field 'email' cannot be left blank"}, 400
        
        if UserModel.find_by_email(dados['email']):
            return {"message": f"The email '{dados['email']}' already exists."}, 400

        if UserModel.find_by_login(dados['login']):
            return {"message": f"The {dados['login']} already exists."}
        
        user = UserModel(**dados)
        user.ativado = False
        try:
            user.save_user()
            user.send_simple_message()
        except:
            user.delete_user()
            traceback.print_exc()
            return {'message': 'An internal server error has ocurred.'}, 500
        return {'message': 'User created successfully! Please check your email or spam folder for confirmation.'}, 201
    
    
class UserLogin(Resource):
    @classmethod
    def post(cls):
        dados = atributos.parse_args()
        
        user = UserModel.find_by_login(dados['login'])
        
        if user and compare_digest(user.senha, dados['senha']):
            if user.ativado:
                token_de_acesso = create_access_token(identity=user.id)
                return {'access_token': token_de_acesso}, 200
            return {'message': 'User not confirmed.'}, 400
        return {'message': 'The username or password is incorrect.'}, 401
    
class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti']
        BLACKLIST.add(jwt_id)
        return {'message': 'logged out successfully!'}, 200
    

class UserConfirm(Resource):
    @classmethod
    def get(cls, id):
        user = UserModel.find_user(id)
        
        if not user:
            return {"message": f"User id {id} not found."}, 404
    
        user.ativado = True
        user.save_user()
        #return {"message": f"User id {id} confirmed successfully."}, 200
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('user_confirm.html', email=user.email, usuario=user.login), 200, headers)