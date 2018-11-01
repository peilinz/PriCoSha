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

INSERT INTO FriendGroup(fg_name, description, owner_email) VALUES
('family', 'Anns Family', 'AA@nyu.edu'),
('roommates', 'Anns Roommates', 'AA@nyu.edu'),
('family', 'Bobs Family', 'BB@nyu.edu');

INSERT INTO Own(email, fg_name) VALUES
('AA@nyu.edu', 'family'),
('AA@nyu.edu', 'roommates'),
('BB@nyu.edu', 'family');

INSERT INTO Belong(email, fg_name) VALUES
('AA@nyu.edu', 'roommates'),
('GG@nyu.edu', 'roommates'),
('HH@nyu.edu', 'roommates');

('AA@nyu.edu', 'family', 'AA@nyu.edu'),
('CC@nyu.edu', 'family', 'AA@nyu.edu'),
('DD@nyu.edu', 'family', 'AA@nyu.edu'),
('EE@nyu.edu', 'family', 'AA@nyu.edu'),

('BB@nyu.edu', 'family', 'BB@nyu.edu'),
('FF@nyu.edu', 'family', 'AA@nyu.edu'),
('EE@nyu.edu', 'family', 'AA@nyu.edu');


INSERT INTO ContentItem(item_id,post_time item_name, is_pub) VALUES
(1, CURRENT_TIMESTAMP, 'Whiskers', False),
(2, CURRENT_TIMESTAMP, 'leftovers in fridge', False);

INSERT INTO Post(
  
  
  
  
  
  
  
  
  
