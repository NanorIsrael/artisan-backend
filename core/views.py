from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Customer, ArtisanCategory, ArtisanPortfolio
from .serializers import CustomerSerializer, ArtisanCategorySerializer, ArtisanPortfolioSerializer

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
	permission_classes = [IsAuthenticated]

	@action(detail=False, methods=['GET', 'PUT'])
	def me(self, request):
		(customer, created) = Customer.objects.get_or_create(user_id=request.user.id)
		serialized = CustomerSerializer(customer)
		return Response(serialized.data)

class ArtisanCategoryViewSet(viewsets.ModelViewSet):
	queryset = ArtisanCategory.objects.all()
	serializer_class = ArtisanCategorySerializer


class ArtisanPortfolioViewSet(
	CreateModelMixin, RetrieveModelMixin, 
	UpdateModelMixin, GenericViewSet
):
	queryset = ArtisanPortfolio.objects.all()
	serializer_class = ArtisanPortfolioSerializer
	permission_classes = [IsAuthenticated]

	@action(detail=False, methods=['GET', 'PUT', 'POST'])
	def profile(self, request):
		(artisan, created) = ArtisanPortfolio.objects.get_or_create(user_id=request.user.id)
		if request.method == 'GET': 
			serialized = ArtisanPortfolioSerializer(artisan)
			return Response(serialized.data)
		else:
			serialized = ArtisanPortfolioSerializer(artisan, data=request.data)
			serialized.is_valid(raise_exception=True)
			serialized.save()
			return Response(serialized.data)