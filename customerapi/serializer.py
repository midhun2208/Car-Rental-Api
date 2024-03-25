from rest_framework import serializers
from adminapi.models import Customer,RentalVehicle,UsedVehicle,RentalTransactions,Report,Payment,VehiclePurchase,ReportResponse


class CustomerSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    password=serializers.CharField(write_only=True)
    is_available=serializers.CharField(read_only=True)

    class Meta:
        model=Customer
        fields=["id","username","firstname","lastname","phone","email_address","password","is_available"]

    def create(self, validated_data):
        return Customer.objects.create_user(**validated_data)
    
    
class RentalVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentalVehicle
        fields="__all__"
        
        
class UsedVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsedVehicle
        fields="__all__"
        
        
class RentalTransactionSerializer(serializers.ModelSerializer):
    totalcost=serializers.CharField(read_only=True)
    vehicle=serializers.CharField(read_only=True)
    
    class Meta:
        model = RentalTransactions
        fields=["id","rental_startdate","rental_enddate","totalcost","vehicle"]
        
        
class RentalTransactionListSerializer(serializers.ModelSerializer):
    totalcost=serializers.CharField(read_only=True)
    vehicle=RentalVehicleSerializer()
    class Meta:
        model = RentalTransactions
        fields=["id","rental_startdate","rental_enddate","totalcost","vehicle"]
        

class ReportSerializer(serializers.ModelSerializer):
    transaction=serializers.CharField(read_only=True)
    class Meta:
        model=Report
        fields="__all__"


class ReportResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model=ReportResponse
        fields="__all__"
        
        
class RentalPaymentSerializer(serializers.ModelSerializer):
    transaction=serializers.CharField(read_only=True)
    paymentamount=serializers.CharField(read_only=True)

    class Meta:
        model = Payment
        fields="__all__"
        
class VehiclePurchaseSerializer(serializers.ModelSerializer):
    vehicle=serializers.CharField(read_only=True)
    amount=serializers.CharField(read_only=True)
    class Meta:
        model = VehiclePurchase
        fields="__all__"


class VehiclePurchaseViewSerializer(serializers.ModelSerializer):
    vehicle=UsedVehicleSerializer()
    amount=serializers.CharField(read_only=True)
    class Meta:
        model = VehiclePurchase
        fields="__all__"