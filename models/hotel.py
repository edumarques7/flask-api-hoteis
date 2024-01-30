from sql_alchemy import banco


class HotelModel(banco.Model):
    __tablename__ = 'hoteis'
    
    id = banco.Column(banco.Integer, primary_key=True)
    nome = banco.Column(banco.String(80))
    estrelas = banco.Column(banco.Float(precision=1))
    diaria = banco.Column(banco.Float(precision=2))
    cidade = banco.Column(banco.String(40))
    site_id = banco.Column(banco.Integer, banco.ForeignKey('sites.id'))
    #site = banco.relationship('SiteModel')
   
    
    def __init__(self, nome, estrelas, diaria, cidade, site_id):
        
        self.nome = nome
        self.estrelas = estrelas
        self. diaria = diaria
        self.cidade = cidade
        self.site_id = site_id
        
    def json(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'estrelas': self.estrelas,
            'diaria': self.diaria,
            'cidade': self.cidade,
            'site_id': self.site_id
        }

    @classmethod
    def find_hotel_id(cls, id):
        hotel = cls.query.filter_by(id=id).first()
        if hotel:
            return hotel
        return None
    
    def save_hotel(self):
        banco.session.add(self)
        banco.session.commit()
        
    def update_hotel(self, nome, estrelas, diaria, cidade):
        self.nome = nome
        self.estrelas = estrelas
        self. diaria = diaria
        self.cidade = cidade
        
    def delete_hotel(self):
        banco.session.delete(self)
        banco.session.commit()
        
    def find_by_hotel(nome):
        hotel = HotelModel.query.filter_by(nome=nome).first()
        if hotel:
            return hotel
        return None