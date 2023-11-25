from django.contrib import admin
from .models import Customer


# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
	list_display = ['first_name', 'last_name', 'membership']
	ordering = ['user__first_name', 'user__last_name']
	# list_editable = ['membership']
	list_per_page = 10
	list_select_related = ['user']
	search_fields = ['user__first_name__istartswith']

