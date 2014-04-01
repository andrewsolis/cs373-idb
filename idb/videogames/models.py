# Create your models here.
from django.db import models

class Media(models.Model):
	"""
	A generic store for links to media, both local and remote.
	link is the URL
	We had to use this type of model because Django does not handle polymorphism
	"""
	link = models.URLField()
	other_id = models.IntegerField()
	other_type = models.CharField(max_length=25, choices=[('GM', 'Game'), ('PPL', 'People'), ('CP', 'Company')])

class Images(Media):
	"""
	A Media table for storing images
	"""
	#id, name, link 
	pass

class Videos(Media):
	"""
	A Media table for storing videos
	"""
	#id, name, link 
	pass

class Genre(models.Model):
	"""
	A store for holding Genre names
	"""
	#id, #types
	types = models.CharField(max_length=25)

# class Job(models.Model):
# 	"""
# 	A store for holding Job names
# 	"""
# 	#id, #profession
# 	profession = models.CharField(max_length=25);

class System(models.Model):
	"""
	A store for holding system names
	"""
	#id, #platform
	platform = models.CharField(max_length=25);


class Game(models.Model):
	"""
	A store for holding info on a game
	"""
	# name, id, system, release_date, genre, publisher, 
	# developer, synopsis, copies_sold, images, videos, People, Companies.
	name = models.CharField(max_length=25)
	system = models.ForeignKey('System')
	genre = models.ManyToManyField('Genre')
	synopsis = models.CharField(max_length=1000)
	copies = models.IntegerField(default=0)
	release_date = models.DateTimeField('date published')
	company = models.ForeignKey('Company')
	people = models.ManyToManyField('Person')
	gamefaq = models.URLField()

	def images(self):
		results = Images(other_id = self.id, other_type = 'GM')
		return results.objects

	def videos(self):
		results = Videos(other_id = self.id, other_type = 'GM')
		return results.objects

class Person(models.Model):
	"""
	A store for holding info for a Person
	"""
	# name, id, DOB, location, job, description, images, Games, Companies
	name = models.CharField(max_length=25)
	DOB = models.DateTimeField('date born')
	# title = models.CharField(max_length=25)
	# jobs = models.ManyToManyField('Job')
	description = models.CharField(max_length=1000)
	residence = models.CharField(max_length=50)
	companies = models.ManyToManyField('Company')
	# games = models.ManyToMany(Game)
	
	def images(self):
		results = Images(other_id = self.id, other_type = 'PPL')
		return results.objects

	def videos(self):
		results = Videos(other_id = self.id, other_type = 'PPL')
		return results.objects

class Company(models.Model):
	"""
	A store for holding info for a Company
	"""
	# name, id, founded, location, kind, description, 
	# images, maps, external_links, contact_info, Games. 
	name = models.CharField(max_length=25)
	founded = models.DateTimeField('date founded')
	description = models.CharField(max_length=1000)
	location = models.CharField(max_length=50)
	mapimage = models.URLField()
	webpage = models.URLField()
	# games = models.ManyToMany(Game)
	# people = models.ManyToMany(Person)

	def images(self):
		results = Images(other_id = self.id, other_type = 'CP')
		return results.objects

	def videos(self):
		return QuerySet.none().objects
