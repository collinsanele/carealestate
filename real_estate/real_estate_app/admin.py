from django.contrib import admin
from .models import Listing, Realtor, Contact

# Register your models here.
admin.site.register(Listing)
admin.site.register(Realtor)
admin.site.register(Contact)
