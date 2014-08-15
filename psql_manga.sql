create schema if not exists manga;

drop table if exists manga.pages;
drop table if exists manga.chapters;
drop table if exists manga.ser_cat_r;
drop table if exists manga.series;
drop table if exists manga.sources;
drop table if exists manga.categories;

create table manga.categories (
	id serial primary key not null,
	title character varying(80) not null);
	
create table manga.sources (
	id serial primary key not null,
	title character varying(50) not null,
	base_url character varying(50),
	images_url character varying(50),
	comics_url character varying(50));
	
create table manga.series (
	id serial primary key not null,
	manga_id character varying(50) not null UNIQUE,
	title character varying(150) not null,
	alias character varying(150) not null UNIQUE,
	image_url character varying(80),
	source_site integer not null,
	description text,
	foreign key(source_site) references manga.sources(id)
		on delete cascade on update cascade);

create table manga.ser_cat_r (
	series_id integer not null,
	category_id integer not null,
	primary key(series_id, category_id),
	foreign key(series_id) references manga.series(id)
		on delete cascade on update cascade,
	foreign key(category_id) references manga.categories(id)
		on delete cascade on update cascade);

create table manga.chapters (
	id serial primary key not null,
	chap_id character varying(50) not null UNIQUE,
	chap_num integer not null,
	chap_title character varying(200),
	series_id integer not null,
	foreign key(series_id) references manga.series(id)
		on delete cascade on update cascade);

create table manga.pages (
	chap_id integer not null,
	page_num integer not null,
	page_url character varying(80) not null UNIQUE,
	primary key(chapter_id, page_num),
	foreign key(chapter_id) references manga.chapters(id)
		on delete cascade on update cascade);