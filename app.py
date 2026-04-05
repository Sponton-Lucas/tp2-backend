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



if __name__ == '__main__':
	app.run(port=5000, debug=True)

