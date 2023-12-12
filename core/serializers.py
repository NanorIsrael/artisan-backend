from django.db.models.aggregates import Avg
from rest_framework import serializers
from .models import (
	Customer, ArtisanCategory, ArtisanPortfolio, Address,
	Customer_profile_photo, Ratings
)

class ArtisanRatingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Ratings
		fields = ['id', 'rating']


class Profile_photo_serializer(serializers.ModelSerializer):
	class Meta:
		model = Customer_profile_photo
		fields = ['id', 'photo']
	

class CustomerSerializer(serializers.ModelSerializer):
	photos = Profile_photo_serializer(many=True, read_only=True)

	class Meta:
		model = Customer
		fields = [
			'id', 'phone', 'first_name', 'last_name',
			'birth_date', 'membership', 'email',
			'username', 'photos',
		]


class AddressSerializer(serializers.ModelSerializer):
	class Meta:
		model = Address
		fields = ['id', 'house_number', 'street', 'city', 'state']

class ArtisanCategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = ArtisanCategory
		fields = ['id', 'category']

class ArtisanAddressSerializer(serializers.ModelSerializer):
	class Meta:
		model = Address
		fields = ['id', 'artisan_id', 'address']

class ArtisanPortfolioSerializer(serializers.ModelSerializer):
	addresses = serializers.SerializerMethodField()
	phone = serializers.SerializerMethodField()
	ratings = serializers.SerializerMethodField()

	class Meta:
		model = ArtisanPortfolio
		fields = ['id', 'job_title', 'summary', 'category', 'phone', 'addresses', 'ratings']

	def get_phone(self, obj):
		try:
			customer = obj.user.customer
			return customer.phone if customer else None
		except Customer.DoesNotExist:
			return None

	def get_ratings(self, obj):
		try:
			user_ratings = Ratings.objects.filter(artisan_id=obj.id).aggregate(average_ratings=Avg('rating'))
			return user_ratings['average_ratings']
		except (ArtisanPortfolio.DoesNotExist, Ratings.DoesNotExist):
			return {'average_ratings': 0}

	def get_addresses(self, obj):
	# 	# Assuming 'address' is the related name in the ArtisanPortfolio model
		addresses = obj.user.address_set.all()
		return AddressSerializer(addresses, many=True).data


class ArtisanUserIdSerializer(serializers.ModelSerializer):
	class Meta:
		model = ArtisanPortfolio
		fields = ['id', 'user_id']
