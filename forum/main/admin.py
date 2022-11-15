from django.contrib import admin
from .models import AbsUser
from .models import Request
from .models import Category
# Register your models here.
admin.site.register(AbsUser)
admin.site.register(Request)
admin.site.register(Category)
