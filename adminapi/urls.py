from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken
from adminapi import views
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register("rentalvehicles",views.RentalVehicleView,basename="rentalvehicles")
router.register("rentaltransactions",views.RentalTransactionsView,basename="rentaltransactionlist")
router.register("rentvehiclepayments",views.RentalPaymentView,basename="rentvehiclepayments")
router.register("usedvehicles",views.UsedVehicleView,basename="usedvehicles")
router.register("vehiclepurchase",views.CarSalePaymentView,basename="vehiclepurchase")
router.register("feedbacks",views.FeedBackView,basename="feedbacks")
router.register("reports",views.ReportView,basename="reports")
router.register("reportresponsestatus",views.ReportResponseView,basename="reportresponsestatus")


urlpatterns = [
    path("register/",views.AdminCreateView.as_view(),name="signup"),
    path("token/",ObtainAuthToken.as_view(),name="token"),

    
] +router.urls