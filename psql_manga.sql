drop table if exists pages;
drop table if exists chapters;
drop table if exists category_r;
drop table if exists series;
drop table if exists sources;
drop table if exists categories;

create table categories (
	id serial primary key not null,
	title character varying(80) not null);
	
create table sources (
	id serial primary key not null,
	title character varying(50) not null,
	base_url character varying(50),
	images_url character varying(50),
	comics_url character varying(50));
	
create table series (
	id serial primary key not null,
	manga_id character varying(50) not null UNIQUE,
	title character varying(150) not null,
	alias character varying(150) not null UNIQUE,
	image_url character varying(80),
	source_site integer not null,
	description text,
	foreign key(source_site) references sources(id)
		on delete cascade on update cascade);

create table category_r (
	series_id integer not null,
	category_id integer not null,
	primary key(series_id, category_id),
	foreign key(series_id) references series(id)
		on delete cascade on update cascade,
	foreign key(category_id) references categories(id)
		on delete cascade on update cascade);

create table chapters (
	id serial primary key not null,
	chap_id character varying(50) not null UNIQUE,
	chap_num integer not null,
	chap_title character varying(200),
	series_id integer not null,
	foreign key(series_id) references series(id)
		on delete cascade on update cascade);

create table pages (
	chap_id integer not null,
	page_num integer not null,
	page_url character varying(80) not null UNIQUE,
	primary key(chap_id, page_num),
	foreign key(chap_id) references chapters(id)
		on delete cascade on update cascade);
