[![Pypi version](https://img.shields.io/pypi/v/relationaldb.svg)](https://pypi.org/project/relationaldb/) [![Python versions](https://img.shields.io/pypi/pyversions/relationaldb.svg)](https://pypi.org/project/relationaldb/) [![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

-----------------

# relationaldb

RelationalDB is a python ODM library for MongoDB that allows you to design collections like you do it for your normal dataclasses objects.

**DISCLAMER**

This library is in alpha-release, it's a work in progress for the moment, excellent libraries for MongoDB ODM in python exist:

- https://github.com/roman-right/beanie/

There are a lot of none implemented main features (I implement them when I have time or when I need it for my project).

# Quickstart

relationaldb wraps `attrs` to create classes boilerplate and add few parameters.

## One to Many relation

Let's say you want a simple one to many relations, with two entities: Animal and Person.

- Each animal can have one owner (Person)
- Each person can have 0 to many animals

```python
from relationaldb import conception

# Object to design the architecture of the database
c = conception()


# Add collection woth 'define' like with attrs
@c.define
class Person:
    # add new attribute with 'field' method
    # in_filter_query parameter allows to use the 'db.Person.feed' method to upsert new documents
    name: str = c.field(in_filter_query=True)

    # all attrs.fields parameters are available
    money: int = c.field(kw_only=True, default=0)
    birth_year: int = c.field(kw_only=True, default=None)


@c.define
class Animal:
    # We can reference
    name: Person = c.field(in_filter_query=True)

    owner: Person = c.field(kw_only=True, default=None)
    birth_year: int = c.field(kw_only=True, default=None)


# Create a new mongodb named "mydb"
db = c.mongodb("relationaldb_mydb_01")

# Create second DB with same architecture
db2 = c.mongodb("relationaldb_mydb_02")

# Create a new person
db.Person.insert_one("John")

# Get the person
person = db.Person.first()
assert isinstance(person, Person)
assert person.name == "John"

for person in db.Person:
    print(person)

# Upsert (create or update) person named 'Smith' if it does not exists (based on in_filter_query)
db.Person.feed("Smith")  # will create the person
db.Person.feed("Smith")  # will do nothing, person already exist
db.Person.feed("Smith", money=1000)  # will update the person 'Smith'
```
