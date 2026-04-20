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
        'partidos': partidos,
        "_links": {
            "_first": {"href": f"/partidos?_limit={limit}&_offset=0{filtros}"},
            "_prev": {"href": f"/partidos?_limit={limit}&_offset={max(0, offset - limit)}{filtros}"} if offset > 0 else None,
            "_next": {"href": f"/partidos?_limit={limit}&_offset={min(last_offset, offset + limit)}{filtros}"} if (offset + limit) < total else None,
            "_last": {"href": f"/partidos?_limit={limit}&_offset={last_offset}{filtros}"}
        }
    }

    if partidos:
        return jsonify(respuesta), 200
    else:
        return '', 204

@app.route('/partidos/<int:id>', methods=['GET'])
def get_partido(id):
    partido = db.get_partido_por_id(id)
    if partido:
        return jsonify(partido)
    else:
        return jsonify({
            "errors": [
                {
                    "code": "404",
                    "message": "Partido no encontrado",
                    "level": "error",
                    "description": f"No existe partido con id {id}"
                }
            ]
        }), 404

@app.route('/partidos/<int:id>', methods=['DELETE'])
def delete_partido(id):
    borrado = db.delete_partido_por_id(id)
    if borrado:
        return '', 204
    else:
        return jsonify({
        "errors": [
            {
                "code": "404",
                "message": "Partido no encontrado",
                "level": "error",
                "description": f"No existe partido con id {id}"
            }
        ]
    }), 404

@app.route('/partidos', methods=['POST'])
def post_partido():
    partido = request.get_json()
    if not partido:
        return jsonify({
            "errors": [{
                "code": "400",
                "message": "Bad Request",
                "level": "error",
                "description": "Body vacio o invalido"
            }]
        }), 400
    if ("equipo_local" not in partido) or ("equipo_visitante" not in partido) or ("fecha" not in partido) or ("fase" not in partido):
        return jsonify({
            "errors": [{
                "code": "400",
                "message": "Bad Request",
                "level": "error",
                "description": "Faltan campos obligatorios"
            }]
        }), 400    
    else:
        equipo_local = partido.get("equipo_local")
        equipo_visitante = partido.get("equipo_visitante")
        fecha = partido.get("fecha")
        fase = partido.get("fase")
        if (not equipo_local) or (not equipo_visitante) or (not fecha) or (not fase):
            return jsonify({
            "errors": [{
                "code": "400",
                "message": "Bad Request",
                "level": "error",
                "description": "Los campos no pueden /ser vacios"
            }]
        }), 400
        partido_nuevo = db.crear_partido(equipo_local, equipo_visitante,fecha, fase)
        if partido_nuevo:
            return '', 201
        else:
            return jsonify({
                "errors": [{
                    "code": "409",
                    "message": "Conflict",
                    "level": "error",
                    "description": "No se pudo crear el partido"
                }]
            }), 400

@app.route('/partidos/<int:id>/resultado', methods=['PUT'])
def put_partidos_resultado(id):
    resultado = request.get_json()
    if (not resultado) or ("goles_visitante" not in resultado) or ("goles_local" not in resultado):
        return jsonify({
            "errors": [{
                "code": "400",
                "message": "Bad Request",
                "level": "error",
                "description": "Faltan goles_local o goles_visitante"
            }]
        }), 400
    else:
        goles_visitante = resultado.get("goles_visitante")
        goles_local = resultado.get("goles_local")
        if goles_local == "" or goles_visitante == "":
            return jsonify({
            "errors": [{
                "code": "400",
                "message": "Bad Request",
                "level": "error",
                "description": "Los goles no pueden ser nulos"
            }]
        }), 400
        
        if goles_local < 0 or goles_visitante < 0:
            return jsonify({
            "errors": [{
                "code": "400",
                "message": "Bad Request",
                "level": "error",
                "description": "Los goles no pueden ser negativos"
            }]
        }), 400

        resultado = db.agregar_resultado_por_id(id, goles_local, goles_visitante)

        if resultado:
             return '', 204
        else:
            return jsonify({
            "errors": [{
                "code": "404",
                "message": "Not Found",
                "level": "error",
                "description": "No existe el partido"
            }]
        }), 404

@app.route('/partidos/<int:id>', methods=['PUT'])
def put_partidos(id):
    partido = request.get_json()
    if (not partido) or ("equipo_local" not in partido) or ("equipo_visitante" not in partido) or ("fecha" not in partido) or ("fase" not in partido):
        return jsonify({
            "errors": [{
                "code": "400",
                "message": "Bad Request",
                "level": "error",
                "description": "Faltan campos obligatorios"
            }]
        }), 400
    else:
        equipo_local = partido.get("equipo_local")
        equipo_visitante = partido.get("equipo_visitante")
        fecha = partido.get("fecha")
        fase = partido.get("fase")
        actualizar_partido = db.actualizar_partido_por_id(id, equipo_local, equipo_visitante,fecha, fase)
        if actualizar_partido:
            return '', 204
        else:
            return jsonify({
            "errors": [{
                "code": "404",
                "message": "Not Found",
                "level": "error",
                "description": f"No existe partido con id {id}"
            }]
        }), 404


@app.route('/partidos/<int:id>', methods=['PATCH'])
def patch_partidos(id):
    partido = request.get_json()
    equipo_local = partido.get("equipo_local")
    equipo_visitante = partido.get("equipo_visitante")
    fecha = partido.get("fecha")
    fase = partido.get("fase")
    if equipo_local is not None and not equipo_local.strip():
        return jsonify({
            "errors": [{
                "code": "400",
                "message": "Bad Request",
                "level": "error",
                "description": "equipo_local no puede estar vacío"
            }]
        }), 400

    if equipo_visitante is not None and not equipo_visitante.strip():
        return jsonify({
            "errors": [{
                "code": "400",
                "message": "Bad Request",
                "level": "error",
                "description": "equipo_visitante no puede estar vacio"
            }]
        }), 400

    if fecha is not None and not fecha.strip():
        return jsonify({
            "errors": [{
                "code": "400",
                "message": "Bad Request",
                "level": "error",
                "description": "fecha no puede estar vacio"
            }]
        }), 400

    if fase is not None and not fase.strip():
        return jsonify({
            "errors": [{
                "code": "400",
                "message": "Bad Request",
                "level": "error",
                "description": "fase no puede estar vacia"
            }]
        }), 400

    actualizar_partido_parcialmente = db.actualizar_partido_parcialmente_por_id(id, equipo_local, equipo_visitante,fecha, fase)
    if actualizar_partido_parcialmente:
        return '', 204
    else:
        return jsonify({
            "errors": [{
                "code": "404",
                "message": "Not Found",
                "level": "error",
                "description": f"No existe partido con id {id}"
            }]
        }), 404


@app.route('/partidos/<int:id>/prediccion', methods=['POST'])
def post_prediccion(id):
    prediccion = request.get_json()
    if (not prediccion) or ("usuario_id" not in prediccion) or ("goles_visitante" not in prediccion) or ("goles_local" not in prediccion):
         return jsonify({
            "errors": [{
                "code": "400",
                "message": "Bad Request",
                "level": "error",
                "description": "Faltan campos obligatorios"
            }]
        }), 400
    else:
        usuario_id = prediccion.get("usuario_id")
        partido_id = id
        goles_local = prediccion.get("goles_local")
        goles_visitante = prediccion.get("goles_visitante")

    if goles_local is None or goles_visitante is None:
        return jsonify({'error': 'Faltan datos de goles.'}), 400

    if goles_local < 0 or goles_visitante < 0:
            return jsonify({
            "errors": [{
                "code": "400",
                "message": "Bad Request",
                "level": "error",
                "description": "Los goles no pueden ser negativos"
            }]
        }), 400

    partido = db.get_partido_por_id(partido_id) 
    if not partido:            
        return jsonify({
            "errors": [{
                "code": "404",
                "message": "Not Found",
                "level": "error",
                "description": "El partido no existe"
            }]
        }), 404
    if (partido['goles_local'] is not None) and (partido['goles_visitante'] is not None):
       return jsonify({
            "errors": [{
                "code": "400",
                "message": "Bad Request",
                "level": "error",
                "description": "El partido ya se jugó"
            }]
        }), 400
        
    usuario = db.obtener_usuario_por_id(usuario_id)
    if not usuario:
        return jsonify({
            "errors": [{
                "code": "404",
                "message": "Not Found",
                "level": "error",
                "description": "El usuario no existe"
            }]
        }), 404

    prediccion_hecha = db.hacer_prediccion(usuario_id, partido_id, goles_local, goles_visitante)
    if prediccion_hecha:
         return '', 201
    else:
        return jsonify({
            "errors": [{
                "code": "409",
                "message": "Conflict",
                "level": "error",
                "description": "Ya existe una prediccion para este usuario y partido"
            }]
        }), 400

@app.route('/usuarios', methods=['POST'])
def post_usuario():
    usuario = request.get_json()
    if (not usuario) or ("nombre" not in usuario) or ("email" not in usuario):
        return jsonify({
            "errors": [{
                "code": "400",
                "message": "Bad Request",
                "level": "error",
                "description": "Faltan campos obligatorios"
            }]
        }), 400
    else:
        nombre = usuario.get("nombre")
        email = usuario.get("email")
        usuario_nuevo = db.crear_usuario(nombre, email)
        if usuario_nuevo:
            return '', 201
        else:
            return jsonify({
            "errors": [{
                "code": "409",
                "message": "Conflict",
                "level": "error",
                "description": "No se pudo crear el usuario"
            }]
        }), 400

@app.route('/usuarios', methods=['GET']) 
def get_usuarios():
    limit = int(request.args.get('_limit', 10))
    offset = int(request.args.get('_offset', 0))

    usuarios, total = db.obtener_usuarios(limit, offset)

    last_offset = max(0, ((total - 1) // limit) * limit)

    respuesta = {
        'usuarios': usuarios,
        'total': total,
        '_links': {
            '_first': f'/usuarios?_limit={limit}&_offset=0',
            '_prev': f'/usuarios?_limit={limit}&_offset={max(0, offset - limit)}' if offset > 0 else None,
            '_next': f'/usuarios?_limit={limit}&_offset={min(last_offset, offset + limit)}' if (offset + limit) < total else None,
            '_last': f'/usuarios?_limit={limit}&_offset={last_offset}'
        }
    }

    return jsonify(respuesta)
    
@app.route('/usuarios/<int:id>', methods=['GET'])
def get_usuario_por_id(id):
    id_usuarios = db.obtener_usuario_por_id(id)
    if id_usuarios:
        return jsonify(id_usuarios)
    else:
        return jsonify({
            "errors": [{
                "code": "404",
                "message": "Not Found",
                "level": "error",
                "description": f"No existe usuario con id {id}"
            }]
        }), 404

@app.route('/usuarios/<int:id>', methods = ['PUT'])
def reemplazar_usuario(id):
    reemplazo_usuario = request.get_json()

    if (not reemplazo_usuario) or ("nombre" not in reemplazo_usuario) or ("email" not in reemplazo_usuario):
        return jsonify({
            "errors": [{
                "code": "400",
                "message": "Bad Request",
                "level": "error",
                "description": "datos incorrectos"
            }]
        }), 400

    nombre = reemplazo_usuario.get("nombre")
    email = reemplazo_usuario.get("email")

    usuario_existente = db.obtener_usuario_por_id(id)

    if usuario_existente:
        actualizado = db.actualizar_usuario_por_id(nombre, email, id)
        if actualizado:
             return '', 204
        else:
            return jsonify({'error':'No se pudo actualizar el usuario'}), 500
    else: 
        usuario_nuevo = db.crear_usuario_por_id(nombre, email, id)
        if usuario_nuevo:
            return jsonify({'message':'Se creo el usuario'}), 201
        else:
            return jsonify({'error':'No se pudo crear el usuario'}), 500

@app.route('/usuarios/<int:id>', methods=['DELETE'])
def delete_usuario(id):
    borrado = db.delete_usuario(id)
    if borrado:
        return '', 204
    else:
        return jsonify({
            "errors": [{
                "code": "404",
                "message": "Not Found",
                "level": "error",
                "description": f"No existe usuario con id {id}"
            }]
        }), 404

if __name__ == '__main__':
	app.run(port=5000, debug=True)  
