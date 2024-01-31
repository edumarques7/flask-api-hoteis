from sql_alchemy import banco
from flask import request, url_for
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


FROM_EMAIL = 'danzinhealer999@gmail.com'
API_KEY = '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'


class UserModel(banco.Model):
    __tablename__ = 'usuarios'
    
    id = banco.Column(banco.Integer, primary_key=True)
    login = banco.Column(banco.String(40), nullable=False, unique=True)
    senha = banco.Column(banco.String(40), nullable=False)
    email = banco.Column(banco.String(80), nullable=False, unique=True)
    ativado = banco.Column(banco.Boolean, default=False)

    def __init__(self, login, senha, ativado, email):
        self.login = login
        self.senha = senha
        self.ativado = ativado
        self.email = email
        

    def send_simple_message(self):
        link = request.url_root[:-1] + url_for('userconfirm', id=self.id)
        message = Mail(
            from_email=FROM_EMAIL,
            to_emails=self.email,
            subject='Confirmação de Cadastro',
            html_content=f'<html><p><b>Confirme seu cadastro clicando no link a seguir: </b> <a href="{link}">CONFIRMAR EMAIL</a></p></html>')
            
        sg = SendGridAPIClient(API_KEY)
        response = sg.send(message)
        print(response.status_code)
        print('Email enviado.')

        
        
    def json(self):
        return {
            'id': self.id,
            'login': self.login,
            'ativado': self.ativado,
            'email': self.email
        }

    @classmethod
    def find_user(cls, id):
        user = cls.query.filter_by(id=id).first()
        if user:
            return user
        return None
    
    
    def find_by_login(login):
        user = UserModel.query.filter_by(login=login).first()
        if user:
            return user
        return None
    
    def save_user(self):
        banco.session.add(self)
        banco.session.commit()

    def delete_user(self):
        banco.session.delete(self)
        banco.session.commit()
        
    def find_by_email(email):
        user = UserModel.query.filter_by(email=email).first()
        if user:
            return user
        return None