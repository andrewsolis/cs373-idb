cs373-idb
=========

Specification
-------------
Create a Django app hosted on Heroku with Python and Twitter Bootstrap that emulates IMDB to track something.

The rest of this description uses world crises just as an example.

Your group must propose a similar topic with similar resources.

For the purposes of grading, do not change the Heroku website between the time that you submit it and the time that it is graded.

For all projects, the minimum requirement for getting a non-zero grade is to write standard-compliant Python (3.2.3), to satisfy all of the requirements in the table below, including the precise naming of all the files, and to fill out the Google Form.

IMDB has two major kinds of pages: movies/shows and people. Movies/shows link to people and people link back to movies/shows.

World Crisis will have three major kinds of pages: crises, organizations, and people, and again each will link to the others.

There will be three phases.

Phase 1
=======

Create a private Git repository at GitHub, named cs373-idb.
Use the same repo for all three phases.
Add all of the requirements (above) to the issue tracker at GitHub.
Clone your private IDB repo onto your local directory.
Invite the grader to your private IDB repo.
Confirm that the grader has invited you back to the public test repo.
Clone the public test repo onto your local directory. It is critical that you clone the public test repo into a different directory than the one you're using for your private IDB repo.
Write unit tests in tests.py until you have an average of 3 tests for each API call, confirm the expected failures, and add, commit, and push to the private IDB repo.
Implement and debug the simplest possible solution in apiary.apib until all tests pass and add, commit, and push to the private IDB repo.
Create a set of Django models.
Create a website with Django and Twitter Bootstrap on Heroku.
Define a workflow that uses pull requests.
Copy your unit tests to your clone of the public test repo, rename the files, do a git pull to synchronize your clone, and then add, commit and push to the public test repo.
Run epydoc on Models.py.
Write the technical report.
Fill in the Google Form.
It is your responsibility to protect your code from the rest of the students in the class. If your code gets out, you are as guilty as the recipient of academic dishonesty.

Submission
==========
Provide your git SHA in the Google Form.

Obtain your git SHA with

Make sure you have the following files:

makefile
apiary.apib
Models.html
Models.py
Report.pdf
tests.out
tests.py
