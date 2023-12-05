from django.contrib import admin
from django.conf import settings
from django.db import models


# Create your models here.
class Customer(models.Model):

	phone = models.CharField(max_length=255)
	birth_date = models.DateField(null=True, blank=True)

	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.user.first_name} {self.user.last_name}'

	def membership(self):
		return self.user.membership

	@admin.display(ordering='user__first_name')
	def first_name(self):
		return self.user.first_name
	
	def last_name(self):
		return self.user.last_name

	class Meta:
		ordering = ['user__first_name', 'user__last_name']


class Address(models.Model):
	house_number = models.CharField(max_length=255)
	street = models.CharField(max_length=255)
	city = models.CharField(max_length=255)
	state = models.CharField(max_length=255)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class ArtisanCategory(models.Model):
	BUILDING_AND_CONSTRUCTION = 'BUILDING_AND_CONSTRUCTION'
	CARPENTRY = 'CARPENTRY'
	ELECTRICAL_ENGINEERING = 'ELECTRICAL ENGINEERING'
	METAL_WORKS = 'METAL WORKS'
	PLUMBING_WORKS = 'PLUMBING WORKS'
	TRANSPORTATION = 'TRANSPORTATION'
	OTHERS = 'OTHERS'

	MEMBERSHIP_CHOICES = [
		(BUILDING_AND_CONSTRUCTION, 'BUILDING AND CONSTRUCTION'),
		(CARPENTRY, 'CARPENTRY'),
		(ELECTRICAL_ENGINEERING, 'ELECTRICAL ENGINEERING'),
		(METAL_WORKS, 'METAL WORKS'),
		(PLUMBING_WORKS, 'PLUMBING WORKS'),
		(TRANSPORTATION, 'TRANSPORTATION'),
		(OTHERS, 'OTHERS'),
	]

	category = models.CharField(max_length=255, choices=MEMBERSHIP_CHOICES, default=BUILDING_AND_CONSTRUCTION)


class ArtisanPortfolio(models.Model):
	BUILDING_AND_CONSTRUCTION = 'BUILDING_AND_CONSTRUCTION'
	CARPENTRY = 'CARPENTRY'
	ELECTRICAL_ENGINEERING = 'ELECTRICAL ENGINEERING'
	METAL_WORKS = 'METAL WORKS'
	PLUMBING_WORKS = 'PLUMBING WORKS'
	TRANSPORTATION = 'TRANSPORTATION'
	OTHERS = 'OTHERS'

	MEMBERSHIP_CHOICES = [
		(BUILDING_AND_CONSTRUCTION, 'BUILDING AND CONSTRUCTION'),
		(CARPENTRY, 'CARPENTRY'),
		(ELECTRICAL_ENGINEERING, 'ELECTRICAL ENGINEERING'),
		(METAL_WORKS, 'METAL WORKS'),
		(PLUMBING_WORKS, 'PLUMBING WORKS'),
		(TRANSPORTATION, 'TRANSPORTATION'),
		(OTHERS, 'OTHERS'),
	]

	job_title = models.CharField(max_length=255)
	summary = models.TextField()
	category = models.CharField(max_length=255, choices=MEMBERSHIP_CHOICES, default=BUILDING_AND_CONSTRUCTION)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
