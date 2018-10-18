from django.db import models
from django.contrib.auth.models import User
from datetime import date
# Create your models here.

class Genre(models.Model):
	"""
	Modelo que representa un genero literario (p. ej. ceincia ficcion, poesia, etc)
	"""
	name = models.CharField(max_length=200, help_text="Enter a book genere")

	def __str__(self):
		"""
		Cadena que representa a la instancia particula del modelo (p. ej en el sition de Administracion)
		"""
		return self.name

from django.urls import reverse #used to generate URLs by reversing the URL patterens

class Book(models.Model):
	#Modelo que representa un libro (pero  no un ejempla especifico)
	title = models.CharField(max_length=200)

	author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
	#ForeignKey ya que un libro tiene un solo autor pero el mismo autor puede haber escrito mucho libros
	# 'Author' es un string, en vez de un objeto, porque la calse Author no ha sido declarada

	summary = models.TextField(max_length=1000, help_text="Enter a brief descrpition of the book")

	isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

	genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")

	#ManyToManyField, porque un genero puede contener muchos libros y un libro puede cubrir varios generos.
	#La clase Genre ya ha sido definida, entonces podemos especificar el obejto arriba

	language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)
	
	def __str__(self):
		#String que representa al objeto Book
		return self.title

	def get_absolute_url(self):
		#Devulve el URL a una instancia particular de Book
		return reverse('book-detail', args=[str(self.id)])

	class Meta:
		ordering =['title']

import uuid #Requerida para las instancias de los libros únicos

class BookInstance(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="ID unico para este libri particular en toda la biblioteca")
	book = models.ForeignKey('Book', on_delete=models.SET_NULL, null = True)
	imprint = models.CharField(max_length=200)
	due_back = models.DateField(null=True, blank=True)
	borrower = models.ForeignKey(User,on_delete=models.SET_NULL,null = True, blank = True)

	@property
	def is_overdue(self):
		if self.due_back and date.today() > self.due_back:
			return True
		return False

	
	hoy = date.today()

	LOAN_STATUS = (
		('m', 'Maintenance'),
		('o', 'On loan'),
		('a', 'Available'),
		('r', 'Reserved'),

	)

	status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, help_text='Disponibilidad del libro')

	class Meta:
		ordering=["due_back"]
		permissions = (("can_mark_returned","Set book as returned"),)
 

	def __str__(self):
		#String para representar el objeto del modelo

		return '%s (%s)' % (self.id, self.book.title)

class Author(models.Model):
	"""
	Modelo que representa un autor
	"""
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	date_of_birth = models.DateField(null=True, blank=True)
	date_of_death = models.DateField('Died', null=True, blank=True)


	def get_absolute_url(self):
		"""
		Retorna la url para acceder a una instancia particular de un autor
		"""
		return reverse('author-detail', args=[str(self.id)])

	def __str__(self):
		"""
		String para representar el Objeto Modelo
		"""		
		return '%s, %s' % (self.last_name, self.first_name)

	class Meta:
		ordering =['last_name']

class Language(models.Model):
	"""Modelo que representa el lenguaje"""

	name = models.CharField(max_length=200, help_text="Idioma del libro")

	def __str__(self):
		"""
		String para representar el objeto modelo
		"""
		return self.name


