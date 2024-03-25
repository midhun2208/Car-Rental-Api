from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet,ViewSet
from rest_framework.decorators import action
from rest_framework import authentication
from rest_framework import permissions
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404


from adminapi.models import Customer,RentalVehicle,UsedVehicle,RentalTransactions,Report,Payment,VehiclePurchase,ReportResponse
from customerapi.serializer import CustomerSerializer,RentalVehicleSerializer,UsedVehicleSerializer,RentalTransactionSerializer,ReportSerializer,VehiclePurchaseSerializer,RentalPaymentSerializer,ReportResponseSerializer,RentalTransactionListSerializer,VehiclePurchaseViewSerializer


class CustomerCreateView(APIView):
    def post(self,request,*args,**kwargs):
        serializer=CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_type="Customer")
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        

class RentalVehicleView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def list(self,request,*args,**kwargs):
        qs=RentalVehicle.objects.filter(rental_status="Available")
        serializer=RentalVehicleSerializer(qs,many=True)
        return Response(data=serializer.data)

    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=RentalVehicle.objects.get(id=id)
        serializer=RentalVehicleSerializer(qs)
        return Response(data=serializer.data)
    
    
    @action(methods=["post"],detail=True)
    def rental_transaction(self,request,*args,**kwargs):
        serializer=RentalTransactionSerializer(data=request.data)
        if serializer.is_valid():
            customer_obj=request.user.customer
            vehicle_id=kwargs.get("pk")
            vehicle_obj=RentalVehicle.objects.get(id=vehicle_id)
            
            rental_start = serializer.validated_data['rental_startdate']
            rental_end = serializer.validated_data['rental_enddate']
            rental_duration_hours = (rental_end - rental_start).total_seconds() / 3600
            if rental_duration_hours <= 0:
                return Response(data={'error': 'Invalid rental duration'})
            total_cost = rental_duration_hours * vehicle_obj.amountperhr
    
            if serializer.is_valid():
                vehicle_obj.rental_status="Not available"
                vehicle_obj.save()
                serializer.save(vehicle=vehicle_obj,customer=customer_obj,totalcost=total_cost)
                response_data = serializer.data
                response_data['vehicle'] = {
                    'make': vehicle_obj.make,
                    'model': vehicle_obj.model,
                    'year': vehicle_obj.year,
                    'colour': vehicle_obj.colour,
                    'reg_number': vehicle_obj.reg_number,
                    'image': str(vehicle_obj.image),
                }
                return Response(response_data)
            else:
                return Response(data=serializer.errors)
        else:
            return Response(data=serializer.errors)
        
        
class RentalPaymentView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    # def list(self, request, *args, **kwargs):
    #     customer_obj = request.user.customer
    #     qs = RentalTransactions.objects.filter(customer=customer_obj)
    #     serializer = RentalTransactionListSerializer(qs, context={'request': request}, many=True)
    #     data = serializer.data
        
    #     for transaction_data in data:
    #         transaction_id = transaction_data['id']

    #         report_response = ReportResponse.objects.filter(report__transaction_id=transaction_id).first()
    #         if report_response:
    #             transaction_data['Response_detail'] = {
    #                 'id': report_response.id,
    #                 'amount': report_response.amount,
    #                 'report_status': report_response.report_status,
    #                 'date_reported': report_response.date_reported
    #             }
    #         else:
    #             transaction_data['Response_detail'] = None
    #     return Response(data)
    
    
    # def retrieve(self,request,*args,**kwargs):
    #     id=kwargs.get("pk")
    #     qs=RentalTransactions.objects.get(id=id)
    #     serializer = RentalTransactionListSerializer(qs, context={'request': request})
    #     transaction_data = serializer.data
        
    #     transaction_id = transaction_data['id']
    #     report_response = ReportResponse.objects.filter(report__transaction_id=transaction_id).first()
    #     if report_response:
    #         transaction_data['Response_detail'] = {
    #             'id': report_response.id,
    #             'amount': report_response.amount,
    #             'report_status': report_response.report_status,
    #             'date_reported': report_response.date_reported
    #         }
    #     else:
    #         transaction_data['Response_detail'] = None
    #     return Response(transaction_data)
    


    def list(self, request, *args, **kwargs):
        customer_obj = request.user.customer
        qs = RentalTransactions.objects.filter(customer=customer_obj)
        serializer = RentalTransactionListSerializer(qs, many=True)
        
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
            serializer = RentalTransactionListSerializer(rental_transaction)
            
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

    
    



        
    @action(methods=["post"],detail=True)
    def report_add(self,request,*args,**kwargs):
        serializer=ReportSerializer(data=request.data)
        customer=request.user.id
        customer_obj=Customer.objects.get(id=customer)
        transaction_id=kwargs.get("pk")
        transaction_obj=RentalTransactions.objects.get(id=transaction_id)
        if serializer.is_valid():
            serializer.save(transaction=transaction_obj,customer=customer_obj)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        
    
    @action(methods=["post"],detail=True)
    def rental_payment(self,request,*args,**kwargs):
        serializer=RentalPaymentSerializer(data=request.data)
        customer=request.user.customer
        transaction_id=kwargs.get("pk")
        transaction_obj=RentalTransactions.objects.get(id=transaction_id)
        total_amount = transaction_obj.totalcost
        if serializer.is_valid():
            serializer.save(transaction=transaction_obj,paymentamount=total_amount,customer=customer)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
    
    
    

class UsedVehicleView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def list(self,request,*args,**kwargs):
        qs=UsedVehicle.objects.filter(vehicle_status="Available")
        serializer=UsedVehicleSerializer(qs,many=True)
        return Response(data=serializer.data)

    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=UsedVehicle.objects.get(id=id)
        serializer=UsedVehicleSerializer(qs)
        return Response(data=serializer.data)
    
    @action(methods=["post"],detail=True)
    def vehicle_payment(self,request,*args,**kwargs):
        serializer=VehiclePurchaseSerializer(data=request.data)
        customer=request.user.customer
        vehicle_id=kwargs.get("pk")
        vehicle_obj=UsedVehicle.objects.get(id=vehicle_id)
        amount=vehicle_obj.amount
        if serializer.is_valid():
            vehicle_obj.vehicle_status="Sold"
            vehicle_obj.save()
            serializer.save(vehicle=vehicle_obj,amount=amount,customer=customer)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        



class vehiclepurchaseView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def list(self,request,*args,**kwargs):
        customer_obj=request.user.customer
        qs=VehiclePurchase.objects.filter(customer=customer_obj)
        serializer=VehiclePurchaseViewSerializer(qs,many=True)
        return Response(data=serializer.data)


class ReportResponseView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
        customer_obj = request.user.customer
        report_responses = ReportResponse.objects.filter(report__customer=customer_obj)
        serializer = ReportResponseSerializer(report_responses, many=True)
        return Response(serializer.data)

    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=ReportResponse.objects.get(id=id)
        serializer=ReportResponseSerializer(qs)
        return Response(data=serializer.data)
    
    @action(detail=True, methods=["post"])
    def report_pay(self, request, *args, **kwargs):
        reportresponse_id = kwargs.get("pk")
        reportresponse_obj = ReportResponse.objects.get(id=reportresponse_id)
        reportresponse_obj.report_status = "No damage till now"
        reportresponse_obj.save()
        
        report_id = reportresponse_obj.report.id
        rental_report = Report.objects.get(id=report_id)
        rental_report.delete()
        
        serializer = ReportResponseSerializer(reportresponse_obj)
        return Response(serializer.data)


