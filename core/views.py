from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from .models import Customer
from .serializers import CustomerSerializer

# Create your views here.
# @api_view(['GET'])
# def Customer(request):
# 	return Response('ok')

class CustomerViewSet(
	CreateModelMixin, RetrieveModelMixin, 
	UpdateModelMixin, GenericViewSet
):
	queryset = Customer.objects.all()
	serializer_class = CustomerSerializer