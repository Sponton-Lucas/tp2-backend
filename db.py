import csv

def leer_partidos(equipo, fecha, fase):
    with open("data/partidos.csv", "r") as archivo:
            lector = csv.DictReader(archivo)
            contenido = list(lector)

    contenido_filtrado = []

    if (not equipo) and (not fecha) and (not fase): #se fija si los parametros estan vacios
            return contenido

    if equipo and ((not fecha) and (not fase)): #solo filtra por equipo
        for i in range(len(contenido)):
            if (contenido[i]["equipo_local"] == equipo) or (contenido[i]["equipo_visitante"] == equipo):
                contenido_filtrado.append(contenido[i])
        return contenido_filtrado
         
    if fecha and ((not equipo) and (not fase)): #solo filtra por fecha
        for i in range(len(contenido)):
            if contenido[i]["fecha"] == fecha:
                contenido_filtrado.append(contenido[i])
        return contenido_filtrado

    if fase and ((not equipo) and (not fecha)): #filtra solo por fase
        for i in range(len(contenido)):
            if contenido[i]["fase"] == fase:
                contenido_filtrado.append(contenido[i])
        return contenido_filtrado

    if (equipo and fecha) and (not fase): #filtra por equipo y fecha
        for i in range(len(contenido)):
            if ((contenido[i]["equipo_local"] == equipo) or (contenido[i]["equipo_visitante"] == equipo)) and (contenido[i]["fecha"] == fecha): 
                contenido_filtrado.append(contenido[i])
        return contenido_filtrado
    
    if (equipo and fase) and (not fecha): #filtra por equipo y fase
        for i in range(len(contenido)):
            if ((contenido[i]["equipo_local"] == equipo) or (contenido[i]["equipo_visitante"] == equipo)) and (contenido[i]["fase"] == fase):
                contenido_filtrado.append(contenido[i])
        return contenido_filtrado
    
    if (fase and fecha) and (not equipo): #filtra por fecha y fase
        for i in range(len(contenido)):
            if (contenido[i]["fecha"] == fecha) and (contenido[i]["fase"] == fase):
                contenido_filtrado.append(contenido[i])
        return contenido_filtrado

    if equipo and fecha and fase: #filtra por equipo, fecha y fase
        for i in range(len(contenido)):
            if ((contenido[i]["equipo_local"] == equipo) or (contenido[i]["equipo_visitante"] == equipo)) and (contenido[i]["fecha"] == fecha) and (contenido[i]["fase"] == fase):
                contenido_filtrado.append(contenido[i])
        return contenido_filtrado
        


def get_partido_por_id(id):
    id_ingresado = str(id)
    with open("data/partidos.csv", "r") as archivo:
        lector = csv.DictReader(archivo)
        partidos = list(lector)
        for i in range(len(partidos)):
            if partidos[i]["id"] == id_ingresado:
                return partidos[i]

def crear_partido(equipo_local, equipo_visitante,estadio,ciudad,fecha, fase):
    partido = {
    "id": "",
    "equipo_local": equipo_local,
    "equipo_visitante": equipo_visitante,
    "estadio": estadio,
    "ciudad": ciudad,
    "fecha": fecha,
    "fase": fase
    }

    with open("data/partidos.csv", "r") as archivo:
        lector = csv.DictReader(archivo)
        contenido = list(lector)
        if contenido:
            max_id = max(int(p["id"]) for p in contenido)
        else:
            max_id = 0
    partido["id"] = max_id + 1

    with open("data/partidos.csv", "a") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=partido.keys())
        writer.writerow(partido)
    return partido

def delete_partido_por_id(id):
    id_ingresado = str(id)
    with open("data/partidos.csv", "r") as archivo:
        lector = csv.DictReader(archivo)
        partidos = list(lector)
    
    for i in range(len(partidos)):
        if partidos[i]["id"] == id_ingresado:
            del partidos[i]
            with open("data/partidos.csv", "w") as archivo:
                writer = csv.DictWriter(archivo, fieldnames=["id", "equipo_local", "equipo_visitante", "estadio", "ciudad", "fecha", "fase"])
                writer.writeheader()
                writer.writerows(partidos)
            return True
        
def agregar_resultado_por_id(id, goles_local, goles_visitante):
    id_ingresado = str(id)
    with open("data/partidos.csv", "r") as archivo:
        lector = csv.DictReader(archivo)
        partidos = list(lector)
    
    for i in range(len(partidos)):
        if partidos[i]["id"] == id_ingresado:
            partidos[i]["goles_local"] = goles_local
            partidos[i]["goles_visitante"] = goles_visitante
            with open("data/partidos.csv", "w") as archivo:
                writer = csv.DictWriter(archivo, fieldnames=partidos[i].keys())
                writer.writeheader()
                writer.writerows(partidos)
            return True
    
    return False
    
    return False
