-- Person

CREATE TABLE Person(
	email VARCHAR(50),
	password CHAR(32),
	first_name VARCHAR(50),
	last_name VARCHAR(50),
	PRIMARY KEY(email)
);

CREATE TABLE ContentItem(
	item_id VARCHAR(50),
	post_time DATETIME,
	file_path VARCHAR(50),
	item_name VARCHAR(50),
	PRIMARY KEY(item_id)
);


CREATE TABLE Tag(
	tagger VARCHAR(50),
	tagged VARCHAR(50),
	item_id VARCHAR(50),
	status VARCHAR(50),
	tag_time DATETIME,
	PRIMARY KEY(tagger, tagged, item_id),
	FOREIGN KEY(tagger) REFERENCES Person(email),
	FOREIGN KEY(tagged) REFERENCES Person(email),
	FOREIGN KEY(item_id) REFERENCES ContentItem(item_id)
);

CREATE TABLE Rate(
	email VARCHAR(50),
	item_id VARCHAR(50),
	rate_time DATETIME,
	emoji VARCHAR(50),
	FOREIGN KEY(email) REFERENCES Person(email),
	FOREIGN KEY(item_id) REFERENCES ContentItem(item_id)
);