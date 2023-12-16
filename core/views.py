from django.conf import settings
from django.db.models.aggregates import Avg
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
# from rest_framework.pagination import Paginator
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import viewsets
from .models import (
	Customer, ArtisanCategory, ArtisanPortfolio, 
	Address, Customer_profile_photo, Ratings, Reviews
)
from .pagination import DefaultPagination
from .serializers import (
	CustomerSerializer, ArtisanCategorySerializer, ArtisanPortfolioSerializer, 
	AddressSerializer, ArtisanUserIdSerializer, Profile_photo_serializer,
	ArtisanRatingSerializer, ArtisanReviewSerializer
)

class CustomerViewSet(
	CreateModelMixin, RetrieveModelMixin, 
	UpdateModelMixin, GenericViewSet
):
	queryset = Customer.objects.all()
	serializer_class = CustomerSerializer
	permission_classes = [IsAuthenticated]

	@action(detail=False, methods=['GET', 'PUT', 'PATCH'])
	def me(self, request):

		(customer, created) = Customer.objects.get_or_create(user_id=request.user.id)
		serialized = CustomerSerializer(customer)
		if request.method == 'PUT':
			customer.user.first_name = request.data['first_name']
			customer.user.last_name = request.data['last_name']
			customer.user.username = request.data['username']
		if request.method == 'PATCH':
			customer.user.membership = request.data['membership']
		if request.method in ['PATCH', 'PUT']:
			customer.user.save() 
			serialized = CustomerSerializer(customer, data=request.data)
			serialized.is_valid(raise_exception=True)
			serialized.save()
	
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
			unique_streets = []
			streets = Address.objects.all()
			serialized = AddressSerializer(streets, many=True)

			for item in serialized.data:
				street = item['street']
				unique_streets.add(street.lower())

			street_data = list(unique_streets)
			return Response(street_data)

	@action(detail=False, methods=['GET'])
	def cities(self, request):
			cities = set()
			cities = Address.objects.all()
			serialized = AddressSerializer(cities, many=True)

			for item in serialized.data:
				city = item['city']
				cities.add(city.lower())
			city_data = list(cities)
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
		return self.queryset.filter(user__membership='A')

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
			'city': 'user__address__city__icontains',
			'street': 'user__address__street__icontains',
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

	@action(detail=True, methods=['GET'])
	def verify(self, request, pk=None):
		artisan = ArtisanPortfolio.objects.get(pk=pk)
		isVerified = artisan.user_id == request.user.id
		return Response(isVerified)

	@action(detail=True, methods=['GET'])
	def info(self, request, pk=None):
		try:
			artisan = ArtisanPortfolio.objects.get(pk=pk)
			serialized_artisan = ArtisanPortfolioSerializer(artisan)

			customer_info = Customer.objects.get(user_id=artisan.user_id)
			serialized_customer = CustomerSerializer(customer_info)

			return Response(
				{
					"email": artisan.user.email, 
					**serialized_artisan.data,
					**serialized_customer.data
				}
			)
		except (ArtisanPortfolio.DoesNotExist, Customer.DoesNotExist):
			return Response({'error': 'Artisan not found'}, status='404')


class ProfilePhotoViewSet(viewsets.ModelViewSet):
	serializer_class = Profile_photo_serializer
	queryset = Customer_profile_photo.objects.all()
	
	@action(detail=False, methods=['GET', 'POST'])
	def photo(self, request):
		try:
			customer = Customer.objects.get(user_id=request.user.id)
			(customer, created) = Customer_profile_photo.objects.get_or_create(customer_id=customer.id)
			if request.method == 'GET':
				serialized = Profile_photo_serializer(customer)
				return Response(serialized.data)
			else: 
				serialized = Profile_photo_serializer(customer, data=request.data)
				serialized.is_valid(raise_exception=True)
				serialized.save()
				return Response({
					'message': 'Photo uploaded successfully',
					'photo': serialized.data['photo']
				}, status='201')
			# Return a response
		except ( Customer.DoesNotExist, Customer_profile_photo.DoesNotExist):
			return Response({'message': 'failed to upload image'})


class ArtisanRatingViewset(viewsets.ModelViewSet):
	queryset = Ratings.objects.all()
	serializer_class = ArtisanRatingSerializer

	def list(self, request, *args, **kwargs):
		artisans = ArtisanPortfolio.objects.all()
		artisan_ratings = []

		for artisan in artisans:
			avg_rating = Ratings.objects.filter(artisan_id=artisan.id).aggregate(average_rating=Avg('rating'))
			avg_rating_value = avg_rating['average_rating'] or 0

			artisan_ratings.append({
				'artisan_id': artisan.id,
				'artisan_name': artisan.user.get_full_name(),
				'average_rating': avg_rating_value,
			})

		return Response(artisan_ratings)
		
	@action(detail=False, methods=['GET', 'POST'])
	def user(self, request):
		try:
			artisan = ArtisanPortfolio.objects.get(user_id=request.user.id)
			user_ratings = Ratings.objects.filter(artisan_id=artisan.id).aggregate(average_ratings=Avg('rating'))
			return Response(user_ratings)
		except (ArtisanPortfolio.DoesNotExist, Ratings.DoesNotExist):
			return Response({'average_ratings': 0})

	@action(detail=False, methods=['POST'])
	def add_rating(self, request):
		customer = Customer.objects.get(user_id=request.user.id)
		artisan_id = request.data['artisan_id']
		artisan = ArtisanPortfolio.objects.get(id=artisan_id)
		(artisan_rating, created) = Ratings.objects.get_or_create(artisan=artisan, customer=customer, rating=request.data['rating'])

		data = {
			"customer_id": customer.id,
			**request.data
		}

		serialized = ArtisanRatingSerializer(artisan_rating, data)
		serialized.is_valid(raise_exception=True)
		serialized.save()
		return Response("OK")

	
class ArtisanReviewViewset(viewsets.ModelViewSet):
	queryset = Reviews.objects.all()
	serializer_class = ArtisanReviewSerializer
		
	@action(detail=False, methods=['GET'])
	def artisan(self, request):
		pass

	@action(detail=False, methods=['POST'])
	def add_review(self, request):
		customer = Customer.objects.get(user_id=request.user.id)
		artisan_id = request.data['artisan_id']
		artisan = ArtisanPortfolio.objects.get(id=artisan_id)
		(artisan_review, created) = Reviews.objects.get_or_create(artisan=artisan, customer=customer)
		data = {
			"customer_id": customer.id,
			**request.data
		}

		serialized = ArtisanReviewSerializer(artisan_review, data)
		serialized.is_valid(raise_exception=True)
		serialized.save()
		return Response('OK')
		