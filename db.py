import csv

def leer_partidos():
    with open("data/partidos.csv", "r") as archivo:
        lector = csv.DictReader(archivo)
        contenido = list(lector)
        return contenido

#return contenido[1]

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
    
    return False