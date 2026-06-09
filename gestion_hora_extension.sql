--
-- PostgreSQL database dump
--

\restrict fjPsyTVPGWnlY8TzQ15xXGEvIkx5D0OMxdGccVs75bKZcmbiEaiPc1w8L1QpyaG

-- Dumped from database version 18.0
-- Dumped by pg_dump version 18.0

-- Started on 2026-06-08 23:01:00

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 225 (class 1259 OID 32930)
-- Name: horas_extension; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.horas_extension (
    id integer NOT NULL,
    alumno_id integer,
    semestre integer NOT NULL,
    ubicacion character varying(150) NOT NULL,
    materia_id integer,
    profesor_id integer,
    horas integer NOT NULL,
    fecha date NOT NULL,
    informe text,
    fecha_registro timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT horas_extension_semestre_check CHECK (((semestre >= 1) AND (semestre <= 12)))
);


ALTER TABLE public.horas_extension OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 32929)
-- Name: horas_extension_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.horas_extension_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.horas_extension_id_seq OWNER TO postgres;

--
-- TOC entry 4944 (class 0 OID 0)
-- Dependencies: 224
-- Name: horas_extension_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.horas_extension_id_seq OWNED BY public.horas_extension.id;


--
-- TOC entry 222 (class 1259 OID 32902)
-- Name: materias; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.materias (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL
);


ALTER TABLE public.materias OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 32901)
-- Name: materias_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.materias_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.materias_id_seq OWNER TO postgres;

--
-- TOC entry 4945 (class 0 OID 0)
-- Dependencies: 221
-- Name: materias_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.materias_id_seq OWNED BY public.materias.id;


--
-- TOC entry 223 (class 1259 OID 32912)
-- Name: profesor_materias; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.profesor_materias (
    profesor_id integer NOT NULL,
    materia_id integer NOT NULL
);


ALTER TABLE public.profesor_materias OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 32888)
-- Name: usuarios; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuarios (
    id integer NOT NULL,
    email character varying(100) NOT NULL,
    password_hash character varying(255) NOT NULL,
    rol character varying(20) NOT NULL,
    CONSTRAINT usuarios_rol_check CHECK (((rol)::text = ANY ((ARRAY['estudiante'::character varying, 'profesor'::character varying])::text[])))
);


ALTER TABLE public.usuarios OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 32887)
-- Name: usuarios_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.usuarios_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.usuarios_id_seq OWNER TO postgres;

--
-- TOC entry 4946 (class 0 OID 0)
-- Dependencies: 219
-- Name: usuarios_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.usuarios_id_seq OWNED BY public.usuarios.id;


--
-- TOC entry 4771 (class 2604 OID 32933)
-- Name: horas_extension id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.horas_extension ALTER COLUMN id SET DEFAULT nextval('public.horas_extension_id_seq'::regclass);


--
-- TOC entry 4770 (class 2604 OID 32905)
-- Name: materias id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.materias ALTER COLUMN id SET DEFAULT nextval('public.materias_id_seq'::regclass);


--
-- TOC entry 4769 (class 2604 OID 32891)
-- Name: usuarios id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios ALTER COLUMN id SET DEFAULT nextval('public.usuarios_id_seq'::regclass);


--
-- TOC entry 4786 (class 2606 OID 32944)
-- Name: horas_extension horas_extension_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.horas_extension
    ADD CONSTRAINT horas_extension_pkey PRIMARY KEY (id);


--
-- TOC entry 4780 (class 2606 OID 32911)
-- Name: materias materias_nombre_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.materias
    ADD CONSTRAINT materias_nombre_key UNIQUE (nombre);


--
-- TOC entry 4782 (class 2606 OID 32909)
-- Name: materias materias_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.materias
    ADD CONSTRAINT materias_pkey PRIMARY KEY (id);


--
-- TOC entry 4784 (class 2606 OID 32918)
-- Name: profesor_materias profesor_materias_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.profesor_materias
    ADD CONSTRAINT profesor_materias_pkey PRIMARY KEY (profesor_id, materia_id);


--
-- TOC entry 4776 (class 2606 OID 32900)
-- Name: usuarios usuarios_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_email_key UNIQUE (email);


--
-- TOC entry 4778 (class 2606 OID 32898)
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (id);


--
-- TOC entry 4789 (class 2606 OID 32945)
-- Name: horas_extension horas_extension_alumno_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.horas_extension
    ADD CONSTRAINT horas_extension_alumno_id_fkey FOREIGN KEY (alumno_id) REFERENCES public.usuarios(id) ON DELETE CASCADE;


--
-- TOC entry 4790 (class 2606 OID 32950)
-- Name: horas_extension horas_extension_materia_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.horas_extension
    ADD CONSTRAINT horas_extension_materia_id_fkey FOREIGN KEY (materia_id) REFERENCES public.materias(id);


--
-- TOC entry 4791 (class 2606 OID 32955)
-- Name: horas_extension horas_extension_profesor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.horas_extension
    ADD CONSTRAINT horas_extension_profesor_id_fkey FOREIGN KEY (profesor_id) REFERENCES public.usuarios(id);


--
-- TOC entry 4787 (class 2606 OID 32924)
-- Name: profesor_materias profesor_materias_materia_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.profesor_materias
    ADD CONSTRAINT profesor_materias_materia_id_fkey FOREIGN KEY (materia_id) REFERENCES public.materias(id) ON DELETE CASCADE;


--
-- TOC entry 4788 (class 2606 OID 32919)
-- Name: profesor_materias profesor_materias_profesor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.profesor_materias
    ADD CONSTRAINT profesor_materias_profesor_id_fkey FOREIGN KEY (profesor_id) REFERENCES public.usuarios(id) ON DELETE CASCADE;


-- Completed on 2026-06-08 23:01:01

--
-- PostgreSQL database dump complete
--

\unrestrict fjPsyTVPGWnlY8TzQ15xXGEvIkx5D0OMxdGccVs75bKZcmbiEaiPc1w8L1QpyaG

