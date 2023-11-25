from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from .models import User


class UserSerializer(UserCreateSerializer):
	membership = serializers.BooleanField()

	def create(self, validated_data):
		membership = validated_data.pop('membership', None)
		user = super().create(validated_data)
		user.membership = 'A' if membership else 'G'
		user.save()
		return user
		
	class Meta:
		model = User
		fields = ['id', 'email', 'username', 'password', 'membership']