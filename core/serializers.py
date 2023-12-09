from rest_framework import serializers
from .models import Customer, ArtisanCategory, ArtisanPortfolio, Address


class CustomerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Customer
		fields = ['id', 'phone', 'first_name', 'last_name', 'birth_date', 'membership']

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

	class Meta:
		model = ArtisanPortfolio
		fields = ['id', 'job_title', 'summary', 'category', 'addresses']

	def get_addresses(self, obj):
	# 	# Assuming 'address' is the related name in the ArtisanPortfolio model
		addresses = obj.user.address_set.all()
		return AddressSerializer(addresses, many=True).data


class ArtisanUserIdSerializer(serializers.ModelSerializer):
	class Meta:
		model = ArtisanPortfolio
		fields = ['id', 'user_id']
