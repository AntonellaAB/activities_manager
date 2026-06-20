DROP TABLE IF EXISTS usuarios CASCADE;
DROP TABLE IF EXISTS materias CASCADE;
DROP TABLE IF EXISTS profesor_materias CASCADE;
DROP TABLE IF EXISTS horas_extension CASCADE;

-- USUARIOS
CREATE TABLE usuarios (
    id_user SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(250) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    rol VARCHAR(20) NOT NULL,
    CONSTRAINT usuarios_rol_check CHECK (rol IN ('estudiante', 'profesor', 'admin'))
);

-- MATERIAS
CREATE TABLE materias (
    id_materias SERIAL PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL
);

-- PROFESORES MATERIAS (Tabla intermedia corregida con INTEGER)
CREATE TABLE profesor_materias (
    profesor_id INTEGER NOT NULL, -- Corregido: Ahora recibe el ID existente del profesor
    materia_id INTEGER NOT NULL,  -- Corregido: Ahora recibe el ID existente de la materia
    PRIMARY KEY(profesor_id, materia_id),
    FOREIGN KEY (profesor_id) REFERENCES usuarios(id_user) ON DELETE CASCADE,
    FOREIGN KEY (materia_id) REFERENCES materias(id_materias) ON DELETE CASCADE
);

-- HORAS EXTENSION 
CREATE TABLE horas_extension (
    id SERIAL PRIMARY KEY NOT NULL,
    alumno_id INTEGER REFERENCES usuarios(id_user) ON DELETE CASCADE,
    semestre INTEGER NOT NULL,
    ubicacion VARCHAR(250) NOT NULL,
    materia_id INTEGER REFERENCES materias(id_materias),
    profesor_id INTEGER REFERENCES usuarios(id_user),
    fecha DATE NOT NULL,
    horas INTEGER NOT NULL,
    informe TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT horas_extension_semestre_check CHECK (semestre BETWEEN 1 AND 12)
); -- Cambiar el nombre del informe a descripcion

CREATE TABLE actividades(
    id_acti SERIAL PRIMARY KEY,
    tipo VARCHAR(20) NOT NULL,
    CONSTRAINT tipo_check CHECK (tipo IN ('EXTRA-MURO', 'INTRA-MURO')),
    subtipo VARCHAR(20) NOT NULL,
    CONSTRAINT tipo_check CHECK (tipo IN ('cat1', 'cat2', 'cat3', 'cat4', 'cat5', 'cat6', 'cat7')),
);


--ALTER TABLE horas_extension cambiar nombre