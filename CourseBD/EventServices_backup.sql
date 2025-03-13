--
-- PostgreSQL database dump
--

-- Dumped from database version 17.2
-- Dumped by pg_dump version 17.2

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

ALTER TABLE ONLY public.users DROP CONSTRAINT users_role_id_fkey;
ALTER TABLE ONLY public.events DROP CONSTRAINT events_venue_id_fkey;
ALTER TABLE ONLY public.events_sponsors DROP CONSTRAINT events_sponsors_sponsor_id_fkey;
ALTER TABLE ONLY public.events_sponsors DROP CONSTRAINT events_sponsors_event_id_fkey;
ALTER TABLE ONLY public.events DROP CONSTRAINT events_category_id_fkey;
ALTER TABLE ONLY public.bookings DROP CONSTRAINT bookings_user_id_fkey;
ALTER TABLE ONLY public.bookings DROP CONSTRAINT bookings_event_id_fkey;
DROP TRIGGER trigger_audit_changes ON public.bookings;
CREATE OR REPLACE VIEW public.events_view AS
SELECT
    NULL::integer AS id,
    NULL::text AS event_title,
    NULL::text AS event_description,
    NULL::timestamp without time zone AS event_date,
    NULL::text AS venue_name,
    NULL::text AS category_name,
    NULL::text[] AS sponsors;
DROP INDEX public.ix_revoked_tokens_token;
DROP INDEX public.ix_revoked_tokens_id;
ALTER TABLE ONLY public.venues DROP CONSTRAINT venues_pkey;
ALTER TABLE ONLY public.users DROP CONSTRAINT users_username_key;
ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
ALTER TABLE ONLY public.roles DROP CONSTRAINT roles_pkey;
ALTER TABLE ONLY public.roles DROP CONSTRAINT roles_name_key;
ALTER TABLE ONLY public.revoked_tokens DROP CONSTRAINT revoked_tokens_pkey;
ALTER TABLE ONLY public.events DROP CONSTRAINT events_pkey;
ALTER TABLE ONLY public.sponsors DROP CONSTRAINT companies_pkey;
ALTER TABLE ONLY public.categories DROP CONSTRAINT categories_pkey;
ALTER TABLE ONLY public.categories DROP CONSTRAINT categories_name_key;
ALTER TABLE ONLY public.bookings DROP CONSTRAINT bookings_pkey;
ALTER TABLE ONLY public.audit_log DROP CONSTRAINT audit_log_pkey;
ALTER TABLE public.venues ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.users ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.sponsors ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.roles ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.revoked_tokens ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.events ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.categories ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.bookings ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.audit_log ALTER COLUMN id DROP DEFAULT;
DROP SEQUENCE public.venues_id_seq;
DROP TABLE public.venues;
DROP SEQUENCE public.users_id_seq;
DROP SEQUENCE public.roles_id_seq;
DROP TABLE public.roles;
DROP SEQUENCE public.revoked_tokens_id_seq;
DROP TABLE public.revoked_tokens;
DROP VIEW public.events_view;
DROP TABLE public.events_sponsors;
DROP SEQUENCE public.events_id_seq;
DROP SEQUENCE public.companies_id_seq;
DROP TABLE public.sponsors;
DROP SEQUENCE public.categories_id_seq;
DROP TABLE public.categories;
DROP VIEW public.bookings_view;
DROP TABLE public.users;
DROP TABLE public.events;
DROP SEQUENCE public.bookings_id_seq;
DROP TABLE public.bookings;
DROP SEQUENCE public.audit_log_id_seq;
DROP TABLE public.audit_log;
DROP FUNCTION public.log_audit_changes();
DROP PROCEDURE public.insert_venue_proc(IN p_name text, IN p_address text, IN p_capacity integer);
DROP FUNCTION public.insert_event(p_title character varying, p_description text, p_date timestamp without time zone, p_venue_name character varying, p_category_name character varying);
DROP FUNCTION public.get_venues();
DROP FUNCTION public.get_events_with_sponsors();
DROP FUNCTION public.get_event_by_id(event_id integer);
DROP FUNCTION public.get_bookings_by_username(p_username text);
DROP FUNCTION public.get_bookings();
--
-- Name: get_bookings(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.get_bookings() RETURNS TABLE(id integer, username text, title text, booking_date timestamp without time zone, payment_status integer)
    LANGUAGE plpgsql
    AS $$
BEGIN
    RETURN QUERY
    SELECT 
		bookings_view.id::integer,
        bookings_view.username::TEXT, 
        bookings_view.title::TEXT, 
        bookings_view.booking_date, 
        CASE 
            WHEN bookings_view.payment_status THEN 1 
            ELSE 0 
        END AS payment_status  
    FROM bookings_view 
	ORDER BY bookings_view.id DESC;
END;
$$;


ALTER FUNCTION public.get_bookings() OWNER TO postgres;

--
-- Name: get_bookings_by_username(text); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.get_bookings_by_username(p_username text) RETURNS TABLE(id integer, username text, title text, booking_date timestamp without time zone, payment_status integer)
    LANGUAGE plpgsql
    AS $$
BEGIN
    RETURN QUERY
    SELECT 
		b.id::integer,
        b.username::TEXT, 
        b.title::TEXT, 
        b.booking_date, 
        CASE 
            WHEN b.payment_status THEN 1 
            ELSE 0 
        END AS payment_status  
    FROM bookings_view AS b
    WHERE p_username IS NULL OR b.username = p_username
	ORDER BY b.id DESC;
END;
$$;


ALTER FUNCTION public.get_bookings_by_username(p_username text) OWNER TO postgres;

--
-- Name: get_event_by_id(integer); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.get_event_by_id(event_id integer) RETURNS TABLE(event_title text, event_description text, event_date timestamp without time zone, venue_name text, category_name text, sponsors text[])
    LANGUAGE plpgsql
    AS $$
BEGIN
    RETURN QUERY
    SELECT ev.event_title, 
        ev.event_description, 
        ev.event_date, 
        ev.venue_name, 
        ev.category_name,
        ev.sponsors
    FROM public.events_view as ev
    WHERE event_id IS NULL OR ev.id = event_id;
END;
$$;


ALTER FUNCTION public.get_event_by_id(event_id integer) OWNER TO postgres;

--
-- Name: get_events_with_sponsors(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.get_events_with_sponsors() RETURNS TABLE(id integer, event_title text, event_description text, event_date timestamp without time zone, venue_name text, category_name text, sponsors text[])
    LANGUAGE plpgsql
    AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM public.events_view;
END;
$$;


ALTER FUNCTION public.get_events_with_sponsors() OWNER TO postgres;

--
-- Name: get_venues(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.get_venues() RETURNS TABLE(id integer, name text, address text, capacity integer)
    LANGUAGE plpgsql
    AS $$
BEGIN
    RETURN QUERY 
    SELECT t.id, 
           t.name::TEXT,  -- Приводим VARCHAR к TEXT
           t.address::TEXT, -- Приводим VARCHAR к TEXT
           t.capacity
    FROM venues t;
END;
$$;


ALTER FUNCTION public.get_venues() OWNER TO postgres;

--
-- Name: insert_event(character varying, text, timestamp without time zone, character varying, character varying); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.insert_event(p_title character varying, p_description text, p_date timestamp without time zone, p_venue_name character varying, p_category_name character varying) RETURNS void
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_venue_id INT;
    v_category_id INT;
BEGIN
    -- Проверяем, существует ли площадка с указанным именем
    SELECT id INTO v_venue_id FROM venues WHERE name = p_venue_name;
    IF v_venue_id IS NULL THEN
        RAISE EXCEPTION 'Venue with name "%" not found', p_venue_name;
    END IF;

    -- Проверяем, существует ли категория с указанным именем
    SELECT id INTO v_category_id FROM categories WHERE name = p_category_name;
    IF v_category_id IS NULL THEN
        RAISE EXCEPTION 'Category with name "%" not found', p_category_name;
    END IF;

    -- Вставляем новое мероприятие
    INSERT INTO events (title, description, date, venue_id, category_id)
    VALUES (p_title, p_description, p_date, v_venue_id, v_category_id);
    
    RAISE NOTICE 'Event "%" successfully inserted', p_title;
END;
$$;


ALTER FUNCTION public.insert_event(p_title character varying, p_description text, p_date timestamp without time zone, p_venue_name character varying, p_category_name character varying) OWNER TO postgres;

--
-- Name: insert_venue_proc(text, text, integer); Type: PROCEDURE; Schema: public; Owner: postgres
--

CREATE PROCEDURE public.insert_venue_proc(IN p_name text, IN p_address text, IN p_capacity integer)
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO venues (name, address, capacity) 
    VALUES (p_name, p_address, p_capacity);
END;
$$;


ALTER PROCEDURE public.insert_venue_proc(IN p_name text, IN p_address text, IN p_capacity integer) OWNER TO postgres;

--
-- Name: log_audit_changes(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.log_audit_changes() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    -- Логирование INSERT
    IF (TG_OP = 'INSERT') THEN
        INSERT INTO audit_log (action_type, table_name, record_id, new_data)
        VALUES ('INSERT', TG_TABLE_NAME, NEW.id, to_jsonb(NEW));
        RETURN NEW;
    END IF;
    
    -- Логирование DELETE
    IF (TG_OP = 'DELETE') THEN
        INSERT INTO audit_log (action_type, table_name, record_id, old_data)
        VALUES ('DELETE', TG_TABLE_NAME, OLD.id, to_jsonb(OLD));
        RETURN OLD;
    END IF;
    
    RETURN NULL;
END;
$$;


ALTER FUNCTION public.log_audit_changes() OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: audit_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.audit_log (
    id integer NOT NULL,
    action_type character varying(50),
    table_name character varying(100),
    record_id integer,
    old_data jsonb,
    new_data jsonb,
    action_time timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.audit_log OWNER TO postgres;

--
-- Name: audit_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.audit_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.audit_log_id_seq OWNER TO postgres;

--
-- Name: audit_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.audit_log_id_seq OWNED BY public.audit_log.id;


--
-- Name: bookings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.bookings (
    id integer NOT NULL,
    user_id integer NOT NULL,
    event_id integer NOT NULL,
    booking_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    payment_status boolean NOT NULL
);


ALTER TABLE public.bookings OWNER TO postgres;

--
-- Name: bookings_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.bookings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.bookings_id_seq OWNER TO postgres;

--
-- Name: bookings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.bookings_id_seq OWNED BY public.bookings.id;


--
-- Name: events; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.events (
    id integer NOT NULL,
    title character varying(100) NOT NULL,
    description text,
    date timestamp without time zone NOT NULL,
    venue_id integer NOT NULL,
    category_id integer NOT NULL
);


ALTER TABLE public.events OWNER TO postgres;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(50) NOT NULL,
    password_hash character varying(255) NOT NULL,
    role_id integer NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: bookings_view; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.bookings_view AS
 SELECT b.id,
    u.username,
    e.title,
    b.booking_date,
    b.payment_status
   FROM ((public.bookings b
     JOIN public.users u ON ((b.user_id = u.id)))
     JOIN public.events e ON ((b.event_id = e.id)));


ALTER VIEW public.bookings_view OWNER TO postgres;

--
-- Name: categories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.categories (
    id integer NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE public.categories OWNER TO postgres;

--
-- Name: categories_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.categories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.categories_id_seq OWNER TO postgres;

--
-- Name: categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.categories_id_seq OWNED BY public.categories.id;


--
-- Name: sponsors; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sponsors (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    description text,
    contact_email character varying(100),
    contact_phone character varying(20)
);


ALTER TABLE public.sponsors OWNER TO postgres;

--
-- Name: companies_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.companies_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.companies_id_seq OWNER TO postgres;

--
-- Name: companies_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.companies_id_seq OWNED BY public.sponsors.id;


--
-- Name: events_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.events_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.events_id_seq OWNER TO postgres;

--
-- Name: events_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.events_id_seq OWNED BY public.events.id;


--
-- Name: events_sponsors; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.events_sponsors (
    event_id integer,
    sponsor_id integer
);


ALTER TABLE public.events_sponsors OWNER TO postgres;

--
-- Name: events_view; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.events_view AS
SELECT
    NULL::integer AS id,
    NULL::text AS event_title,
    NULL::text AS event_description,
    NULL::timestamp without time zone AS event_date,
    NULL::text AS venue_name,
    NULL::text AS category_name,
    NULL::text[] AS sponsors;


ALTER VIEW public.events_view OWNER TO postgres;

--
-- Name: revoked_tokens; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.revoked_tokens (
    id integer NOT NULL,
    token character varying,
    revoked_at timestamp without time zone
);


ALTER TABLE public.revoked_tokens OWNER TO postgres;

--
-- Name: revoked_tokens_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.revoked_tokens_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.revoked_tokens_id_seq OWNER TO postgres;

--
-- Name: revoked_tokens_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.revoked_tokens_id_seq OWNED BY public.revoked_tokens.id;


--
-- Name: roles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.roles (
    id integer NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE public.roles OWNER TO postgres;

--
-- Name: roles_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.roles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.roles_id_seq OWNER TO postgres;

--
-- Name: roles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.roles_id_seq OWNED BY public.roles.id;


--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: venues; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.venues (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    address character varying(255) NOT NULL,
    capacity integer NOT NULL,
    CONSTRAINT venues_capacity_check CHECK ((capacity > 0))
);


ALTER TABLE public.venues OWNER TO postgres;

--
-- Name: venues_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.venues_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.venues_id_seq OWNER TO postgres;

--
-- Name: venues_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.venues_id_seq OWNED BY public.venues.id;


--
-- Name: audit_log id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.audit_log ALTER COLUMN id SET DEFAULT nextval('public.audit_log_id_seq'::regclass);


--
-- Name: bookings id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bookings ALTER COLUMN id SET DEFAULT nextval('public.bookings_id_seq'::regclass);


--
-- Name: categories id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories ALTER COLUMN id SET DEFAULT nextval('public.categories_id_seq'::regclass);


--
-- Name: events id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events ALTER COLUMN id SET DEFAULT nextval('public.events_id_seq'::regclass);


--
-- Name: revoked_tokens id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.revoked_tokens ALTER COLUMN id SET DEFAULT nextval('public.revoked_tokens_id_seq'::regclass);


--
-- Name: roles id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles ALTER COLUMN id SET DEFAULT nextval('public.roles_id_seq'::regclass);


--
-- Name: sponsors id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sponsors ALTER COLUMN id SET DEFAULT nextval('public.companies_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: venues id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.venues ALTER COLUMN id SET DEFAULT nextval('public.venues_id_seq'::regclass);


--
-- Data for Name: audit_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.audit_log (id, action_type, table_name, record_id, old_data, new_data, action_time) FROM stdin;
55	DELETE	bookings	59	{"id": 59, "user_id": 28, "event_id": 10, "booking_date": "2025-03-09T11:18:27.049", "payment_status": false}	\N	2025-03-10 22:47:04.074171
56	DELETE	bookings	60	{"id": 60, "user_id": 41, "event_id": 10, "booking_date": "2025-03-09T11:55:38.395", "payment_status": false}	\N	2025-03-10 22:47:04.074171
57	INSERT	bookings	61	\N	{"id": 61, "user_id": 41, "event_id": 13, "booking_date": "2025-03-10T20:36:46.651", "payment_status": false}	2025-03-10 23:36:46.656845
58	INSERT	bookings	62	\N	{"id": 62, "user_id": 28, "event_id": 13, "booking_date": "2025-03-13T08:08:11.517", "payment_status": false}	2025-03-13 11:08:11.523476
59	INSERT	bookings	63	\N	{"id": 63, "user_id": 42, "event_id": 13, "booking_date": "2025-03-13T09:25:20.008", "payment_status": false}	2025-03-13 12:25:20.013958
60	INSERT	bookings	64	\N	{"id": 64, "user_id": 42, "event_id": 14, "booking_date": "2025-03-13T09:26:02.846", "payment_status": false}	2025-03-13 12:26:02.849992
61	DELETE	bookings	64	{"id": 64, "user_id": 42, "event_id": 14, "booking_date": "2025-03-13T09:26:02.846", "payment_status": true}	\N	2025-03-13 12:26:45.250521
62	INSERT	bookings	65	\N	{"id": 65, "user_id": 43, "event_id": 14, "booking_date": "2025-03-13T10:11:00.261", "payment_status": false}	2025-03-13 13:11:00.267046
63	INSERT	bookings	66	\N	{"id": 66, "user_id": 43, "event_id": 16, "booking_date": "2025-03-13T10:11:04.568", "payment_status": false}	2025-03-13 13:11:04.571893
64	INSERT	bookings	67	\N	{"id": 67, "user_id": 43, "event_id": 17, "booking_date": "2025-03-13T10:11:08.407", "payment_status": false}	2025-03-13 13:11:08.411574
65	DELETE	bookings	61	{"id": 61, "user_id": 41, "event_id": 13, "booking_date": "2025-03-10T20:36:46.651", "payment_status": true}	\N	2025-03-13 13:13:22.346785
66	INSERT	bookings	68	\N	{"id": 68, "user_id": 28, "event_id": 17, "booking_date": "2025-03-13T11:47:29.746", "payment_status": false}	2025-03-13 14:47:29.75257
67	INSERT	bookings	69	\N	{"id": 69, "user_id": 28, "event_id": 16, "booking_date": "2025-03-13T11:47:32.372", "payment_status": false}	2025-03-13 14:47:32.376687
\.


--
-- Data for Name: bookings; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.bookings (id, user_id, event_id, booking_date, payment_status) FROM stdin;
62	28	13	2025-03-13 08:08:11.517	t
65	43	14	2025-03-13 10:11:00.261	f
66	43	16	2025-03-13 10:11:04.568	t
67	43	17	2025-03-13 10:11:08.407	t
68	28	17	2025-03-13 11:47:29.746	f
69	28	16	2025-03-13 11:47:32.372	f
63	42	13	2025-03-13 09:25:20.008	t
\.


--
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.categories (id, name) FROM stdin;
1	Концерт
2	Фестиваль
3	Театр
\.


--
-- Data for Name: events; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.events (id, title, description, date, venue_id, category_id) FROM stdin;
13	Концерт классической музыки	Замечательный концерт классической музыки с множеством разных исполнителей 	2025-05-22 18:30:00	19	1
14	Рок фестиваль 	Масштабный рок фестиваль экспериментальной музыки 	2025-06-12 23:45:00	20	2
15	Ежегодный фестиваль джаза	Ежегодный фестиваль джаза с множеством исполнителей под открытым небом в парке	2025-07-30 19:30:00	21	2
16	Постановка Король Лир	Постановка Шекспира под открытым небом в ВДНХ	2025-07-31 18:00:00	22	3
17	Выступление народной музыки 	Выступление коллектива русской народной музыки 	2025-03-28 14:30:00	23	1
\.


--
-- Data for Name: events_sponsors; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.events_sponsors (event_id, sponsor_id) FROM stdin;
\.


--
-- Data for Name: revoked_tokens; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.revoked_tokens (id, token, revoked_at) FROM stdin;
1	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IjIyMjIiLCJleHAiOjE3NDExNzcwMjN9.Q62s20m_tZ9pSfWqsgp-P2XR32nutcJ8vSnAessJXsw	2025-03-05 11:47:34.900039
\.


--
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.roles (id, name) FROM stdin;
1	admin
2	user
\.


--
-- Data for Name: sponsors; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sponsors (id, name, description, contact_email, contact_phone) FROM stdin;
1	Company A	Tech sponsor	contact@companya.com	123-456-7890
2	Company B	Music equipment provider	contact@companyb.com	098-765-4321
3	Company A	Tech sponsor	contact@companya.com	123-456-7890
4	Company B	Music equipment provider	contact@companyb.com	098-765-4321
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, username, password_hash, role_id) FROM stdin;
9	admin	admin	1
28	1234	03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4	1
42	xengu	8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92	2
43	username	16f78a7d6317f102bbd95fc9a4f3ff2e3249287690b8bdad6b7810f82b34ace3	2
\.


--
-- Data for Name: venues; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.venues (id, name, address, capacity) FROM stdin;
19	Дворец культуры Выхино	г. Москва, ул. Рязанская, дом 8	500
20	Стадион Лужники	г. Москва, ул. Косыгина, дом 4	3000
21	Парк Царицыно	г. Москва, Дольская ул., 1	5000
22	Зеленый театр ВДНХ	г. Москва, ул. Иванова, дом 3	2000
23	Новая третьяковка	г. Москва ул. Крымский Вал, 10	1000
\.


--
-- Name: audit_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.audit_log_id_seq', 67, true);


--
-- Name: bookings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.bookings_id_seq', 69, true);


--
-- Name: categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.categories_id_seq', 3, true);


--
-- Name: companies_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.companies_id_seq', 4, true);


--
-- Name: events_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.events_id_seq', 17, true);


--
-- Name: revoked_tokens_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.revoked_tokens_id_seq', 1, true);


--
-- Name: roles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.roles_id_seq', 2, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 43, true);


--
-- Name: venues_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.venues_id_seq', 24, true);


--
-- Name: audit_log audit_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.audit_log
    ADD CONSTRAINT audit_log_pkey PRIMARY KEY (id);


--
-- Name: bookings bookings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bookings
    ADD CONSTRAINT bookings_pkey PRIMARY KEY (id);


--
-- Name: categories categories_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_name_key UNIQUE (name);


--
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (id);


--
-- Name: sponsors companies_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sponsors
    ADD CONSTRAINT companies_pkey PRIMARY KEY (id);


--
-- Name: events events_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_pkey PRIMARY KEY (id);


--
-- Name: revoked_tokens revoked_tokens_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.revoked_tokens
    ADD CONSTRAINT revoked_tokens_pkey PRIMARY KEY (id);


--
-- Name: roles roles_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_name_key UNIQUE (name);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: venues venues_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.venues
    ADD CONSTRAINT venues_pkey PRIMARY KEY (id);


--
-- Name: ix_revoked_tokens_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_revoked_tokens_id ON public.revoked_tokens USING btree (id);


--
-- Name: ix_revoked_tokens_token; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_revoked_tokens_token ON public.revoked_tokens USING btree (token);


--
-- Name: events_view _RETURN; Type: RULE; Schema: public; Owner: postgres
--

CREATE OR REPLACE VIEW public.events_view AS
 SELECT e.id,
    (e.title)::text AS event_title,
    e.description AS event_description,
    e.date AS event_date,
    (v.name)::text AS venue_name,
    (c.name)::text AS category_name,
    COALESCE(array_agg((s.name)::text) FILTER (WHERE (s.id IS NOT NULL)), '{}'::text[]) AS sponsors
   FROM ((((public.events e
     LEFT JOIN public.venues v ON ((e.venue_id = v.id)))
     LEFT JOIN public.categories c ON ((e.category_id = c.id)))
     LEFT JOIN public.events_sponsors es ON ((e.id = es.event_id)))
     LEFT JOIN public.sponsors s ON ((es.sponsor_id = s.id)))
  GROUP BY e.id, v.name, c.name;


--
-- Name: bookings trigger_audit_changes; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_audit_changes AFTER INSERT OR DELETE ON public.bookings FOR EACH ROW EXECUTE FUNCTION public.log_audit_changes();


--
-- Name: bookings bookings_event_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bookings
    ADD CONSTRAINT bookings_event_id_fkey FOREIGN KEY (event_id) REFERENCES public.events(id);


--
-- Name: bookings bookings_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bookings
    ADD CONSTRAINT bookings_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: events events_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(id);


--
-- Name: events_sponsors events_sponsors_event_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events_sponsors
    ADD CONSTRAINT events_sponsors_event_id_fkey FOREIGN KEY (event_id) REFERENCES public.events(id);


--
-- Name: events_sponsors events_sponsors_sponsor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events_sponsors
    ADD CONSTRAINT events_sponsors_sponsor_id_fkey FOREIGN KEY (sponsor_id) REFERENCES public.sponsors(id);


--
-- Name: events events_venue_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_venue_id_fkey FOREIGN KEY (venue_id) REFERENCES public.venues(id);


--
-- Name: users users_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id);


--
-- PostgreSQL database dump complete
--

