# Create your models here.
from django.db import models

class Images(models.Model):
	#id, link 
	link = models.URLField()
	

class Videos(models.Model):
	#id, link 
	link = models.URLField()

class Genre(model.Model):
	#id, #types
	types = models.CharField(max_length=100)

class Job(models.Model):
	#id, #profession
	profession = models.CharField(max_length=100);

class System(models.Model):
	#id, #platform
	platform = models.CharField(max_length=100);


class Game(models.Model):
	# name, id, system, release_date, genre, publisher, 
	# developer, synopsis, copies_sold, images, videos, People, Companies.
	name = models.CharField(max_length=100)
	system = models.ForeignKey(System)
	genre = models.ManyToManyField(Genre)
	synopsis = models.CharField(max_length=1000)
	copies = models.IntegerField(default=0)
	release_date = models.DateTimeField('date published')
	company = models.ForeignKey(Company)
	people = models.ManyToManyField(Person)
	images = models.
	videos = models.
	gamefaq = models.URLField()

class Person(models.Model):
	# name, id, DOB, location, job, description, images, Games, Companies
	name = models.CharField(max_length=100)
	DOB = models.DateTimeField('date born')
	title = models.CharField(max_length=100)
	jobs = models.ManyToMany(Job)
	description = models.CharField(max_length=1000)
	residence = models.CharField(max_length=100)
	# games = models.ManyToMany(Game)
	companies = models.ManyToMany(Company)
	images = models.
	videos = models.

class Company(models.Model):
	# name, id, founded, location, kind, description, 
	# images, maps, external_links, contact_info, Games. 
	name = models.CharField(max_length=100)
	founded = models.DateTimeField('date founded')
	description = models.CharField(max_length=1000)
	location = models.CharField(max_length=100)
	kind = models.CharField(max_length=100)
	# games = models.ManyToMany(Game)
	# people = models.ManyToMany(Person)
	images = models.
	_map = models.URLField()
	webpage = models.URLField()


