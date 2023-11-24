from django.contrib import admin
from django.conf import settings
from django.db import models


# Create your models here.
class Customer(models.Model):
	GUEST = 'G'
	ARTISAN = 'A'

	MEMBERSHIP_CHOICES = [
		(GUEST, 'GUEST'),
		(ARTISAN, 'ARTISAN')
	]
	phone = models.CharField(max_length=255)
	birth_date = models.DateField(null=True, blank=True)
	membership = models.CharField(
		max_length=1,
		choices=MEMBERSHIP_CHOICES,
		default = GUEST
	)
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.user.first_name} {self.user.last_name}'
	
	@admin.display(ordering='user__first_name')
	def first_name(self):
		return self.user.first_name
	
	def last_name(self):
		return self.user.last_name
	
	class Meta:
		ordering = ['user__first_name', 'user__last_name']