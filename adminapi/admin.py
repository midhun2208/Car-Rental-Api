from django.contrib import admin
from adminapi.models import RentalVehicle,VehiclePurchase,Payment,Report,UsedVehicle,RentalTransactions,ReportResponse

# Register your models here.

admin.site.register(UsedVehicle)
admin.site.register(RentalTransactions)
admin.site.register(Report)
admin.site.register(ReportResponse)
admin.site.register(Payment)
admin.site.register(RentalVehicle)


