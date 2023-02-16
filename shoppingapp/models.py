import datetime
from django.db import models
from django.utils import timezone
from django.db.models import F, Sum, Count

class Categories(models.Model):
    name = models.CharField(max_length=50, default="")
    desc = models.TextField(max_length=400, default="")
    def __str__(self):
        return str(self.id) + ":" + self.name
    def getCountProduct(self):
        count = Products.objects.filter(category=self).aggregate(count=Count('pid'))
        return count['count']
    def getCountProducts(self):
        categories = Categories.objects.annotate(number_of_product=Count('product'))

class Products(models.Model):
    pid = models.CharField(max_length=13, primary_key=True, default="")
    name = models.CharField(max_length=50, default="")
    price=models.FloatField(default=0.00)
    net = models.IntegerField(default=0)
    picture = models.ImageField(upload_to ='static/products/', default="")
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, default=None)
    def __str__(self):
        return self.pid + ":" + self.name + ", " + str(self.price)
    def getCountOrder(self):
        count = OrderDetails.objects.filter(product=self).aggregate(count=Count('id'))
        return count['count']
    def getSaleAmount(self):
        amount = Samplesale.objects.filter(product=self).aggregate(amount=Sum(F('amount')))
        return amount['amount']

class Employees(models.Model):
    eid = models.CharField(max_length=13, primary_key=True, default="")
    name = models.CharField(max_length=50, default="")
    birthdate = models.DateField(default=None)
    position = models.CharField(max_length=50, default="")
    def __str__(self):
        return self.eid + ":" + self.name + ", " + self.position
    def getCountConfirm(self): #ยืนยัน Order
        count = Confirms.objects.filter(employee=self).aggregate(count=Count('id'))
        return count['count']
    def getCountAccept(self): #ยืนยันการโอนเงิน
        count = Accepts.objects.filter(employee=self).aggregate(count=Count('id'))
        return count['count']
    def getCountSend(self): #การส่งสินค้า
        count = Send.objects.filter(employee=self).aggregate(count=Count('id'))
        return count['count']


class Customers(models.Model):
    cid = models.CharField(max_length=13, primary_key=True, default="")
    name = models.CharField(max_length=50, default="")
    address = models.TextField(max_length=400, default="")
    tel = models.CharField(max_length=20, default="")
    def __str__(self):
        return self.cid + ":" + self.name + ", " + self.tel

class Orders(models.Model):
    oid = models.CharField(max_length=13, primary_key=True, default="")
    odate = models.DateTimeField(auto_now_add = True)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE, default=None)
    status = models.CharField(max_length=1, default="")
    def __str__(self):
        return self.oid + " " + str(self.odate.strftime("%Y-%m-%d")) + " : " + self.customer.name + ", " + str(self.getTotal()) + ", "+  self.getStatus()

    def newOrderId(self):
        #OD-yymm-xxxxx  ===> OD-2302-00001
        yy = str(datetime.date.today().strftime('%y'))
        mm = str(datetime.date.today().strftime('%m'))
        lastOrder = Orders.objects.last()
        if lastOrder:
            lastId = int(lastOrder.oid[9:])
        else:
            lastId = 0
        id = str(lastId+1)
        id=id.zfill(5)
        newId  = "OD-"+ yy + mm + "-" + id
        self.oid = newId

    def getStatus(self):
        if self.status == '1':
            return 'Wait for Confirm'
        elif self.status == '2':
            return 'Wait for Money Transfer'
        elif self.status == '3':
            return 'Wait for Money Accept'
        elif self.status == '4':
            return 'Wait for Product Send'
        elif self.status == '5':
            return 'C o m p l e t e'
        elif self.status == '6':
            return 'Order Cancel'
        elif self.status == '7':
            return 'Order Reject'

    def getOrderDetails(self):
        orderDetails = OrderDetails.objects.filter(order=self)
        return orderDetails

    def getTotal(self):
        total=OrderDetails.objects.filter(order=self).aggregate(total=Sum(F('oprice') * F('quantity')))
        return total['total']

    def getCount(self):
        count= OrderDetails.objects.filter(order=self).aggregate(count=Count('id'))
        return count['count']

class OrderDetails(models.Model):
    order=models.ForeignKey(Orders, on_delete=models.CASCADE, default=None)
    product=models.ForeignKey(Products, on_delete=models.CASCADE, default=None)
    oprice = models.FloatField(default=0.00)
    quantity=models.IntegerField(default=1)
    def __str__(self):
        return self.order.oid + " : " + self.product.pid + " " + self.product.name + ", " + str(self.quantity)
    def getTotal(self):
        return self.oprice * self.quantity

class Confirms(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, default=None)
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE, default=None)
    cdate = models.DateTimeField(auto_now_add = True)
    comment = models.CharField(max_length=200, default="")

class Transfers(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, default=None)
    tdate = models.DateTimeField(auto_now_add = True)
    reference = models.CharField(max_length=35, default="")
    bank = models.CharField(max_length=50, default="")
    bill = models.ImageField(upload_to ='static/bills/', default="")
    comment = models.CharField(max_length=200, default="")

class Accepts(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, default=None)
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE, default=None)
    adate =models.DateTimeField(auto_now_add = True)
    comment = models.CharField(max_length=200, default="")

class Send(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, default=None)
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE, default=None)
    sdate = models.DateTimeField(auto_now_add = True)
    company = models.CharField(max_length=50, default="")
    tag = models.CharField(max_length=50, default="")
    comment = models.CharField(max_length=200, default="")

class Cancel(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, default=None)
    cdate = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=200, default="")

class Reject(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, default=None)
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE, default=None)
    rdate = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=200, default="")

class Samplesale(models.Model): # ตารางสมมุติ เอาไว้เก็บยอดขาย เพื่อเอาไปทำ Dashboard
    product = models.ForeignKey(Products, on_delete=models.CASCADE, default=None)
    datesale = models.DateField(default=None)
    amount = models.IntegerField(default=0)  #ยอดขาย

    def __str__(self):
        return "Hey: " + str(self.id) + ":" + self.product.name + ", " + str(self.datesale.year) + ", " + str(self.amount)















