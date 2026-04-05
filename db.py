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
