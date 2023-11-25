from rest_framework import serializers
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
	user_id = serializers.IntegerField()

	class Meta:
		model = Customer
		fields = ['id', 'user_id', 'phone', 'first_name', 'last_name', 'birth_date', 'membership']