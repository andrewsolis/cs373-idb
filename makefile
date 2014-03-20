all:

clean:
	rm -f *.pyc
	rm -f Models.html

Models.html: Models.py
	epydoc IDB
