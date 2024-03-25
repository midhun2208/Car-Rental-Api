from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator,MaxValueValidator



class CustomUser(AbstractUser):
    user_type_choices=[
        ('Admin', 'Admin'),
        ('Customer' ,'Customer'),
    ]
    user_type=models.CharField(max_length=50,choices=user_type_choices,default='Customer')
    
    
class Admin(CustomUser):
    email_address=models.EmailField()
    

class Customer(CustomUser):
    firstname=models.CharField(max_length=100)
    lastname=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    email_address=models.EmailField()
    address=models.CharField(max_length=100)
    is_available=models.BooleanField(default=True)

    def __str__(self):
        return self.first_name
    

class RentalVehicle(models.Model):
    make=models.CharField(max_length=100)
    model=models.CharField(max_length=100)
    year=models.CharField(max_length=100)
    colour=models.CharField(max_length=100)
    reg_number=models.CharField(max_length=100)
    image=models.ImageField(upload_to="images",null=True)
    options=[
        ('Available', 'Available'),
        ('Not available', 'Not available'),
    ]
    rental_status=models.CharField(max_length=50,choices=options,default="Available")
    amountperhr=models.PositiveIntegerField(null=True)
    
    

class UsedVehicle(models.Model):
    make=models.CharField(max_length=100)
    model=models.CharField(max_length=100)
    type=models.CharField(max_length=100)
    transmission=models.CharField(max_length=100)
    year=models.CharField(max_length=100)
    colour=models.CharField(max_length=100)
    reg_number=models.CharField(max_length=100)
    image=models.ImageField(upload_to="images",null=True)
    description=models.CharField(max_length=100)
    amount=models.PositiveIntegerField()
    options=[
        ('Available', 'Available'),
        ('Sold', 'Sold'),
    ]
    vehicle_status=models.CharField(max_length=50,choices=options,default="Available")
    
    
class VehiclePurchase(models.Model):
    vehicle=models.ForeignKey(UsedVehicle,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,null=True)
    amount=models.PositiveIntegerField()
    purchase_date=models.DateField(auto_now_add=True)
    options=[
        ('cash', 'cash'),
        ('online', 'online'),
    ]
    purchase_method=models.CharField(max_length=50,choices=options,default="online")
    options=[
        ('pending', 'pending'),
        ('processing', 'processing'),
        ('failed', 'failed'),
        ('completed', 'completed'),
    ]
    purchase_status=models.CharField(max_length=50,choices=options,default="completed")
    
    

class RentalTransactions(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    vehicle=models.ForeignKey(RentalVehicle,on_delete=models.CASCADE)
    rental_startdate=models.DateTimeField()
    rental_enddate=models.DateTimeField()
    totalcost=models.PositiveIntegerField()
    
    
class Payment(models.Model):
    transaction=models.ForeignKey(RentalTransactions,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,null=True)
    paymentdate=models.DateField(auto_now_add=True)
    paymentamount=models.PositiveIntegerField()
    options=[
        ('cash', 'cash'),
        ('online', 'online'),
    ]
    payment_method=models.CharField(max_length=50,choices=options,default="online")
    options=[
        ('pending', 'pending'),
        ('processing', 'processing'),
        ('failed', 'failed'),
        ('completed', 'completed'),
    ]
    payment_status=models.CharField(max_length=50,choices=options,default="completed")
    
    @property
    def total_profit(self):
        rental_cost = self.transaction.totalcost if self.transaction else 0
        return rental_cost - self.paymentamount    

    
class Report(models.Model):
    transaction=models.ForeignKey(RentalTransactions,on_delete=models.CASCADE,unique=True)
    damage_image=models.ImageField(upload_to="images",null=True)
    description=models.CharField(max_length=100)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,null=True)
    date_reported=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.description

class ReportResponse(models.Model):
    report=models.ForeignKey(Report,on_delete=models.CASCADE,unique=True)
    amount=models.PositiveIntegerField()
    options=[
        ('No damage till now', 'No damage till now'),
        ('Damage req sent','Damage req sent'),
        ('Damage money pending', 'Damage money pending'),
        ('Damage solved', 'Damage solved'), 
    ]
    report_status=models.CharField(max_length=50,choices=options,default="No damage till now")
    date_reported=models.DateTimeField(auto_now_add=True)
    
    
class Feedback(models.Model):
    transaction=models.ForeignKey(RentalTransactions,on_delete=models.CASCADE)
    rating=models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    comment=models.CharField(max_length=300)
    date_submitted=models.DateField(auto_now_add=True)
    
    
class FeedbackResponse(models.Model):
    feedback=models.ForeignKey(Feedback,on_delete=models.CASCADE)
    comment=models.CharField(max_length=100)
    
    


    

    
    



    
