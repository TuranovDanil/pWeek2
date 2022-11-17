from django.contrib import admin
from .forms import RequestForm
from .models import AbsUser
from .models import Request
from .models import Category


# Register your models here.
class RequestAdmin(admin.ModelAdmin):
    form = RequestForm
    list_filter = ('status',)
    list_display = ('name', 'status', 'category', 'date',)
    fields = ('status', 'photo2', 'comment')


admin.site.register(Request, RequestAdmin)
# admin.site.register(AbsUser)
admin.site.register(Category)
