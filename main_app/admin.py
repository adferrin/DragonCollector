from django.contrib import admin

# Register your models here.
from .models import Dragon, Toy, Feeding

admin.site.register(Dragon)
admin.site.register(Toy)
admin.site.register(Feeding)