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
	name = models.CharField(max_length=100)
	system = models.ForeignKey('System')
	genre = models.ManyToManyField('Genre')
	synopsis = models.TextField()
	copies = models.IntegerField(default=0)
	release_date = models.DateTimeField('date published')
	company = models.ForeignKey('Company')
	people = models.ManyToManyField('Person')
	gamefaq = models.URLField()

	def images(self):
		return Images.objects.filter(other_id = self.id, other_type = 'GM')

	def videos(self):
		return Videos.objects.filter(other_id = self.id, other_type = 'GM')

class Person(models.Model):
	"""
	A store for holding info for a Person
	"""
	# name, id, DOB, location, job, description, images, Games, Companies
	name = models.CharField(max_length=100)
	DOB = models.DateTimeField('date born')
	twitter = models.CharField(max_length=200)
	description = models.TextField()
	residence = models.CharField(max_length=50)
	companies = models.ManyToManyField('Company')
	# games = models.ManyToMany(Game)
	
	def images(self):
		return Images.objects.filter(other_id = self.id, other_type = 'PPL')
	def videos(self):
		return Videos.objects.filter(other_id = self.id, other_type = 'PPL')

class Company(models.Model):
	"""
	A store for holding info for a Company
	"""
	# name, id, founded, location, kind, description, 
	# images, maps, external_links, contact_info, Games. 
	name = models.CharField(max_length=100)
	founded = models.DateTimeField('date founded')
	description = models.TextField()
	twitter = models.CharField(max_length=200)
	location = models.CharField(max_length=50)
	mapimage = models.URLField()
	webpage = models.URLField()
	# games = models.ManyToMany(Game)
	# people = models.ManyToMany(Person)

	def images(self):
		return Images.objects.filter(other_id = self.id, other_type = 'CP')

