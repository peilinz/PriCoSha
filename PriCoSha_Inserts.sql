-- Insert people
INSERT INTO Person(email, password, first_name, last_name) VALUES
('AA@nyu.edu', SHA2('AA',256), 'Ann', 'Anderson'),
('BB@nyu.edu', SHA2('BB',256), 'Bob', 'Baker'),
('CC@nyu.edu', SHA2('CC',256), 'Cathy', 'Chang'),
('DD@nyu.edu', SHA2('DD',256), 'David','Davidson'),
('EE@nyu.edu', SHA2('EE',256), 'Ellen', 'Ellenberg'),
('FF@nyu.edu', SHA2('FF',256), 'Fred', 'Fox'),
('GG@nyu.edu', SHA2('GG',256), 'Gina', 'Gupta'),
('HH@nyu.edu', SHA2('HH',256), 'Helen', 'Harper');

INSERT INTO FriendGroup(fg_name, description, owner_email) VALUES
('family', 'Anns Family', 'AA@nyu.edu'),
('roommates', 'Anns Roommates', 'AA@nyu.edu'),
('family', 'Bobs Family', 'BB@nyu.edu');

INSERT INTO Own(owner_email, fg_name) VALUES
('AA@nyu.edu', 'family'),
('AA@nyu.edu', 'roommates'),
('BB@nyu.edu', 'family');

INSERT INTO Belong(member_email, fg_name, creator_email) VALUES
('AA@nyu.edu', 'roommates','AA@nyu.edu'),
('GG@nyu.edu', 'roommates','AA@nyu.edu'),
('HH@nyu.edu', 'roommates','AA@nyu.edu'),

('AA@nyu.edu', 'family', 'AA@nyu.edu'),
('CC@nyu.edu', 'family', 'AA@nyu.edu'),
('DD@nyu.edu', 'family', 'AA@nyu.edu'),
('EE@nyu.edu', 'family', 'AA@nyu.edu'),

('BB@nyu.edu', 'family', 'BB@nyu.edu'),
('FF@nyu.edu', 'family', 'BB@nyu.edu'),
('EE@nyu.edu', 'family', 'BB@nyu.edu');


INSERT INTO ContentItem(item_id,post_time, item_name, is_pub) VALUES
(1, CURRENT_TIMESTAMP, 'Whiskers', 0),
(2, CURRENT_TIMESTAMP, 'leftovers in fridge', 0),
(3, CURRENT_TIMESTAMP, 'Rover', 0);

INSERT INTO Posted(poster_email, item_id) VALUES
('AA@nyu.edu', 1),
('AA@nyu.edu', 2),
('BB@nyu.edu', 3);

INSERT INTO Share(fg_name, item_id,owner_email) VALUES
('family', 1,'AA@nyu.edu'),
('roommates', 2, 'AA@nyu.edu'),
('family', 3, 'BB@nyu.edu');
  
  
  
  
  
  
  
  