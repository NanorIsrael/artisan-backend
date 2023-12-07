from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
# from rest_framework.pagination import Paginator
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Customer, ArtisanCategory, ArtisanPortfolio, Address
from .pagination import DefaultPagination
from .serializers import (
	CustomerSerializer, ArtisanCategorySerializer, ArtisanPortfolioSerializer, AddressSerializer
)

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


class AddressViewSet(
	CreateModelMixin, RetrieveModelMixin, 
	UpdateModelMixin, GenericViewSet
):
	queryset = Address.objects.all()
	serializer_class = AddressSerializer
	filter_backends = [SearchFilter]
	search_fields = ['street', 'city', 'state']

	@action(detail=False, methods=['GET', 'PUT', 'POST'])
	def profile(self, request):
		permission_classes = [IsAuthenticated]
		(address, created) = Address.objects.get_or_create(user_id=request.user.id)
		if request.method == 'GET': 
			serialized = AddressSerializer(address)
			return Response(serialized.data)
		else:
			serialized = AddressSerializer(address, data=request.data)
			serialized.is_valid(raise_exception=True)
			serialized.save()
			return Response(serialized.data)

	@action(detail=False, methods=['GET'])
	def streets(self, request):
			streets = Address.objects.all()
			serialized = AddressSerializer(streets, many=True)
			street_data = [item['street'] for item in serialized.data]
			return Response(street_data)

	@action(detail=False, methods=['GET'])
	def cities(self, request):
			cities = Address.objects.all()
			serialized = AddressSerializer(cities, many=True)
			city_data = [item['city'] for item in serialized.data]
			return Response(city_data)

	@action(detail=False, methods=['GET'])
	def states(self, request):
			return Response([
				'Greater Accra', 'Volta', 'Oti', 'Eastern',
				'Ashanti', 'Brong Ahafo', 'Bono East', 'Western',
				'Upper west', 'Ahafo', 'Western North', 'Upper East',
				'Central', 'North East', 'Northern', 'Savannah',
				])

class ArtisanCategoryViewSet(viewsets.ModelViewSet):
	queryset = ArtisanCategory.objects.all()
	serializer_class = ArtisanCategorySerializer


class ArtisanPortfolioViewSet(
	viewsets.ModelViewSet
):
	queryset = ArtisanPortfolio.objects.all()
	serializer_class = ArtisanPortfolioSerializer
	filter_backends = [SearchFilter]
	pagination_class = DefaultPagination
	search_fields = ['job_title', 'category', 'summary', 'user__address__city', 'user__address__state', 'user__address__street']

	def get_queryset(self):
		return ArtisanPortfolio.objects.all()

	@action(detail=False, methods=['GET', 'PUT', 'POST'])
	def profile(self, request):
		permission_classes = [IsAuthenticated]

		(artisan, created) = ArtisanPortfolio.objects.get_or_create(user_id=request.user.id)
		if request.method == 'GET': 
			serialized = ArtisanPortfolioSerializer(artisan)
			return Response(serialized.data)
		else:
			serialized = ArtisanPortfolioSerializer(artisan, data=request.data)
			serialized.is_valid(raise_exception=True)
			serialized.save()
			return Response(serialized.data)

	@action(detail=False, methods=['GET'])
	def search(self, request):
		queryset = self.queryset

		# Define a mapping of query parameters to model fields
		search_fields_mapping = {
			'title': 'job_title__icontains',
			'state': 'user__address__state__icontains',
			# Add more search criteria as needed
		}

		# Apply filters based on query parameters
		for query, model_field in search_fields_mapping.items():
			search_query = request.query_params.get(query, '')
			if search_query:
				queryset = queryset.filter(**{model_field: search_query})

		# Paginate the queryset
		paginated_queryset = self.paginate_queryset(queryset)

		serializer = self.serializer_class(paginated_queryset, many=True)
		return self.get_paginated_response(serializer.data)
