-- create table author
CREATE TABLE author (
    author_id SERIAL PRIMARY KEY NOT NULL,
    author_name VARCHAR(100) UNIQUE NOT NULL,
    author_type VARCHAR(40)
);

-- create table document
CREATE TABLE document (
    doc_id SERIAL PRIMARY KEY NOT NULL,
    author_id INTEGER REFERENCES author(author_id) NOT NULL,
    doc_title VARCHAR(120) NOT NULL,
    year_of_pub DATE,
    loc_class VARCHAR(300) NOT NULL,
    doc_content text
    gutenberg_url VARCHAR(100) NOT NULL,
);