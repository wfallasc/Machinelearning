from flask import Flask
from flask_restful import Api, Resource, reqparse
import pickle
import numpy as np
from flask import request

# variables Flask
app = Flask(__name__)
api = Api(app)


# se carga el modelo de Logistic Regression del Notebook #3
pkl_filename = "ModeloLR.pkl"
with open(pkl_filename, 'rb') as file:
    model = pickle.load(file)


class Predict(Resource):

    @staticmethod
    def post():
        # parametros
        parser = reqparse.RequestParser()
        parser.add_argument('petal_length')
        parser.add_argument('petal_width')
        parser.add_argument('sepal_length')
        parser.add_argument('sepal_width')

        # request para el modelo
        args = parser.parse_args() 
        datos = np.fromiter(args.values(), dtype=float) 

        # prediccion
        out = {'Prediccion': int(model.predict([datos])[0])}

        return out, 200

    # TODO: Define el def get()
    # ejercicio semanal
    @staticmethod
    @app.route('/get-predict')
    def get():

       # parser = reqparse.RequestParser()
        petal_length = request.args.get('petal_length') 
        petal_width = request.args.get('petal_width') 
        sepal_length = request.args.get('sepal_length') 
        sepal_width = request.args.get('sepal_width') 
        
        datos= [petal_length,petal_width,sepal_length,sepal_width]

        datos1 = np.fromiter(datos, dtype=float) 

        out = {'Prediccion': int(model.predict([datos1])[0])}

        return out, 200



api.add_resource(Predict, '/predict')

if __name__ == '__main__':
    app.run(debug=True, port='1080')