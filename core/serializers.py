from rest_framework import serializers
from .models import Customer, ArtisanCategory, ArtisanPortfolio, Address


class CustomerSerializer(serializers.ModelSerializer):
	user_id = serializers.IntegerField()

	class Meta:
		model = Customer
		fields = ['id', 'user_id', 'phone', 'first_name', 'last_name', 'birth_date', 'membership']


class ArtisanCategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = ArtisanCategory
		fields = ['id', 'category']


class ArtisanPortfolioSerializer(serializers.ModelSerializer):
	class Meta:
		model = ArtisanPortfolio
		fields = ['id', 'job_title', 'summary', 'category']


class AddressSerializer(serializers.ModelSerializer):
	class Meta:
		model = Address
		fields = ['id', 'house_number', 'street', 'city', 'state']
