from flask import Flask, jsonify, request 
import db
import mysql.connector

app = Flask(__name__)

@app.route('/')
def home():
    return "API de Partidos funcionando. Usa /partidos para ver datos."


@app.route('/partidos', methods=['GET'])
def get_partidos():
    equipo = request.args.get('equipo')
    fecha = request.args.get('fecha')
    fase = request.args.get('fase')
    limit = int (request.args.get('_limit', 10))
    offset = int (request.args.get('_offset', 0))

    partidos, total = db.get_partidos(equipo=equipo, fecha=fecha, fase=fase, limit=limit, offset=offset)

    filtros= ''
    if equipo: filtros += f'&equipo={equipo}'
    if fase: filtros += f'&fase={fase}'
    if fecha: filtros += f'&fecha={fecha}'

    last_offset = max(0, ((total - 1) // limit) * limit)

    respuesta = {
        'data': partidos,
        'total': total,
        '_first': f'/partidos?_limit={limit}&_offset=0{filtros}',
        '_prev': f'/partidos?_limit={limit}&_offset={max(0, offset - limit)}{filtros}' if offset > 0 else None,
        '_next': f'/partidos?_limit={limit}&_offset=(min(last_offset, offset + limit)){filtros}' if (offset + limit) < total else None,
        '_last': f'/partidos?_limit={limit}&_offset={last_offset}{filtros}'
    }

    if partidos:
        return jsonify(respuesta)
    else:
        return jsonify({'error': 'error'}), 404

@app.route('/partidos/<int:id>', methods=['GET'])
def get_partido(id):
    partido = db.get_partido_por_id(id)
    if partido:
        return jsonify(partido)
    else:
        return jsonify({'error': 'Partido no encontrado'}), 404

@app.route('/partidos/<int:id>', methods=['DELETE'])
def delete_partido(id):
    borrado = db.delete_partido_por_id(id)
    if borrado:
        return jsonify({'mensaje': 'partido borrado'}), 200
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
        partido_nuevo = db.crear_partido(equipo_local, equipo_visitante,fecha, fase)
        if partido_nuevo:
            return jsonify({'message': 'partido creado'}), 201
        else:
            return jsonify({'error': 'no se pudo crea el partido'}), 400

@app.route('/partidos/<int:id>/resultado', methods=['PUT'])
def put_partidos_resultado(id):
    resultado = request.get_json()
    if (not resultado) or ("goles_visitante" not in resultado) or ("goles_local" not in resultado):
        return jsonify({'error': 'Algo falta'}), 400
    else:
        goles_visitante = resultado.get("goles_visitante")
        goles_local = resultado.get("goles_local")
        
        if goles_local < 0 or goles_visitante < 0:
            return jsonify({'error': 'Los goles no pueden ser negativos'}), 400
        resultado = db.agregar_resultado_por_id(id, goles_local, goles_visitante)

        if resultado:
            return jsonify({'mensaje': 'resultado cargado'}), 200
        else:
            return jsonify({'error': 'No se encuentra el partido para actualizar'}), 404

@app.route('/partidos/<int:id>', methods=['PUT'])
def put_partidos(id):
    partido = request.get_json()
    if (not partido) or ("equipo_local" not in partido) or ("equipo_visitante" not in partido) or ("fecha" not in partido) or ("fase" not in partido):
        return jsonify({'error': 'Algo falta'}), 400
    else:
        equipo_local = partido.get("equipo_local")
        equipo_visitante = partido.get("equipo_visitante")
        fecha = partido.get("fecha")
        fase = partido.get("fase")
        actualizar_partido = db.actualizar_partido_por_id(id, equipo_local, equipo_visitante,fecha, fase)
        if actualizar_partido:
            return jsonify({'message': 'partido actualizado'}), 201
        else:
            return jsonify({'error': 'no se pudo actualizar el partido'}), 404


@app.route('/partidos/<int:id>', methods=['PATCH'])
def patch_partidos(id):
    partido = request.get_json()
    equipo_local = partido.get("equipo_local")
    equipo_visitante = partido.get("equipo_visitante")
    fecha = partido.get("fecha")
    fase = partido.get("fase")
    actualizar_partido_parcialmente = db.actualizar_partido_parcialmente_por_id(id, equipo_local, equipo_visitante,fecha, fase)
    if actualizar_partido_parcialmente:
        return jsonify({'message': 'partido actualizado parcialmente'}), 201
    else:
        return jsonify({'error': 'no se pudo actualizar el partido'}), 404


if __name__ == '__main__':
	app.run(port=5000, debug=True)  
