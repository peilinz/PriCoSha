-- Write a query to show the ID and name of each content item that is shared with David

SELECT DISTINCT item_id, item_name FROM ContentItem 
	WHERE is_pub = 1 OR 
		item_id IN (SELECT item_id FROM Share JOIN Belong ON email = creator_email AND share.fg_name = belong.fg_name WHERE member_email = 'dd@nyu.edu') OR 
		item_id IN (SELECT item_id FROM Tag WHERE tagger = 'dd@nyu.edu' OR tagged = 'dd@nyu.edu')