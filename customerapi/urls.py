from django.urls import path
from customerapi import views
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static


router=DefaultRouter()
router.register("rentalvehicles",views.RentalVehicleView,basename="rentalvehicles")
router.register("usedvehicles",views.UsedVehicleView,basename="usedvehicles")
router.register("vehiclepurchases",views.vehiclepurchaseView,basename="vehiclepurchaseView")
router.register("rentaltransactions",views.RentalPaymentView,basename="rentaltransactions")
router.register("reportresponse",views.ReportResponseView,basename="reportresponse")


urlpatterns = [
    
    path("register/",views.CustomerCreateView.as_view(),name="signup"),
    path("token/",ObtainAuthToken.as_view(),name="token"),
]+ router.urls