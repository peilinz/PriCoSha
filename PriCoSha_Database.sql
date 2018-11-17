-- Creating tables 

CREATE TABLE IF NOT EXISTS Person(
	email VARCHAR(50),
	password CHAR(64),
	first_name VARCHAR(50),
	last_name VARCHAR(50),
	PRIMARY KEY(email)
);

CREATE TABLE IF NOT EXISTS FriendGroup(
	fg_name VARCHAR(50),
	description VARCHAR(50),
	owner_email VARCHAR(50),
	PRIMARY KEY (fg_name, owner_email),
	FOREIGN KEY (owner_email) REFERENCES Person(email)
);

CREATE TABLE IF NOT EXISTS ContentItem(
	item_id INT AUTO_INCREMENT,
	email_post VARCHAR(50),
	post_time TIMESTAMP,
	file_path VARCHAR(50),
	item_name VARCHAR(50),
	is_pub BOOLEAN,
	PRIMARY KEY(item_id),
	FOREIGN KEY(email_post) REFERENCES Person(email_post)
);


CREATE TABLE IF NOT EXISTS Tag(
	tagger VARCHAR(50),
	tagged VARCHAR(50),
	item_id INT,
	status VARCHAR(50),
	tag_time TIMESTAMP,
	PRIMARY KEY(tagger, tagged, item_id),
	FOREIGN KEY(tagger) REFERENCES Person(email),
	FOREIGN KEY(tagged) REFERENCES Person(email),
	FOREIGN KEY(item_id) REFERENCES ContentItem(item_id)
);

CREATE TABLE IF NOT EXISTS Rate(
	rater_email VARCHAR(50),
	item_id INT,
	rate_time TIMESTAMP,
	emoji VARCHAR(50) CHARACTER SET utf8mb4,
	PRIMARY KEY(rater_email, item_id),
	FOREIGN KEY(rater_email) REFERENCES Person(email),
	FOREIGN KEY(item_id) REFERENCES ContentItem(item_id)
);


CREATE TABLE IF NOT EXISTS Own(
	owner_email VARCHAR(50),
	fg_name VARCHAR(50),
	PRIMARY KEY (owner_email, fg_name),
	FOREIGN KEY (fg_name, owner_email) REFERENCES FriendGroup(fg_name, owner_email)
);

CREATE TABLE IF NOT EXISTS Belong(
	member_email VARCHAR(50),
	fg_name VARCHAR(50),
	creator_email VARCHAR(50),
	PRIMARY KEY (member_email, fg_name, creator_email),
	FOREIGN KEY (member_email) REFERENCES Person(email),
	FOREIGN KEY (fg_name,creator_email) REFERENCES FriendGroup(fg_name, creator_email) 
);

CREATE TABLE IF NOT EXISTS Posted(
	poster_email VARCHAR(50),
	item_id INT AUTO_INCREMENT,
	PRIMARY KEY (poster_email, item_id),
	FOREIGN KEY (poster_email) REFERENCES Person(email),
	FOREIGN KEY (item_id) REFERENCES ContentItem(item_id)
);

CREATE TABLE IF NOT EXISTS Share(
	fg_name VARCHAR(50),
	item_id INT,
	owner_email VARCHAR(50),
	PRIMARY KEY (fg_name, item_id, owner_email),
	FOREIGN KEY (fg_name, owner_email) REFERENCES FriendGroup(fg_name, owner_email),
	FOREIGN KEY (item_id) REFERENCES ContentItem(item_id)
);


