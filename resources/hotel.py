from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required
from models.site import SiteModel




class Hoteis(Resource):
    query_params = reqparse.RequestParser()
    query_params.add_argument("cidade", type=str, default="", location="args")
    query_params.add_argument("estrelas_min", type=float, default=0, location="args")
    query_params.add_argument("estrelas_max", type=float, default=0, location="args")
    query_params.add_argument("diaria_min", type=float, default=0, location="args")
    query_params.add_argument("diaria_max", type=float, default=0, location="args")
    query_params.add_argument("limit",type=float, default=100, location="args")
    query_params.add_argument("offset",type=float, default=0, location="args")
 
    def get(self):
        filters = Hoteis.query_params.parse_args()
 
        query = HotelModel.query
 
        if filters["cidade"]:
            query = query.filter(HotelModel.cidade == filters["cidade"])
        if filters["estrelas_min"]:
            query = query.filter(HotelModel.estrelas >= filters["estrelas_min"])
        if filters["estrelas_max"]:
            query = query.filter(HotelModel.estrelas <= filters["estrelas_max"])
        if filters["diaria_min"]:
            query = query.filter(HotelModel.diaria >= filters["diaria_min"])
        if filters["diaria_max"]:
            query = query.filter(HotelModel.diaria <= filters["diaria_max"])
        if filters["limit"]:
            query = query.limit(filters["limit"])
        if filters["offset"]:
            query = query.offset(filters["offset"])
 
        return {"hoteis": [hotel.json() for hotel in query]}
    
    def post(self):
        dados = Hotel.atributos.parse_args()
        if HotelModel.find_by_hotel(dados['nome']):
            return {"message": f"The {dados['nome']} already exists."}, 400
    
        
        hotel = HotelModel(**dados)
        
        if not SiteModel.find_by_id(dados["site_id"]):
            
            return {"message": f"The hotel id '{dados['site_id']}' must be associated to a valid site id."}, 400
        try:
            hotel.save_hotel()
        except:
            return {'message': 'An internal erro ocurred to save hotel.'}, 500
        return hotel.json(), 201
    
class Hotel(Resource):
        
    atributos = reqparse.RequestParser()
    atributos.add_argument('nome', type=str, required=True, help="The field 'nome' cannot be left blank")
    atributos.add_argument('estrelas', type=str, required=True, help="The field 'estrelas' cannot be left blank")
    atributos.add_argument('diaria')
    atributos.add_argument('cidade')
    atributos.add_argument('site_id', type=int, required=True, help="Every hotel needs to be linked with a site.")
    
    
    def get(self, id):
        hotel = HotelModel.find_hotel_id(id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel not found.'}, 404
    
    #@jwt_required()
    def put(self, id):
        
        dados = Hotel.atributos.parse_args()
        hotel_encrontrado = HotelModel.find_hotel_id(id)
        if hotel_encrontrado:
            hotel_encrontrado.update_hotel(**dados)
            hotel_encrontrado.save_hotel()
            return hotel_encrontrado.json(), 200
        hotel = HotelModel(id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {'message': 'An internal erro ocurred to save hotel.'}, 500
        return hotel.json(), 201
    

    #@jwt_required()
    def delete(self, id):
        hotel = HotelModel.find_hotel_id(id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message': 'An internal erro ocurred to delete hotel.'}, 500
            return {'message': 'Hotel deleted.'}, 200
        return {'message': 'Hotel not found.'}, 404
    
    