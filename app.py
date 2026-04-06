from flask import Flask, jsonify, request 
import db

app = Flask(__name__)

@app.route('/partidos', methods=['GET'])
def get_partidos():
    partidos = db.leer_partidos()
    return jsonify(partidos), 200

@app.route('/partidos/<int:id>', methods=['GET'])
def get_partido(id):
    partido = db.get_partido_por_id(id)
    if partido:
        return jsonify(partido), 200
    else:
        return jsonify({'error': 'No se encuentra el partido'}), 404

@app.route('/partidos', methods=['POST'])
def post_partido():
    partido = request.get_json()
    if (not partido) or ("equipo_local" not in partido) or ("equipo_visitante" not in partido) or ("fecha" not in partido) or ("fase" not in partido):
        return jsonify({'error': 'Algo falta'}), 400
    else:
        equipo_local = partido.get("equipo_local")
        equipo_visitante = partido.get("equipo_visitante")
        fecha = partido.get("fecha")
        fase = partido.get("fase")

        nuevo_partido = db.crear_partido(equipo_local, equipo_visitante, fecha, fase)
        return jsonify(nuevo_partido), 201
        
@app.route('/partidos/<int:id>', methods=['DELETE'])
def delete_partido(id):
    borrado = db.delete_partido_por_id(id)
    if borrado:
        return jsonify({'mensaje': 'partido borrado'}), 200
    else:
        return jsonify({'error': 'No se encuentra el partido'}), 404

if __name__ == '__main__':
	app.run(port=5000, debug=True)

