# CHANGELOG

<a name="unreleased"></a>
## [Unreleased]

### Code Refactoring
- **console.py:** refactor to use comparison operators for equality tests
- **console.py:** refactored precmd to use comparison operator for equality test
- **console.py:** refactored do_count to call storage.all
- **console.py:** refactored do_all to call storage.all
- **console.py:** Refactored do_show to call storage.all

### Features
- **console.py:** Updated the do_create method to handle the <key name>=<value> parameter syntax for instantiation with kwargs

### Styles
- **console:** pycodestyle formatting
- **console.py:** pycodestyle formatting


<a name="v2.1.0"></a>
## [v2.1.0] - 2025-02-12
### Chores
- **setup_mysql_dev.sql:** Added MySQL setup file for development ([f34c4e0](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/f34c4e0f3c21d8c0d5996b87cae25969fe1323ea))
- **setup_mysql_test.sql:** Added MySQL setup file for testing ([59eeb6e](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/59eeb6eed7268f39d8ed6d3f66d8fcaab73e3dbd))

### Code Refactoring
- **console.py:** Refactored storage import from models ([8fcd9e7](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/8fcd9e75692ff88124b7e5fa148e98db35337d0f))
- **console.py:** Refactored exit() and print() with return True in do_EOF method ([d534c1e](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/d534c1e7a511d17424e8fcbdbe4c5ea7985d30a6))
- **console.py:** Refactored exit() with return True in do_quit method ([ad891f6](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/ad891f6bae73541cf1153c37646596dd0bcb6f94))

### Documentation
- **AUTHORS:** Added 'Albert Mwanza to authors' ([eb1305e](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/eb1305e1b5bbad2ceae12d7b92fd9f3f1dbc1345))
- **CHANGELOG.md:** Updated commit links ([8f2a484](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/8f2a484529f40376cd4aaa6349ecd02156348ac0))
- **CHANGELOG.md:** Updated to show commit links ([f2dd2a2](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/f2dd2a296a9efdba2e8759482e1ddc2fd1a9c9b1))
- **CHANGELOG.md:** Updated to show commit links ([169356d](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/169356dbc9b8542c9b1591745f377f42afaaf176))
- **CHANGELOG.md:** Added change log file ([d976a1d](https://github.com/mwanzaalbert/AirBnB_clone_v2/commit/d976a1d761adba4d73b8c8e364e8fd3af6d65df6))


<a name="v2.0.0"></a>
## v2.0.0 - 2025-02-11

[Unreleased]: https://github.com/mwanzaalbert/AirBnB_clone_v2/compare/v2.1.0...HEAD
[v2.1.0]: https://github.com/mwanzaalbert/AirBnB_clone_v2/compare/v2.0.0...v2.1.0
