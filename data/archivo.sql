CREATE DATABASE tp2_db;
USE tp2_db;

CREATE TABLE partidos (
	id INT AUTO_INCREMENT PRIMARY KEY,
	equipo_visitante varchar(100) NOT NULL,
	equipo_local varchar(100) NOT NULL,
	fecha DATE NOT NULL,
	fase varchar(100) NOT NULL  /* Posible cambio de unificar tablas(o añadir) la tabla resultados a tabla partidos. por el hecho de que deberia poder estar vacios los campos de goles, para luego la tabla de predicciones.*/
);

CREATE TABLE resultados (
	partido_id INT PRIMARY KEY,
	goles_visitante INT NOT NULL,    /* Esto deberia admitir q sea null, lo probar desp con la funcion de predicciones. */
	goles_local INT NOT NULL,   /* Esto deberia admitir q sea null, lo probar desp con la funcion de predicciones. */
	FOREIGN KEY (partido_id) REFERENCES partidos(id) ON DELETE CASCADE
);

CREATE TABLE usuarios (
	id INT AUTO_INCREMENT PRIMARY KEY,
	nombre varchar(100) NOT NULL,
	email varchar(100) UNIQUE NOT NULL
);

CREATE TABLE predicciones (
	id INT AUTO_INCREMENT PRIMARY KEY,
	usuario_id INT NOT NULL,
	partido_id INT NOT NULL,
	goles_visitante INT NOT NULL,
	goles_local INT NOT NULL,
	UNIQUE (usuario_id, partido_id),
	FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
	FOREIGN KEY (partido_id) REFERENCES partidos(id) ON DELETE CASCADE
);
