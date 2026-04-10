from flask import Flask, jsonify, request 
import db

app = Flask(__name__)

@app.route('/')
def home():
    return "API de Partidos funcionando. Usa /partidos para ver datos."


@app.route('/partidos', methods=['GET'])
def get_partidos():
    equipo = request.args.get('equipo')
    fecha = request.args.get('fecha')
    fase = request.args.get('fase')
    
    partidos = db.leer_partidos(equipo=equipo, fecha=fecha, fase=fase)
    if partidos:
        return jsonify(partidos), 200
    else:
        return jsonify({'error': 'filtrado incorrecto'}), 404

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
        gol_local = partido.get("goles_local", "")  #opcional
        gol_visitante = partido.get("goles_visitante", "")  #opcional
        estadio = partido.get("estadio", "")  #opcional
        ciudad = partido.get("ciudad", "")   #opcional
        nuevo_partido = db.crear_partido(equipo_local, equipo_visitante,estadio,ciudad,fecha, fase, gol_local, gol_visitante)
        return jsonify(nuevo_partido), 201
        
@app.route('/partidos/<int:id>', methods=['DELETE'])
def delete_partido(id):
    borrado = db.delete_partido_por_id(id)
    if borrado:
        return jsonify({'mensaje': 'partido borrado'}), 200
    else:
        return jsonify({'error': 'No se encuentra el partido'}), 404
    
@app.route('/partidos/<int:id>/resultado', methods=['PUT'])
def resultado_partido(id):
    datos = request.get_json()
    if (not datos) or ("goles_local" not in datos) or ("goles_visitante" not in datos):
        return jsonify({'error': 'No se envio la informacion pedida (gol local o gol visitante)'}), 400
    
    goles_local = datos.get("goles_local")
    goles_visitante = datos.get("goles_visitante")
    
    if goles_local < 0 or goles_visitante < 0:
        return jsonify({'error': 'Los goles no pueden ser negativos'}), 400
    
    resultado = db.agregar_resultado_por_id(id, goles_local, goles_visitante)
    if resultado:
        return jsonify({'mensaje': 'resultado cargado'}), 200
    else:
        return jsonify({'error': 'No se encuentra el partido'}), 404
    

if __name__ == '__main__':
	app.run(port=5000, debug=True)

