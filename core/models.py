from django.contrib import admin
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class Customer(models.Model):
	MALE = 'M'
	FEMALE = 'F'
	OTHER = 'OTHER'
	SEX_CHOICES = [
		(MALE, 'M'),
		(FEMALE, 'F'),
		(OTHER, 'OTHER'),
	]
	birth_date = models.DateField(null=True, blank=True)
	phone = models.CharField(max_length=255)
	sex = models.CharField(max_length=255, choices=SEX_CHOICES, default=OTHER)
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

	def email(self):
		return self.user.email

	def username(self):
		return self.user.username


	class Meta:
		ordering = ['user__first_name', 'user__last_name']


class Customer_profile_photo(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='photos');
	photo = models.ImageField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def save(self, *args, **kwargs):
		self.updated_at = timezone.now()
		super().save(*args, **kwargs)


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
	category = models.CharField(max_length=255, choices=MEMBERSHIP_CHOICES, default=OTHERS)
	business_line = models.CharField(max_length=255)

	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	class Meta:
		ordering = ['id']  # Replace 'id' with the field you want to use for ordering


class Artisan_profile_photo(models.Model):
	artisan = models.ForeignKey(ArtisanPortfolio, on_delete=models.CASCADE, related_name='photos');
	photo = models.ImageField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def save(self, *args, **kwargs):
		self.updated_at = timezone.now()
		super().save(*args, **kwargs)


class Countries(models.Model):
	name = models.CharField(max_length=255)
	code = models.CharField(max_length=255)
	flag = models.CharField(max_length=255)

class States(models.Model):
	name = models.CharField(max_length=255)
	country = models.ForeignKey(Countries, on_delete=models.CASCADE)

class Cities(models.Model):
	name = models.CharField(max_length=255)
	state = models.ForeignKey(States, on_delete=models.CASCADE)

class Streets(models.Model):
	name = models.CharField(max_length=255)
	city = models.ForeignKey(Cities, on_delete=models.CASCADE)

class ArtisanAddress(models.Model):
	artisan= models.ForeignKey(ArtisanPortfolio, on_delete=models.CASCADE)
	address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='address')


class Ratings(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE);
	artisan = models.ForeignKey(ArtisanPortfolio, on_delete=models.CASCADE, related_name='ratings');
	rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Reviews(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE);
	artisan = models.ForeignKey(ArtisanPortfolio, on_delete=models.CASCADE, related_name='reviews');
	review = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
