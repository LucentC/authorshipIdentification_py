-- create table author
CREATE TABLE author (
	author_id SERIAL PRIMARY KEY NOT NULL,
	author_name VARCHAR(40) NOT NULL,
	author_type VARCHAR(40)
);

-- create table document
CREATE TABLE document (
	doc_id SERIAL PRIMARY KEY NOT NULL,
	author_id INTEGER REFERENCES author(author_id) NOT NULL,
	doc_title VARCHAR(40) NOT NULL,
	year_of_pub DATE
);

-- create table paragraph
CREATE TABLE paragraph (
	para_id SERIAL PRIMARY KEY NOT NULL,
	doc_id INTEGER REFERENCES document(doc_id) NOT NULL,
	chapter_id INTEGER REFERENCES chapter(chapter_id),
	path VARCHAR(20) NOT NULL
);

CREATE TABLE feature (
	feature_id SERIAL PRIMARY KEY NOT NULL,
	feature_type VARCHAR(40), -- need to think is it really to add this entry
	feature_name VARCHAR(40),
--	is_bigram BOOLEAN,
);

CREATE TABLE fact (
	doc_id INTEGER REFERENCES document (doc_id) NOT NULL,
	para_id INTEGER REFERENCES paragraph (para_id) NOT NULL,
	feature_id INTEGER REFERENCES feature(feature_id) NOT NULL,
	feature_value DOUBLE NOT NULL,
);


--------------------------------------------------------------------
-- create table chapter
CREATE TABLE chapter (
	chapter_id SERIAL PRIMARY KEY NOT NULL,
);
-- storing the chapter no is always optional
--------------------------------------------------------------------

-- create table bigram
CREATE TABLE bigram_feature (
	feature_id INTEGER REFERENCES feature(feature_id) NOT NULL,
	first_word VARCHAR(40) NOT NULL,
	second_word VARCHAR(40) NOT NULL,
);