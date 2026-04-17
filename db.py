import csv
import mysql.connector

db_config = {
    'host':'localhost',
    'user':'agustin',
    'password':'000000',
    'database':'tp2_db'
}

def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

def get_partidos(equipo, fecha, fase):
    coneccion = get_db_connection()
    cursor = coneccion.cursor(dictionary=True)
    try:
        cursor.execute('SELECT * FROM partidos WHERE ( (equipo_visitante = %s OR equipo_local = %s) OR %s IS NULL) AND (fecha = %s OR %s IS NULL) AND (fase = %s OR %s IS NULL);', (equipo, equipo, equipo, fecha, fecha, fase, fase,))
        partidos = cursor.fetchall()
        return partidos
    finally:
        cursor.close()
        coneccion.close()


def get_partido_por_id(id):
    id_ingresado = str(id)
    coneccion = get_db_connection()
    cursor = coneccion.cursor(dictionary=True)
    
    try:
        cursor.execute('SELECT * FROM partidos WHERE id = %s', (id_ingresado,))
        partido = cursor.fetchone()
        return partido
    finally:
        cursor.close()
        coneccion.close()

def delete_partido_por_id(id):
    id_ingresado = str(id)
    coneccion = get_db_connection()
    cursor = coneccion.cursor(dictionary=True)
    
    try:
        cursor.execute('DELETE FROM partidos WHERE id = %s', (id_ingresado,))
        coneccion.commit()
        return True
    finally:
        cursor.close()
        coneccion.close()  
  
def crear_partido(equipo_local, equipo_visitante,fecha, fase):
    coneccion = get_db_connection()
    cursor = coneccion.cursor(dictionary=True)
    
    try:
        cursor.execute('INSERT INTO partidos (equipo_visitante, equipo_local, fecha, fase) VALUES(%s, %s, %s, %s)', (equipo_visitante, equipo_local, fecha, fase,))
        coneccion.commit()
        return True
    finally:
            cursor.close()
            coneccion.close()

def agregar_resultado_por_id(id, goles_local, goles_visitante):
    coneccion = get_db_connection()
    cursor = coneccion.cursor(dictionary=True)
    id_ingresado = str(id)    

    try:
        cursor.execute('SELECT id FROM partidos WHERE id = %s', (id_ingresado,))    
        partido = cursor.fetchone()
        if not partido:
            return False
        else:
            cursor.execute('INSERT INTO resultados (partido_id, goles_visitante, goles_local) VALUES(%s, %s, %s) ON DUPLICATE KEY UPDATE goles_visitante = VALUES(goles_visitante), goles_local = VALUES(goles_local)', (id_ingresado, goles_visitante, goles_local,))
            coneccion.commit()
            return True
    finally:
        cursor.close()
        coneccion.close()


def actualizar_partido_por_id(id, equipo_local, equipo_visitante,fecha, fase):
    coneccion = get_db_connection()
    cursor = coneccion.cursor(dictionary=True)
    id_ingresado = str(id)  
    
    try:
        cursor.execute('SELECT id FROM partidos WHERE id = %s', (id_ingresado,))    
        partido = cursor.fetchone()
        if not partido:
            return False
        else:
            cursor.execute('UPDATE partidos SET equipo_local = %s, equipo_visitante = %s, fecha = %s, fase = %s WHERE id = %s', (equipo_local, equipo_visitante, fecha, fase, id_ingresado,))

            coneccion.commit()
            return True
    finally:
        cursor.close()
        coneccion.close()


def actualizar_partido_parcialmente_por_id(id, equipo_local, equipo_visitante,fecha, fase):
    coneccion = get_db_connection()
    cursor = coneccion.cursor(dictionary=True)
    id_ingresado = str(id)  
    
    try:
        cursor.execute('SELECT id FROM partidos WHERE id = %s', (id_ingresado,))    
        partido = cursor.fetchone()
        if not partido:
            return False
        else:
            cursor.execute('UPDATE partidos SET equipo_local = COALESCE(%s, equipo_local), equipo_visitante = COALESCE(%s, equipo_visitante), fecha = COALESCE(%s, fecha), fase = COALESCE(%s, fase) WHERE id = %s', (equipo_local, equipo_visitante, fecha, fase, id_ingresado,))

            coneccion.commit()
            return True
    finally:
        cursor.close()
        coneccion.close()


