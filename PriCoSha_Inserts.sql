-- Insert people
INSERT INTO Person(email, password, first_name, last_name) VALUES
('AA@nyu.edu', sha256('AA'), 'Ann', 'Anderson'),
('BB@nyu.edu', sha256('BB'), 'Bob', 'Baker'),
('CC@nyu.edu', sha256('CC'), 'Cathy', 'Chang'),
('DD@nyu.edu', sha256('DD'), 'David','Davidson'),
('EE@nyu.edu', sha256('EE'), 'Ellen', 'Ellenberg'),
('FF@nyu.edu', sha256('FF'), 'Fred', 'Fox'),
('GG@nyu.edu', sha256('GG'), 'Gina', 'Gupta'),
('HH@nyu.edu', sha256('HH'), 'Helen', 'Harper');

INSERT INTO FriendGroup(fg_name, description, email) VALUES
('family', 'Ann's Family', 'AA@nyu.edu'),
('roommates', 'Ann's Roommates', 'AA@nyu.edu'),
('family', 'Bob's Family', 'BB@nyu.edu');

INSERT INTO Own(email, fg_name) VALUES
('AA@nyu.edu', 'family'),
('AA@nyu.edu', 'roommates'),
('BB@nyu.edu', 'family');

INSERT INTO Belong(email, fg_name) VALUES
('AA@nyu.edu', 'roommates'),
('GG@nyu.edu', 'roommates'),
('HH@nyu.edu', 'roommates');

