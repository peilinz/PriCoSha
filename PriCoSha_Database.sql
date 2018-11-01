-- Creating tables 

CREATE TABLE IF NOT EXISTS Person(
	email VARCHAR(50),
	password CHAR(32),
	first_name VARCHAR(50),
	last_name VARCHAR(50),
	PRIMARY KEY(email)
);

CREATE TABLE IF NOT EXISTS FriendGroup(
	fg_name VARCHAR(50),
	description VARCHAR(50),
	email VARCHAR(50),
	PRIMARY KEY (fg_name, email),
	FOREIGN KEY (email) REFERENCES Person(email)
);

CREATE TABLE IF NOT EXISTS ContentItem(
	item_id INT,
	post_time DATETIME,
	file_path VARCHAR(50),
	item_name VARCHAR(50),
	PRIMARY KEY(item_id)
);


CREATE TABLE IF NOT EXISTS Tag(
	tagger VARCHAR(50),
	tagged VARCHAR(50),
	item_id INT,
	status VARCHAR(50),
	tag_time DATETIME,
	PRIMARY KEY(tagger, tagged, item_id),
	FOREIGN KEY(tagger) REFERENCES Person(email),
	FOREIGN KEY(tagged) REFERENCES Person(email),
	FOREIGN KEY(item_id) REFERENCES ContentItem(item_id)
);

CREATE TABLE IF NOT EXISTS Rate(
	email VARCHAR(50),
	item_id INT,
	rate_time DATETIME,
	emoji VARCHAR(50),
	FOREIGN KEY(email) REFERENCES Person(email),
	FOREIGN KEY(item_id) REFERENCES ContentItem(item_id)
);


CREATE TABLE IF NOT EXISTS Own(
	email VARCHAR(50),
	fg_name VARCHAR(50),
	FOREIGN KEY (email) REFERENCES Person(email),
	FOREIGN KEY (fg_name) REFERENCES FriendGroup(fg_name)
);
CREATE TABLE IF NOT EXISTS Belong(
	email VARCHAR(50),
	fg_name VARCHAR(50),
	creator_email VARCHAR(50),
	PRIMARY KEY (email, fg_name, creator_email),
	FOREIGN KEY (email) REFERENCES Person(email),
	FOREIGN KEY (fg_name) REFERENCES FriendGroup(fg_name) 
);
CREATE TABLE IF NOT EXISTS Posted(
	email VARCHAR(50),
	item_id INT,
	FOREIGN KEY (email) REFERENCES Person(email),
	FOREIGN KEY (item_id) REFERENCES ContentItem(item_id)
);
CREATE TABLE IF NOT EXISTS Share(
	fg_name VARCHAR(50),
	item_id INT,
	FOREIGN KEY (fg_name) REFERENCES FriendGroup(fg_name),
	FOREIGN KEY (item_id) REFERENCES ContentItem(item_id)
);
