from django.contrib import admin

# Register your models here.
from .models import CustomUser, PatientRecord

admin.site.register(CustomUser)
admin.site.register(PatientRecord)