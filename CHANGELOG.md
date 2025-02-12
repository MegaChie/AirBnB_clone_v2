<a name="unreleased"></a>
## [Unreleased]


<a name="v2.1.0"></a>
## [v2.1.0] - 2025-02-12
### Chores
- **setup_mysql_dev.sql:** Added MySQL setup file for development ([f34c4e0](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/f34c4e0f3c21d8c0d5996b87cae25969fe1323ea))
- **setup_mysql_test.sql:** Added MySQL setup file for testing ([59eeb6e](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/59eeb6eed7268f39d8ed6d3f66d8fcaab73e3dbd))

### Code Refactoring
- **console.py:** refactor to use comparison operators for equality tests ([efeb973](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/efeb973a43ac69267b3ed331fbcd1ea6b29c442a))
- **console.py:** refactored precmd to use comparison operator for equality test ([b1d03c2](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/b1d03c2cb0b3963acd0a8721020768343e6fcd8d))
- **console.py:** refactored do_count to call storage.all ([a5737f4](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/a5737f442be825cb2ce0ee932a20606940a8c547))
- **console.py:** refactored do_all to call storage.all ([1083dd1](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/1083dd15342653537467d4105dd6f08ec432f812))
- **console.py:** Refactored do_show to call storage.all ([8efeabd](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/8efeabd761daf018b276b3a04c684654baa90c28))
- **console.py:** Refactored storage import from models ([8fcd9e7](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/8fcd9e75692ff88124b7e5fa148e98db35337d0f))
- **console.py:** Refactored exit() and print() with return True in do_EOF method ([d534c1e](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/d534c1e7a511d17424e8fcbdbe4c5ea7985d30a6))
- **console.py:** Refactored exit() with return True in do_quit method ([ad891f6](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/ad891f6bae73541cf1153c37646596dd0bcb6f94))
- **console.py:** refactor to use comparison operators for equality tests ([efeb973](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/efeb973))
- **console.py:** refactored precmd to use comparison operator for equality test ([b1d03c2](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/b1d03c2))
- **console.py:** refactored do_count to call storage.all ([a5737f4](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/a5737f4))
- **console.py:** refactored do_all to call storage.all ([1083dd1](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/1083dd1))
- **console.py:** Refactored do_show to call storage.all ([8efeabd](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/8efeabd))
- **tests/test_models/review.py:** Added instantiation of review to setUp method and refactored the test methods ([ab20561](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/ab20561))
- **tests/test_models/place.py:** Added instantiation of place to setUp method and refactored the test methods ([f843c72](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/f843c72))
- **models/base_model.py:** Refactored to_dict method to iterate over __dict__ attribute and ignore the _sa_instance_state attribute ([ce431f5](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/ce431f5))
- **models/base_model.py:** Refactored save method to call storage.new method ([71c19ff](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/71c19ff))
- **models/base_model.py:** Refactored __str__ to use f-strings for the return string and to removed the _sa_instance_state attribute from the string representation ([a38b99e](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/a38b99e))
- **models/base_model.py:** Refactored __init__ to iterate over kwargs and update attributes using setattr function. Removed storage import from __init__ and calling of the storage.new method ([d788011](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/d788011))
- **models/engine/file_storage.py:** Refactored reload method to use self to access FileStorage__file_path and to load data to FileStorage__objects ([62bc9ce](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/62bc9ce))
- **models/engine/file_storage.py:** Refactored save method to use dictionary comprehension ([9303c93](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/9303c93))
- **models/engine/file_storage.py:** Refactored save method to use f-strings for key and self to update FileStorage__objects ([6578f5a](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/6578f5a))
- **console.py:** Refactored storage import from models ([8fcd9e7](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/8fcd9e7))
- **console.py:** Refactored exit() and print() with return True in do_EOF method ([d534c1e](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/d534c1e))
- **console.py:** Refactored exit() with return True in do_quit method ([ad891f6](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/ad891f6))
- **tests/test_models/amenity.py:** Renamed class to Pascal naming style ([b4b5a96](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/b4b5a96))

### Documentation
- **AUTHORS:** Added 'Albert Mwanza to authors' ([eb1305e](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/eb1305e1b5bbad2ceae12d7b92fd9f3f1dbc1345))
- **CHANGELOG.md:** Updated commit links ([8f2a484](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/8f2a484529f40376cd4aaa6349ecd02156348ac0))
- **CHANGELOG.md:** Updated to show commit links ([f2dd2a2](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/f2dd2a296a9efdba2e8759482e1ddc2fd1a9c9b1))
- **CHANGELOG.md:** Updated to show commit links ([169356d](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/169356dbc9b8542c9b1591745f377f42afaaf176))
- **CHANGELOG.md:** Added change log file ([d976a1d](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/d976a1d761adba4d73b8c8e364e8fd3af6d65df6))
- **tests/test_models/city.py:** Added docstrings ([de81e99](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/de81e99))
- **tests/test_models/amenity.py:** Added docstrings ([d70a4eb](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/d70a4eb))
- **tests/test_models/base_model.py:** Added module and method docstrings ([1ed07ba](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/1ed07ba))
- **CHANGELOG.md:** Added change log file ([d976a1d](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/d976a1d))
- **/CHANGELOG.md:** Added commit links ([2dbd158](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/2dbd158))
- **/CHANGELOG.md:** Updated log to include commit links ([c97d457](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/c97d457))
- **/CHANGELOG.md:** Added title ([067afbe](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/067afbe))
- **/CHANGELOG.md:** Added title ([7081a34](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/7081a34))
- **/CHANGELOG.md:** Updated changelog ([29d9569](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/29d9569))
- **CHANGELOG.md:** Updated changelog ([ed51879](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/ed51879))
- CHANGELOG.md added ([7d81b6f](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/7d81b6f))
- Add Albert Mwanza to AUTHORS file ([e574683](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/e574683))


### Features
- **console.py:** Updated the do_create method to handle the <key name>=<value> parameter syntax for instantiation with kwargs ([52f2dbc](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/52f2dbc1e76e7ca27dff33574cedd5313c3f6410))
- **models/user.py:** Updated class with attributes for SLQAlchemy table mapping ([10f26ef](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/10f26ef))
- **models/state.py:** Update class with attributes for SQLAlchemy table mapping ([6725fe2](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/6725fe2))
- **model/review.py:** Updated class with attributes for SQLAlchemy table mapping ([166e957](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/166e957))
- **models/place.py:** Updated class with class attributes for ORM mapping. Added association table for many-to-many relationship mapping between places and amenities tables. Added property and setter methods for use with FileStorage. ([22baca0](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/22baca0))
- **models/city.py:** Added class attributes for SQLAlchemy table mapping and relationship mapping ([a8c7707](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/a8c7707))
- **models/amenity.py:** Updated class Amenity to Inherit from BaseModel and Base. Added class attributes for SQLAlchemy table mapping and Many to Many relationship mapping with Places ([764f169](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/764f169))
- **models/base_model.py:** Added delete method to call storage.delete method to delete object from storage ([984e473](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/984e473))
- **models/basem_model.py:** Added class attributes for SQLAlchemy table mapping ([a2cbcac](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/a2cbcac))
- **models/engine/db_storage.py:** Added DBStorage module for managing database storage in MySQL ([50988b8](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/50988b8))
- **models/__init__.py:** Updated to instantiate storage based on the environment variable HBNB_TYPE_STORAGE ([0244162](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/0244162))
- **models/engine/file_storage.py:** Updated all method to allow filtering based on class ([c773e45](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/c773e45))
- **models/engine/file_storage.py:** Added a new public instance method to delete objects from storage ([a295eb8](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/a295eb8))


### Styles
- **console:** pycodestyle formatting ([0d3e2ef](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/0d3e2efdcc3173010d5f0501e2a3ace12447f785))
- **console.py:** pycodestyle formatting ([9be3ffe](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/9be3ffe3266439542d23b96d9ed890562f44d530))
- **console:** pycodestyle formatting ([0d3e2ef](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/0d3e2ef))
- **tests/test_console.py:** pycodestyle formatting ([e92953c](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/e92953c))
- **tests/test_models/test_engine/test_file_storage.py:** pycodestyle formatting ([e32e936](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/e32e936))
- **console.py:** pycodestyle formatting ([9be3ffe](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/9be3ffe))
- **tests/test_models/city.py:** Renamed imported class test_base_model to pascal case TestBaseModel ([fa5dc8e](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/fa5dc8e))
- **tests/test_models/amenity.py:** Renamed imported class test_base_model to pascal case TestBaseModel ([62ff0d2](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/62ff0d2))
- **tests/test_models/base_model.py:** renamed class name to conform to PascalCase ([83d8a3d](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/83d8a3d))
- **tests/test_models/test_engine/test_db_storage.py:** pycodestyle formatting ([c0ce84b](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/c0ce84b))
- **models/base_model.py:** pycodestyle formatting ([96d660f](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/96d660f))
- **models/engine/file_storage.py:** Pycodestyle Formatting ([fcedbb6](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/fcedbb6))

### Tests
- **tests/test_models/test_engine/test_file_storage.py:** Added test for the delete method and test classes for each model ([534c45c](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/534c45c))
- **tests/test_models/user.py:** Added docstrings and additional assertions for each test method ([8a55601](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/8a55601))
- **tests/test_models/state.py:** Added docstrings and additional assertions for test_name3 ([a731604](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/a731604))
- **tests/test_models/test_engine/test_db_storage.py:** Add tests for DBStorage ([3dd588b](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/3dd588b))
- **tests/test_console.py:** Add console tests for file and database storage ([9a8fc14](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/9a8fc14))

### Chores
- **models/state.py:** Added executable rights ([f75d27f](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/f75d27f))
- **models/place.py:** Added executable rights ([7eae5aa](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/7eae5aa))
- **models/city.py:** Added executable rights ([4d8948c](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/4d8948c))
- **models/amenity.py:** Added executable rights ([2d497fb](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/2d497fb))
- **models/engine/file_storage.py:** Added encoding declaration ([37d9454](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/37d9454))
- **models/__init__.py:** Added executable rights ([38af25e](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/38af25e))
- **models/__init_.py:** Added encoding declaration ([b767157](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/b767157))
- **models/engine/__init__.py:** Added executable rights ([c1467b9](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/c1467b9))
- **models/engine/file_storage.py:** Added executable rights ([a313ed6](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/a313ed6))
- **setup_mysql_test.sql:** Added MySQL setup file for testing ([59eeb6e](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/59eeb6e))
- **setup_mysql_dev.sql:** Added MySQL setup file for development ([f34c4e0](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/f34c4e0))
- **setup_mysql_dev.sql:** Added MySQL setup file for development ([628f4a2](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/628f4a2))
- **tests/__init__:** Added executable rights ([0775e3f](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/0775e3f))

<a name="v2.0.0"></a>
## v2.0.0 - 2025-02-11

[Unreleased]: https://github.com/mwanzaalbert/AirBnB_clone_v2/compare/v2.1.0...HEAD
[v2.1.0]: https://github.com/mwanzaalbert/AirBnB_clone_v2/compare/v2.0.0...v2.1.0
