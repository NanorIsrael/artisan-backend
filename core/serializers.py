from django.db.models.aggregates import Avg
from rest_framework import serializers
from .models import (
	Customer, ArtisanCategory, ArtisanPortfolio, Address,
	Customer_profile_photo, Ratings, Reviews, Artisan_profile_photo
)

class ArtisanRatingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Ratings
		fields = ['id', 'rating']

class ArtisanReviewSerializer(serializers.ModelSerializer):
	reviewer = serializers.SerializerMethodField()

	class Meta:
		model = Reviews
		fields = ['id', 'review', 'updated_at', 'reviewer']

	def get_reviewer(self, obj):
		customer = CustomerSerializer(obj.customer)
		if customer.data['first_name']:
			reviewer = f"{customer.data['first_name']} {customer.data['last_name']}"
		else:
			reviewer = customer.data['username']
		return reviewer
		


class Profile_photo_serializer(serializers.ModelSerializer):
	class Meta:
		model = Customer_profile_photo
		fields = ['id', 'photo']
	
class Business_photo_serializer(serializers.ModelSerializer):
	class Meta:
		model = Artisan_profile_photo
		fields = ['id', 'photo']
	

class CustomerSerializer(serializers.ModelSerializer):
	photos = Profile_photo_serializer(many=True, read_only=True)
	isArtisan = serializers.SerializerMethodField()

	class Meta:
		model = Customer
		fields = [
			'id', 'phone', 'first_name', 'last_name',
			'birth_date', 'membership', 'email',
			'username', 'photos', 'isArtisan'
		]

	def get_isArtisan(self, obj):
		return ArtisanPortfolio.objects.filter(user=obj.user).exists()

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
	ratings = serializers.SerializerMethodField()
	reviews = ArtisanReviewSerializer(many=True, read_only=True)
	photo = serializers.SerializerMethodField()


	class Meta:
		model = ArtisanPortfolio
		fields = ['id', 'job_title', 'summary', 'category', 'business_line', 'addresses', 'ratings', 'reviews', 'photo']

	def get_photo(self, obj):
		try:
			artisan_user = Customer.objects.get(user_id=obj.user.id)
			artisan_photo = Customer_profile_photo.objects.get(customer_id=artisan_user.id)
			serialized = Profile_photo_serializer(artisan_photo)
			return serialized.data['photo'] if artisan_photo else None
		except Customer_profile_photo.DoesNotExist:
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
