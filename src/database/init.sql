DROP SCHEMA public;

CREATE SCHEMA public AUTHORIZATION pg_database_owner;
-- public."User" определение

-- Drop table

-- DROP TABLE public."User";

CREATE TABLE public."User" (
	user_id int8 GENERATED ALWAYS AS IDENTITY NOT NULL,
	is_admin bool NOT NULL,
	tg_id int8 NOT NULL,
	CONSTRAINT users_pk PRIMARY KEY (user_id)
);


-- public."Place" определение

-- Drop table

-- DROP TABLE public."Place";

CREATE TABLE public."Place" (
	place_id int8 GENERATED ALWAYS AS IDENTITY NOT NULL,
	category varchar NOT NULL,
	city varchar NOT NULL,
	"name" varchar NOT NULL,
	CONSTRAINT place_pk PRIMARY KEY (place_id)
);


-- public."Rate" определение

-- Drop table

-- DROP TABLE public."Rate";

CREATE TABLE public."Rate" (
	rate_id int8 GENERATED ALWAYS AS IDENTITY NOT NULL,
	user_id int8 NOT NULL,
	place_id int8 NOT NULL,
	rate int4 NOT NULL,
	CONSTRAINT rate PRIMARY KEY (rate_id),
	CONSTRAINT rate_place_fk FOREIGN KEY (place_id) REFERENCES public."Place"(place_id) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT rate_user_fk FOREIGN KEY (user_id) REFERENCES public."User"(user_id) ON DELETE CASCADE ON UPDATE CASCADE
);


-- public."Comment" определение

-- Drop table

-- DROP TABLE public."Comment";

CREATE TABLE public."Comment" (
	comment_id int8 GENERATED ALWAYS AS IDENTITY NOT NULL,
    is_moderated bool NOT NULL, 
	user_id int8 NOT NULL,
	place_id int8 NOT NULL,
	"text" varchar NOT NULL,
	CONSTRAINT comment_pk PRIMARY KEY (comment_id),
	CONSTRAINT comment_place_fk FOREIGN KEY (place_id) REFERENCES public."Place"(place_id) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT comment_user_fk FOREIGN KEY (user_id) REFERENCES public."User"(user_id) ON DELETE CASCADE ON UPDATE CASCADE
);


-- DROP SCHEMA public;

CREATE SCHEMA public AUTHORIZATION pg_database_owner;
-- public."User" определение

-- Drop table

-- DROP TABLE public."User";

CREATE TABLE public."User" (
	user_id int8 GENERATED ALWAYS AS IDENTITY NOT NULL,
	is_admin bool NOT NULL,
	tg_id int8 NOT NULL,
	CONSTRAINT users_pk PRIMARY KEY (user_id)
);


-- public."Place" определение

-- Drop table

-- DROP TABLE public."Place";

CREATE TABLE public."Place" (
	place_id int8 GENERATED ALWAYS AS IDENTITY NOT NULL,
	category varchar NOT NULL,
	city varchar NOT NULL,
	"name" varchar NOT NULL,
	CONSTRAINT place_pk PRIMARY KEY (place_id)
);


-- public."Rate" определение

-- Drop table

-- DROP TABLE public."Rate";

CREATE TABLE public."Rate" (
	rate_id int8 GENERATED ALWAYS AS IDENTITY NOT NULL,
	user_id int8 NOT NULL,
	place_id int8 NOT NULL,
	rate int4 NOT NULL,
	CONSTRAINT rate PRIMARY KEY (rate_id),
	CONSTRAINT rate_place_fk FOREIGN KEY (place_id) REFERENCES public."Place"(place_id) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT rate_user_fk FOREIGN KEY (user_id) REFERENCES public."User"(user_id) ON DELETE CASCADE ON UPDATE CASCADE
);
