# familytree
system which can help a user define his family tree

Backend Coding Challenge for market pulse


# How to setup the project for test

1. clone
2. `cd familytree`
3. `pip3 install -r requirements.txt`  # Note - better you do this using virtualenvwrapper
4. `python manage.py runserver 0:8000`
5. go to `localhost:8000/admin`
6. login with `breadearner@family.com/@Least8Chars`
7. create family members as you wish.
8. for querying the data using ORM 
	8.1 go to terminal
	8.2 `cd familytree` 
	8.3 `python3 manage.py shell`
	8.4 `from family.models import FamilyMember, Marriage`
	8.5 create object of FamilyMember
		8.5.1 `fm = FamilyMember.objects.get(id=1)`
		8.5.2 `fm`
		8.5.3. `dir(fm)`


# to do:

following queries need to be addressed

1. `family-tree count immediate sons of <name>`
2. `family-tree count all daughters of <name>`
3. `family-tree count immediate cousins of <name>`
4. `family-tree count wives of <name>`
5. `family-tree is <name> and <name> related?`
6. `family-tree count uncles of <name>`

