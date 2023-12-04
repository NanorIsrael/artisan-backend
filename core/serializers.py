from rest_framework import serializers
from .models import Customer, ArtisanCategory, ArtisanPortfolio, Address


class CustomerSerializer(serializers.ModelSerializer):
	user_id = serializers.IntegerField()

	class Meta:
		model = Customer
		fields = ['id', 'user_id', 'phone', 'first_name', 'last_name', 'birth_date', 'membership']

class AddressSerializer(serializers.ModelSerializer):
	class Meta:
		model = Address
		fields = ['id', 'house_number', 'street', 'city', 'state']

class ArtisanCategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = ArtisanCategory
		fields = ['id', 'category']


class ArtisanPortfolioSerializer(serializers.ModelSerializer):
	address = serializers.SerializerMethodField()
	# AddressSerializer(many=True, read_only=True)
	class Meta:
		model = ArtisanPortfolio
		fields = ['id', 'job_title', 'summary', 'category', 'address']
		depth = 1

	def get_address(self, obj):
		# Assuming 'address' is the related name in the ArtisanPortfolio model
		# users = obj.user
		# print(users)
		addresses = Address.objects.all()
		return AddressSerializer(addresses).data