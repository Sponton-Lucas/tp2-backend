# Proyecto Flask - TP NRO 2 - BACKEND

Este proyecto utiliza **Flask** como framework principal para desarrollo web.  

---

## 🚀 Requisitos previos
- Python 3.x instalado
- Git instalado
- (Opcional) VS Code como editor

---

## 📥 Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/Sponton-Lucas/tp2-back-end.git
   cd tp2-backend
   ```

2. **Crear entorno virtual**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate       # Windows
   ```

3. **Instalar dependencias**
   ```bash
   python3 -m pip install -r requirements.txt
   ```

---

# Guía rápida de pruebas API de Partidos

Te documentamos cómo probar los endpoints de la API de partidos usando curl desde la terminal.

##📌 Endpoints disponibles

- GET /partidos → Lista todos los partidos.

- GET /partidos/<id> → Muestra un partido específico.

- POST /partidos → Crea un nuevo partido.

- DELETE /partidos/<id> → Elimina un partido por ID.

---

##🔹 Pruebas con curl

1. **Listar todos los partidos**
```bash
curl http://127.0.0.1:5000/partidos
```
2. **Ver detalle de un partido**
```bash
curl http://127.0.0.1:5000/partidos/1
```
3. **Crear un partido (POST)**
```bash
curl -X POST http://127.0.0.1:5000/partidos \
     -H "Content-Type: application/json" \
     -d '{"equipo_local":"Brasil","equipo_visitante":"Chile","fecha":"2026-06-15","fase":"grupos","estadio":"Maracaná","ciudad":"Rio de Janeiro"}'
```
- *➡️ Si no se envían estadio y ciudad, se guardan vacíos:*
```bash
curl -X POST http://127.0.0.1:5000/partidos \
     -H "Content-Type: application/json" \
     -d '{"equipo_local":"Brasil","equipo_visitante":"Chile","fecha":"2026-06-15","fase":"grupos"}'
```
4. **Eliminar un partido por su ID (DELETE)**
```bash
curl -X DELETE http://127.0.0.1:5000/partidos/2
```
- *Si existe, devuelve:*
```bash
{"mensaje": "partido borrado"}
```
- *Si no existe, devuelve:*
```bash
{"error": "No se encuentra el partido"}
```

---

##📂 Verificación

- Revisar el archivo data/partidos.csv para confirmar que los cambios se reflejan.

- Usar GET /partidos después de un POST o DELETE para validar que el partido se agregó o eliminó correctamente.

---

##✅ Flujo de prueba recomendado

- GET /partidos → ver lista inicial.

- POST /partidos → crear un nuevo partido.

- GET /partidos → confirmar que se agregó.

- DELETE /partidos/<id> → eliminar un partido.

- GET /partidos → confirmar que se borró.