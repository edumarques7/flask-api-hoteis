from sql_alchemy import banco


class UserModel(banco.Model):
    __tablename__ = 'usuarios'
    
    id = banco.Column(banco.Integer, primary_key=True)
    login = banco.Column(banco.String(40))
    senha = banco.Column(banco.String(40))

    def __init__(self, login, senha):
        self.login = login
        self.senha = senha
     
        
    def json(self):
        return {
            'id': self.id,
            'login': self.login,

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