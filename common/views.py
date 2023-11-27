from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import api_view
from .models import User
from .serializers import UserSerializer


# Create your views here.
# @api_view(['POST'])
# def UserSignup(request):
# 	user = User.objects.get_or_create(username=request.data.get('username'))
# 	serializer = UserSerializer(user)
# 	serializer.is_validate(raise_exception=True)
# 	serializer.save()
# 	return Response(serializer.data)
