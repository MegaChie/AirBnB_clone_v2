Project design stages
The console project (completed - 7 days sprint)
Web static project (completed - 2 days sprint)
MySQL storage project (active - 6 days sprint)
Deploy Web Static (active - 2 days sprint)
Console CRUD operations
Below, there is a demonstration of some commands possible with the console program. Once the user initiates the command-line interface with the prompt "(hbnb)." They explore available commands using the help command, which lists options like all, create, and update. After checking all instances (resulting in an empty list), they create a new User instance with a unique ID using the create command. Subsequently, they view all instances, including the newly created User. Using the update command, the user modifies the User instance's name attribute. Another all command is then used to confirm the update. Finally, the user gracefully exits the command line with the quit command.

(hbnb) help

Documented commands (type help <topic>):
========================================
EOF  all  count  create  destroy  help  quit  show  update

(hbnb) help all
Prints all string representation of all instances based or not on the class name

Usage: all <class name> or all

data models are: BaseModel, User, State, City, Amenity, Place, Review
(hbnb) all
[]
(hbnb) help create
Create a new instance of data models, save it (to the JSON file) and print the id

Usage: create <class name>

data models are: BaseModel, User, State, City, Amenity, Place, Review
(hbnb) create User
60b0bba8-e9af-4da0-83e3-ab0e479a5285
(hbnb) all
["[User] (60b0bba8-e9af-4da0-83e3-ab0e479a5285) {'id': '60b0bba8-e9af-4da0-83e3-ab0e479a5285', 'created_at': datetime.datetime(2023, 8, 20, 9, 12, 59, 700603), 'updated_at': datetime.datetime(2023, 8, 20, 9, 12, 59, 700623)}"]
(hbnb) help update
Updates data model based on the class name and id by adding or updating attribute

Usage: update <class name> <id> <attribute name> 

data models are: BaseModel, User, State, City, Amenity, Place, Review
(hbnb) update User 60b0bba8-e9af-4da0-83e3-ab0e479a5285 name Betty
(hbnb) all User
["[User] (60b0bba8-e9af-4da0-83e3-ab0e479a5285) {'id': '60b0bba8-e9af-4da0-83e3-ab0e479a5285', 'created_at': datetime.datetime(2023, 8, 20, 9, 12, 59, 700603), 'updated_at': datetime.datetime(2023, 8, 20, 9, 12, 59, 700623), 'name': 'Betty'}"]
(hbnb) quit

