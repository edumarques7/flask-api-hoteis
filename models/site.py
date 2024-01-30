from sql_alchemy import banco


class SiteModel(banco.Model):
    __tablename__ = 'sites'
    
    id = banco.Column(banco.Integer, primary_key=True)
    url = banco.Column(banco.String(80))
    hoteis = banco.relationship('HotelModel')
    
    def __init__(self, url):
        self.url = url

        
    def json(self):
        return {
            'id': self.id,
            'url': self.url,
            'hoteis': [hotel.json() for hotel in self.hoteis]
  
        }

    @classmethod
    def find_site(cls, url):
        site = cls.query.filter_by(url=url).first()
        if site:
            return site
        return None
    
    def save_site(self):
        banco.session.add(self)
        banco.session.commit()
        

    def delete_site(self):
        [hotel.delete_hotel() for hotel in self.hoteis]
        banco.session.delete(self)
        banco.session.commit()
    
        
    def find_by_id(id):
        site = SiteModel.query.filter_by(id=id).first()
        if site:
            return site
        return None
        