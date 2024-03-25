from rest_framework import serializers
from adminapi.models import Admin,Customer,RentalVehicle,UsedVehicle,RentalTransactions,Report,Feedback,VehiclePurchase,FeedbackResponse,Payment,ReportResponse


class AdminSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    password=serializers.CharField(write_only=True)

    class Meta:
        model=Admin
        fields=["id","username","email_address","password"]

    def create(self, validated_data):
        return Admin.objects.create_user(**validated_data)
    

class RentalVehicleSerializer(serializers.ModelSerializer):

    class Meta:
        model = RentalVehicle
        fields="__all__"

        
        
class UsedVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model=UsedVehicle
        fields="__all__"
        
        
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Customer
        fields=["id","username","firstname","lastname","phone","email_address"]
        
        
class RentalPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Payment
        fields="__all__"
        
        
class VehiclePurchaseSerializer(serializers.ModelSerializer):
    customer=CustomerSerializer()
    vehicle=RentalVehicleSerializer()
    class Meta:
        model=VehiclePurchase
        fields="__all__"
        

class RentalTransactionSerializer(serializers.ModelSerializer):
    customer=CustomerSerializer()
    vehicle=RentalVehicleSerializer()
    class Meta:
        model=RentalTransactions
        fields="__all__"
        

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model=Report
        fields="__all__"


class ReportResponseSerializer(serializers.ModelSerializer):
    report=serializers.CharField(read_only=True)
    class Meta:
        model=ReportResponse
        fields="__all__"


class ReportstatusSerializer(serializers.ModelSerializer):
    report=ReportSerializer()
    class Meta:
        model=ReportResponse
        fields="__all__"
        
        
class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model=Feedback
        fields="__all__"
        

class FeedBackResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model=FeedbackResponse
        fields="__all__"