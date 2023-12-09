from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from .models import User


class UserSerializer(UserCreateSerializer):
	membership = serializers.BooleanField()

	def create(self, validated_data):
		membership = validated_data.pop('membership', False)
		user = super().create(validated_data)  # Corrected method name

		# Set the membership status based on the boolean value
		user.membership = 'A' if membership else 'G'
		user.save()

		return user

	class Meta(UserCreateSerializer.Meta):
		model = User
		fields = ['id', 'email', 'username', 'password', 'membership']
