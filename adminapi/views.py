from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import authentication
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet,ViewSet
from rest_framework import status
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404




from adminapi.serializer import AdminSerializer,RentalTransactionSerializer,UsedVehicleSerializer,RentalVehicleSerializer,FeedbackSerializer,ReportSerializer,CustomerSerializer,FeedBackResponseSerializer\
                                ,RentalPaymentSerializer,VehiclePurchaseSerializer,ReportResponseSerializer,ReportstatusSerializer
from adminapi.models import Admin,RentalVehicle,Feedback,Report,Customer,Payment,UsedVehicle,VehiclePurchase,RentalTransactions,ReportResponse




class AdminCreateView(APIView):
    def post(self,request,*args,**kwargs):
        serializer=AdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_type="Admin",is_superuser=True)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        
        
class RentalVehicleView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def create(self,request,*args,**kwargs):
        serializer=RentalVehicleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
    
    def list(self,request,*args,**kwargs):
        qs=RentalVehicle.objects.all()
        serializer=RentalVehicleSerializer(qs,many=True)
        data=serializer.data
        car_count=RentalVehicle.objects.count()
        data_with_count={'car_count': car_count, 'vehicles': data}
        return Response(data=data_with_count)
    
    def update(self,request,*args,**kwargs): 
        id=kwargs.get("pk")
        obj=RentalVehicle.objects.get(id=id)
        serializer=RentalVehicleSerializer(data=request.data,instance=obj)
        if request.user.admin:
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data)
            else:
                return Response(data=serializer.errors)
        else:
            return Response(data={"message":"permission denied"})
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=RentalVehicle.objects.get(id=id)
        serializer=RentalVehicleSerializer(qs)
        return Response(data=serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        try:
            instance = RentalVehicle.objects.get(id=id)
            instance.delete()
            return Response({"msg": "Vehicle removed"})
        except RentalVehicle.DoesNotExist:
            return Response({"msg": "Vehicle not found"}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=True, methods=["post"])
    def make_active(self, request, *args, **kwargs):
        id = kwargs.get("pk")     
        rentvehicle_obj = RentalVehicle.objects.get(id=id)
        rentvehicle_obj.rental_status = "Available"
        rentvehicle_obj.save()
        serializer = RentalVehicleSerializer(rentvehicle_obj)
        return Response(serializer.data)
    
        
class UsedVehicleView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def create(self,request,*args,**kwargs):
        serializer=UsedVehicleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
    
    def list(self,request,*args,**kwargs):
        qs=UsedVehicle.objects.filter(vehicle_status="Available")
        serializer=UsedVehicleSerializer(qs,many=True)
        data=serializer.data
        car_count=UsedVehicle.objects.count()
        data_with_count={'car_count': car_count, 'vehicles': data}
        return Response(data=data_with_count)
    
    def update(self,request,*args,**kwargs): 
        id=kwargs.get("pk")
        obj=UsedVehicle.objects.get(id=id)
        serializer=UsedVehicleSerializer(data=request.data,instance=obj)
        if request.user.admin:
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data)
            else:
                return Response(data=serializer.errors)
        else:
            return Response(data={"message":"permission denied"})
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=UsedVehicle.objects.get(id=id)
        serializer=UsedVehicleSerializer(qs)
        return Response(data=serializer.data)

    def destroy(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        try:
            instance = UsedVehicle.objects.get(id=id)
            instance.delete()
            return Response({"msg": "Vehicle removed"})
        except UsedVehicle.DoesNotExist:
            return Response({"msg": "Vehicle not found"}, status=status.HTTP_404_NOT_FOUND)
        
  
class CustomerView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def list(self,request,*args,**kwargs):
        qs=Customer.objects.all()
        serializer=CustomerSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Customer.objects.get(id=id)
        serializer=CustomerSerializer(qs)
        return Response(data=serializer.data)
        

class ReportView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def list(self,request,*args,**kwargs):
        qs=Report.objects.all()
        serializer=ReportSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Report.objects.get(id=id)
        serializer=ReportSerializer(qs)
        return Response(data=serializer.data)
    
    
    @action(methods=["post"],detail=True)
    def report_response(self,request,*args,**kwargs):
        serializer=ReportResponseSerializer(data=request.data)
        report_id=kwargs.get("pk")
        report_obj=Report.objects.get(id=report_id)
        if serializer.is_valid():
            amount=int(request.data.get('amount'))
            if amount>0:
                status="Damage req sent"
            else:
                status="No damage till now"
            serializer.save(report=report_obj,report_status=status)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        

class ReportResponseView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def list(self,request,*args,**kwargs):
        qs=ReportResponse.objects.exclude(report_status="No damage till now")
        serializer=ReportstatusSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    
class RentalTransactionsView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def list(self,request,*args,**kwargs):
        transactions=RentalTransactions.objects.all()
        data=[]
        for trans in transactions:
            transaction_data={
                'id':trans.id,
                'rental_startdate':trans.rental_startdate,
                'rental_enddate':trans.rental_enddate,
                'totalcost':trans.totalcost,
                'customer':{
                    'customer_name':trans.customer.firstname,
                    'phone':trans.customer.phone
                },
                'vehicle':{
                    'vehicle_regno':trans.vehicle.reg_number
                }
                
            }
            data.append(transaction_data)
        return Response(data)
    
    
        

class RentalPaymentView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
        qs = RentalTransactions.objects.all()
        serializer = RentalTransactionSerializer(qs, many=True)
        
        for data_item in serializer.data:
            transaction_id = data_item['id']
            report = Report.objects.filter(transaction_id=transaction_id).first()
            if report:
                report_serializer = ReportSerializer(report)
                data_item['rental_report'] = report_serializer.data
            else:
                data_item['rental_report'] = None
                
            response=ReportResponse.objects.filter(report__transaction_id=transaction_id).first()
            if response:
                response_serializer = ReportResponseSerializer(response)
                data_item['rental_response'] =response_serializer.data
            else:
                data_item['rental_response'] = None

        return Response(data=serializer.data)
    

    def retrieve(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        try:
            rental_transaction = RentalTransactions.objects.get(id=id)
            serializer = RentalTransactionSerializer(rental_transaction)
            
            data_item = serializer.data
            transaction_id = data_item['id']
            
            report = Report.objects.filter(transaction_id=transaction_id).first()
            if report:
                report_serializer = ReportSerializer(report)
                data_item['rental_report'] = report_serializer.data
            else:
                data_item['rental_report'] = None
                
            response = ReportResponse.objects.filter(report__transaction_id=transaction_id).first()
            if response:
                response_serializer = ReportResponseSerializer(response)
                data_item['rental_response'] = response_serializer.data
            else:
                data_item['rental_response'] = None

            return Response(data=data_item)
        except RentalTransactions.DoesNotExist:
            return Response({"error": "Rental transaction not found"}, status=404)


    
    
    

class CarSalePaymentView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def list(self,request,*args,**kwargs):
        vehiclepurchases=VehiclePurchase.objects.all()
        data=[]
        for purchase in vehiclepurchases:
            purchase_data={
                'id':purchase.id,
                'amount':purchase.amount,
                'purchase_date':purchase.purchase_date,
                'purchase_method':purchase.purchase_method,
                'purchase_status':purchase.purchase_status,
                'vehicle':{
                    'model':purchase.vehicle.model,
                    'reg_number':purchase.vehicle.reg_number
                },
                'customer':{
                    'customer_name':purchase.customer.firstname,
                    'phone':purchase.customer.phone,
                    'address':purchase.customer.address
                }
            }
            data.append(purchase_data)
        return Response(data)


        
class FeedBackView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def list(self,request,*args,**kwargs):
        qs=Feedback.objects.all()
        serializer=FeedbackSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    @action(methods=["post"],detail=True)
    def feedback_response(self,request,*args,**kwargs):
        serializer=FeedBackResponseSerializer(data=request.data)
        feedback_id=kwargs.get("pk")
        feedback_obj=Feedback.objects.get(id=feedback_id)
        if serializer.is_valid():
            serializer.save(feedback=feedback_obj)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)


