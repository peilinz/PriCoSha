-- Creating tables 

CREATE TABLE IF NOT EXISTS Person(
	email VARCHAR(50),
	password CHAR(64),
	first_name VARCHAR(50),
	last_name VARCHAR(50),
	PRIMARY KEY(email)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS FriendGroup(
	fg_name VARCHAR(50),
	description VARCHAR(50),
	email VARCHAR(50),
	PRIMARY KEY (fg_name, email),
	FOREIGN KEY (email) REFERENCES Person(email)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS ContentItem(
	item_id INT AUTO_INCREMENT,
	email VARCHAR(50),
	post_time TIMESTAMP,
	file_path VARCHAR(50),
	item_name VARCHAR(50),
	is_pub BOOLEAN,
	PRIMARY KEY(item_id),
	FOREIGN KEY(email) REFERENCES Person(email)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE IF NOT EXISTS Tag(
	tagger VARCHAR(50),
	tagged VARCHAR(50),
	item_id INT AUTO_INCREMENT,
	status VARCHAR(50),
	tag_time TIMESTAMP,
	PRIMARY KEY(tagger, tagged, item_id),
	FOREIGN KEY(tagger) REFERENCES Person(email),
	FOREIGN KEY(tagged) REFERENCES Person(email),
	FOREIGN KEY(item_id) REFERENCES ContentItem(item_id)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS Belong(
	member_email VARCHAR(50),
	fg_name VARCHAR(50),
	creator_email VARCHAR(50),
	PRIMARY KEY (member_email, fg_name, creator_email),
	FOREIGN KEY (member_email) REFERENCES Person(email),
	FOREIGN KEY (fg_name, creator_email) REFERENCES FriendGroup(fg_name, email) 
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS Share(
	fg_name VARCHAR(50),
	item_id INT AUTO_INCREMENT,
	email VARCHAR(50),
	PRIMARY KEY (fg_name, item_id, email),
	FOREIGN KEY (fg_name) REFERENCES FriendGroup(fg_name),
	FOREIGN KEY (email,fg_name) REFERENCES Belong(member_email,fg_name),
	FOREIGN KEY (item_id) REFERENCES ContentItem(item_id)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS Comment(
	email VARCHAR(50),
	item_id INT AUTO_INCREMENT,
	time_posted TIMESTAMP,
	description VARCHAR(1000),
	PRIMARY KEY(email, item_id, time_posted),
	FOREIGN KEY(email) REFERENCES Person(email),
	FOREIGN KEY(item_id) REFERENCES ContentItem(item_id)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;


/*CREATE TABLE IF NOT EXISTS Own(
	email VARCHAR(50),
	fg_name VARCHAR(50),
	PRIMARY KEY (email, fg_name),
	FOREIGN KEY (fg_name, email) REFERENCES FriendGroup(fg_name, email)
);

CREATE TABLE IF NOT EXISTS Posted(
	email VARCHAR(50),
	item_id INT AUTO_INCREMENT,
	PRIMARY KEY (email, item_id),
	FOREIGN KEY (item_id, email) REFERENCES ContentItem(item_id, email
);*/
