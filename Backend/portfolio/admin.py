from django.contrib import admin
from .models import User,Portfolio,Stock,Alert
# Register your models here.
admin.site.register(User)
admin.site.register(Portfolio)
# admin.site.register(Asset)
admin.site.register(Stock)
admin.site.register(Alert)