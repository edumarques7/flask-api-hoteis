from flask_restful import Resource, reqparse
from models.site import SiteModel


class Sites(Resource):
    atributos = reqparse.RequestParser()
    atributos.add_argument('url', type=str, required=True, help="The field 'url' cannot be left blank")
    
    def get(self):
        return {'sites': [site.json() for site in SiteModel.query.all()]}
    
    def post(self):
        dados = Sites.atributos.parse_args()
        if SiteModel.find_site(dados['url']):
            return {"message": f"The site {dados['url']} already exists."}, 400
        site = SiteModel(**dados)
        try:
            site.save_site()
        except:
            return {'message': 'An internal error ocurred trying to create a new site.'}, 500
        return site.json()
    
class Site(Resource):
    def get(self, id):
        site = SiteModel.find_by_id(id)
        if site:
            return site.json()
        return {'message': 'Site not found.'}, 404
    

    
    def delete(self, id):
        site = SiteModel.find_by_id(id)
        if site:
            site.delete_site()
            return {'message': 'Site deleted.'}, 200
        return {'message': 'Site not found.'}, 404