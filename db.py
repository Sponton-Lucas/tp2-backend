import mysql.connector

db_config = {
    'host':'localhost',
    'user':'caidaSiu',
    'password':'1234',
    'database':'tp2_db'
}

def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

def get_partidos(equipo, fecha, fase, limit, offset):
    coneccion = get_db_connection()
    cursor = coneccion.cursor(dictionary=True)
    try:
        cursor.execute('SELECT COUNT(*) as total FROM partidos WHERE ( (equipo_visitante = %s OR equipo_local = %s) OR %s IS NULL) AND (fecha = %s OR %s IS NULL) AND (fase = %s OR %s IS NULL);', (equipo, equipo, equipo, fecha, fecha, fase, fase))
        total = cursor.fetchone()['total']

        cursor.execute('SELECT * FROM partidos WHERE ( (equipo_visitante = %s OR equipo_local = %s) OR %s IS NULL) AND (fecha = %s OR %s IS NULL) AND (fase = %s OR %s IS NULL) LIMIT %s OFFSET %s;',(equipo, equipo, equipo, fecha, fecha, fase, fase, limit,  offset))
        partidos = cursor.fetchall()

        return partidos, total
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
        cursor.execute('SELECT * FROM partidos WHERE id = %s', (id_ingresado,))
        existe_partido = cursor.fetchone()
        if not existe_partido:
            return False
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


def hacer_prediccion(usuario_id, partido_id, goles_local, goles_visitante):
    coneccion = get_db_connection()
    cursor = coneccion.cursor(dictionary=True)

    try:
        # Buscar partido
        cursor.execute("SELECT id FROM partidos WHERE id = %s", (partido_id,))
        partido = cursor.fetchone()
        if not partido:
            return False
        
        # Buscar usuario
        cursor.execute("SELECT id FROM usuarios WHERE id = %s", (usuario_id,))
        usuario = cursor.fetchone()
        if not usuario:
            return False
        
        # cursor.execute("SELECT  goles_visitante goles_local FROM resultados WHERE goles_visitante IS NULL or goles_local IS NULL")
        # se refiere a resultados, pero primero hay que hacer el cambio de los goles, agregarlos a la tabla partidos.

        cursor.execute("SELECT usuario_id FROM predicciones WHERE usuario_id = %s AND partido_id = %s", (usuario_id, partido_id))
        prediccion_hecha = cursor.fetchone()
        if prediccion_hecha:
            return False, 'No se puede hacer mas de una prediccion por partido.', 400   #esto esta para probar, no sabemos si se puede devolver todo esto.

        cursor.execute('INSERT INTO predicciones (usuario_id, partido_id, goles_local, goles_visitante) VALUES(%s, %s, %s, %s)', (usuario_id, partido_id, goles_local, goles_visitante))
        coneccion.commit()
        return True
    finally:
            cursor.close()
            coneccion.close()

def crear_usuario(nombre, email):
    coneccion = get_db_connection()
    cursor = coneccion.cursor(dictionary=True)
    try:
        cursor.execute('INSERT INTO usuarios (nombre, email) VALUES(%s, %s)', (nombre, email,))
        coneccion.commit()
        return True
    finally:
            cursor.close()
            coneccion.close()

def obtener_usuarios():
    coneccion = get_db_connection()
    cursor = coneccion.cursor(dictionary=True)
    
    try:
        cursor.execute('SELECT * FROM usuarios')
        todos_usuarios = cursor.fetchall()
        return todos_usuarios
    finally:
        cursor.close()
        coneccion.close()

def obtener_usuario_por_id(id):
    coneccion = get_db_connection()
    cursor = coneccion.cursor(dictionary=True)

    try:
        cursor.execute('SELECT * FROM usuarios WHERE id = %s', (id,))
        id_encontrado = cursor.fetchall()
        if id_encontrado:
            return id_encontrado
        else:
            return False
    finally:
        cursor.close()
        coneccion.close()

def actualizar_usuario_por_id(nombre, email, id):
    coneccion = get_db_connection()
    cursor = coneccion.cursor(dictionary=True)

    try:
        cursor.execute('UPDATE usuarios SET nombre = %s, email = %s WHERE id = %s', (nombre, email, id,))
        coneccion.commit()
        return True
    finally:
        cursor.close()
        coneccion.close()

def crear_usuario_por_id(nombre, email, id):
    coneccion = get_db_connection()
    cursor = coneccion.cursor(dictionary=True)

    try:
        cursor.execute('INSERT INTO usuarios (nombre, email, id) VALUES(%s, %s, %s)', (nombre, email, id,))
        coneccion.commit()
        return True
    finally:
        cursor.close()
        coneccion.close() 
