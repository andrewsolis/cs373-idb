from django.db import models

# Create your models here.

class Game(models.Model):
	# name, id, system, release_date, genre, publisher, 
	# developer, synopsis, copies_sold, images, videos, People, Companies.
	name = models.CharField(max_length=100)
	system = models.CharField(max_length=100)
	genre = models.CharField(max_length=100)
	synopsis = models.CharField(max_length=1000)
	copies = models.IntegerField(default=0)
	release_date = models.DateTimeField('date published')
	companies = models.ForeignKey(Company)
	people = models.ForeignKey(Person)

class Company(models.Model):
	# name, id, founded, location, kind, description, 
	# images, maps, external_links, contact_info, Games. 
	name = models.CharField(max_length=100)
	founded = models.DateTimeField('date founded')
	location = models.CharField(max_length=100)
	kind = models.CharField(max_length=100)
	games = models.ForeignKey(Game)
	people = models.ForeignKey(Person)


class Person(models.Model):
	# name, id, DOB, location, job, description, images, Games, Companies
	name = models.CharField(max_length=100)
	DOB = models.DateTimeField('date born')
	title = models.CharField(max_length=100)
	residence = models.CharField(max_length=100)
	games = models.ForeignKey(Game)
	companies = models.ForeignKey(Company)
