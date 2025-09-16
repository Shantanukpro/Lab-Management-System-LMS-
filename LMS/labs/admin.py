from django.contrib import admin
from .models import Role, UserAccount, Lab, PC, MaintenanceRequest, Booking, ClassPeriod, PCAvailability

# Register your models here.

admin.site.register(Role)
admin.site.register(UserAccount)
admin.site.register(Lab)
admin.site.register(PC)
admin.site.register(MaintenanceRequest)
admin.site.register(Booking)
admin.site.register(ClassPeriod)
admin.site.register(PCAvailability)
