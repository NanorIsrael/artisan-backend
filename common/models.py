from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


# Create your models here.
class User(AbstractUser):
	GUEST = 'G'
	ARTISAN = 'A'

	MEMBERSHIP_CHOICES = [
		(GUEST, 'GUEST'),
		(ARTISAN, 'ARTISAN')
	]

	email =  models.EmailField(unique=True)
	membership = models.CharField(
		max_length=1,
		choices=MEMBERSHIP_CHOICES,
		default = GUEST
	)