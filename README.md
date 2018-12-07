# PriCoSha
Fall 2018 Database Project 

Pricosha:
1) People can login or register from the homepage.
2) Register asks for email, password, first name, last name and checks if the person is already registered, if not, adds them to the Person table.
3) Login checks if the email and password match with on the database and goes to home if it does, raises an error if not.
4) The home page has the individuals public feed and private feed from friend groups, reverse chronically sorted.
    The home page also has various buttons to other features: delete friend, add friend, manage tags, view friend group, post privately, post publicly, and logout. 
5) Post publicly asks for item name, url(optional) and inserts it into the ContentItem table with a public value of true.
6) Post privately asks for item name, url(optional) and inserts it into the ContentItem table with a private value of false. It also asks for friend groups in which the user wants to add the item to. Adds that to the Share table.
7) View friend group shows all of the user’s friend groups that they are in.
8) Manage tags shows the user all of their tags that are pending action. The user can choose to accept a tag, decline a tag, or create a tag. 
    Accept a tag and decline a tag asks to select a item id, and user must choose the one they want to accept. 
    Create a tag asks for the tagged person’s email and to select the item id they want to tag. 
9) Add a friend asks for the friend group with which the user wants to add the friend, the friend’s first name, last name and email. It is added to the Belong table. 
    Also checks if friend is already in the group or not. 
10) Logout returns to the homepage.

Extra Features:
1) Defriend: Kevin Chen
    This feature allows the owner of the friend group to remove people. 
    Also removes all content items that the person shared to the friend group. 
    Also removes all tags the person made to content items share to the friend group. 
    Checks if the email provided is a valid email, meaning the person is in the friend group or even exists.
    Makes sure the person removing is actually the owner of the friend group.
    
2)Add comments: Peilin Zhen
    This feature allows users to comment on the content items that are visible to them by clicking on the item id of each item. A new page will display all the comments have been posted for that content as well as allow the user to comment.
    It is a good feature because it allows the user to express their opinions about a particular content
    We basically used Rate as the Comment database. There are four attributes in the Comment databases: email, item_id, post_time, description, where description is the same as comment on the post. The primary keys are email, item_id, and post_time so that a user can comment more than once.

Kevin - Primarily worked on Flask, some HTML
Peilin - Primarily worked on HTML, some Flask
