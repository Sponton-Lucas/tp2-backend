# Proyecto Flask - TP NRO 2 - BACKEND
## GRUPO: Caida del Siu
Este proyecto utiliza **Flask** como framework principal para desarrollo web.  

**Integrantes**
- Lucas Sponton
- Mia Torres
- Ivan Nolasco
- Thomas Alabart
- Sofia Ramirez
- Agustin Antonic
- Silvana Romero
- Alejandro Daniel Pinto

---

## 🚀 Requisitos previos

- Python 3.x instalado
- MySQL instalado y corriendo en localhost
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


## ⚙️ Configuración de la base de datos

1. **Entrar a MySql como root:**
   ```bash
   mysql -u root -p
   ```
2. **Crear la base de datos:**
   ```Sql
   CREATE DATABASE tp2_db;
   ```
3. **Crear el usuario del proyecto:**
   ```Sql
   CREATE USER 'caidaSiu'@'localhost' IDENTIFIED BY '1234';
   GRANT ALL PRIVILEGES ON tp2_db.* TO 'caidaSiu'@'localhost';
   FLUSH PRIVILEGES;
   ```
4. **Importar el esquema desde el archivo .sql:
- Primero debe pararse sobre la carpeta del repo en una terminal y luego ejecutar el comando siguiente:
   ```bash
   cd tp2-back-end   # entrar al repo clonado
   mysql -u caidaSiu -p tp2_db < data/archivo.sql
   ```

## ▶️ Levantar la API.
   ```bash
   python3 app.py
   ```
- La API corre en http://127.0.0.1:5000/.

---

## 📌 Endpoints principales

*Partidos*

- GET /partidos → Lista todos los partidos (con filtros por equipo, fecha, fase y paginación con _limit y _offset).
- GET /partidos/<id> → Muestra un partido específico.
- POST /partidos → Crea un nuevo partido.
- PUT /partidos/<id> → Reemplaza un partido completo.
- PATCH /partidos/<id> → Actualiza parcialmente un partido.
- DELETE /partidos/<id> → Elimina un partido por ID.
- PUT /partidos/<id>/resultado → Carga o reemplaza el resultado de un partido.
- POST /partidos/<id>/prediccion → Crea una predicción de un usuario para un partido.

*Usuarios*

- GET /usuarios → Lista todos los usuarios (con paginación con _limit y _offset).
- GET /usuarios/<id> → Muestra un usuario específico.
- POST /usuarios → Crea un nuevo usuario.
- PUT /usuarios/<id> → Reemplaza un usuario (si no existe, lo crea).
- DELETE /usuarios/<id> → Elimina un usuario por ID.

*Ranking*

- GET /ranking → Lista las predicciones de usuarios por puntaje (con paginación con _limit y _offset).

---

# Guía rápida de pruebas API de Partidos
Te documentamos cómo probar los endpoints de la API de partidos usando curl desde la terminal.

## 🔹 Pruebas con curl

1. **Listar todos los partidos**
```bash
curl http://127.0.0.1:5000/partidos
```
2. **Filtrar por categoria**
```bash
curl "http://127.0.0.1:5000/partidos?equipo=Boca Juniors" #Filtrar por equipo.
curl "http://127.0.0.1:5000/partidos?fecha=2025-08-19"     #Filtrar por fecha.
curl "http://127.0.0.1:5000/partidos?fase=cuartos"              #Filtrar por fase.
curl "http://127.0.0.1:5000/partidos?equipo=River Plate&fecha=2025-06-17&fase=grupos" #Filtrar por mas de una categoria.
```
3. **Ver detalle de un partido**
```bash
curl http://127.0.0.1:5000/partidos/1  #Mostrar el partido, por su ID,  que se quiere detallar.
```
4. **Crear un partido**
```bash
curl -X POST http://127.0.0.1:5000/partidos \
     -H "Content-Type: application/json" \
     -d '{"equipo_local":"Brasil","equipo_visitante":"Chile","fecha":"2026-06-15","fase":"grupos"}'
```
- *➡️ Los goles local y de visitante se pasaran mediante el endpoint con PUT*

5. **Cargar resultado**
```bash
curl -X PUT http://127.0.0.1:5000/partidos/1/resultado \
     -H "Content-Type: application/json" \
     -d '{"goles_local":2,"goles_visitante":1}'
```
6. **Crear predicción**
```bash
curl -X POST http://127.0.0.1:5000/partidos/1/prediccion \
     -H "Content-Type: application/json" \
     -d '{
           "usuario_id": 1,
           "goles_local": 2,
           "goles_visitante": 1
         }'
```
7. **Actualizar un partido**
```bash
curl -X PATCH http://127.0.0.1:5000/partidos/1 \
     -H "Content-Type: application/json" \
     -d '{
           "equipo_local": "Argentina",
           "equipo_visitante": "Brasil",
           "fecha":"2025-08-17",
           "fase": "semifinal"
         }'
```
8. **Reemplazar un partido**
```bash
curl -X PUT http://127.0.0.1:5000/partidos/1 \
     -H "Content-Type: application/json" \
     -d '{
           "equipo_local": "Argentina",
           "equipo_visitante": "Brasil",
           "fecha": "2026-07-01",
           "fase": "final"
         }'
```
9. **Eliminar un partido por su ID**
```bash
curl -X DELETE http://127.0.0.1:5000/partidos/2
```

---

## 🔹 Pruebas con Postman

### Abrí Postman y hacé click en **+** para una nueva request

### 1. Listar todos los partidos
- Método: `GET`
- URL: `http://127.0.0.1:5000/partidos`
- Click en **Send**

### 2. Filtrar partidos
- Método: GET
- URL:
   - http://127.0.0.1:5000/partidos?equipo=Boca Juniors
   - http://127.0.0.1:5000/partidos?fecha=2025-08-19
   - http://127.0.0.1:5000/partidos?fase=cuartos
   - http://127.0.0.1:5000/partidos?equipo=River Plate&fecha=2025-06-17&fase=grupos
   - Click en Send

### 3. Ver detalle de un partido
- Método: `GET`
- URL: `http://127.0.0.1:5000/partidos/1`
- Click en **Send**

### 4. Crear un partido
- Método: `POST`
- URL: `http://127.0.0.1:5000/partidos`
- Ir a **Body** → seleccionar **raw** → elegir **JSON**
```json
{
  "equipo_local": "Brasil",
  "equipo_visitante": "Chile",
  "fecha": "2026-06-15",
  "fase": "grupos"
}
```
- Click en **Send**

### 5. Cargar resultado
- Método: PUT
- URL: http://127.0.0.1:5000/partidos/1/resultado
- Ir a **Body** →seleccionar **raw** → elegir **JSON**
```json
{
  "goles_local": 2,
  "goles_visitante": 1
}
```
- Click en **Send**

### 6. Crear predicción
- Método: POST
- URL: http://127.0.0.1:5000/partidos/1/prediccion
- Ir a **Body** →seleccionar **raw** → elegir **JSON**
```json
{
  "usuario_id": 1,
  "goles_local": 2,
  "goles_visitante": 1
}
```
- Click en **Send**

### 7. Actualizar un partido
- Método: PATCH
- URL: http://127.0.0.1:5000/partidos/1
- Ir a **Body** →seleccionar **raw** → elegir **JSON**
```json
{
  "equipo_local": "Argentina",
  "equipo_visitante": "Brasil",
  "fecha": "2025-08-17",
  "fase": "semifinal"
}
```
- Click en **Send**

### 8. Reemplazar un partido
- Método: PUT
- URL: http://127.0.0.1:5000/partidos/1
- Ir a **Body** →seleccionar **raw** → elegir **JSON**
```json
{
  "equipo_local": "Argentina",
  "equipo_visitante": "Brasil",
  "fecha": "2026-07-01",
  "fase": "final"
}
```
- Click en **Send**


### 4. Eliminar un partido
- Método: `DELETE`
- URL: `http://127.0.0.1:5000/partidos/2`
- Click en **Send**

---

## 📂 Verificación

- Usar GET /partidos después de un POST o DELETE para validar que el partido se agregó o eliminó correctamente.

---

## ✅ Flujo de prueba recomendado

- GET /partidos → ver lista inicial.

- POST /partidos → crear un nuevo partido.

- GET /partidos → confirmar que se agregó.

- DELETE /partidos/<id> → eliminar un partido.

- GET /partidos → confirmar que se borró.
