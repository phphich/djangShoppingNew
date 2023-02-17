import datetime

from django.forms import modelformset_factory
from django.shortcuts import render,redirect,get_object_or_404, HttpResponse
from shoppingapp.forms import *
import datetime, os
from django.db.models import Q
from django.core.paginator import (Paginator, EmptyPage,PageNotAnInteger,)
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def chkPermission(request):
    if 'userStatus' in request.session:
        userStatus = request.session['userStatus']
        if userStatus == 'customer':
            messages.add_message(request, messages.WARNING, "ท่านกำลังเข้าใช้ในส่วนที่ไม่ได้รับอนุญาต!!!")
            return False
        else:
            return True
    else:
        if Employees.objects.count() != 0:
            return False
        else:
            return True

def home(request):
    countEmp = Employees.objects.count()
    print("countEmp:" + str(countEmp))
    if countEmp == 0:
        messages.add_message(request, messages.INFO, "เพิ่มข้อมูลพนักงาน สำหรับการเข้าใช้ครั้งแรก")
        return redirect('employeeNew')
    else:
        return render(request, 'home.html')

@login_required(login_url='userAuthen')
def categoryList(request):
    if not chkPermission(request):
        return redirect('home')
    categories = Categories.objects.all().order_by('id')
    context = {'categories':categories}
    return render(request, 'crud/categoryList.html', context)

@login_required(login_url='userAuthen')
def categoryNew(request):
    if not chkPermission(request):
        return redirect('home')
    if request.method == 'POST':
        form = CategoiesForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('categoryList')
        else:
            context = {'form': form}
            return render(request, 'crud/categoryNew.html', context)
    else:
        form = CategoiesForm()
        context = {'form': form}
        return render(request, 'crud/categoryNew.html', context)

@login_required(login_url='userAuthen')
def categoryUpdate(request, id):
    if not chkPermission(request):
        return redirect('home')
    category = get_object_or_404(Categories, id=id)
    form = CategoiesForm(data=request.POST or None, instance=category)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('categoryList')
        else:
            context = {'form':form}
            return render(request, 'crud/categoryUpdate.html')
    else:
        context = {'form':form}
        return render(request, 'crud/categoryUpdate.html', context)

@login_required(login_url='userAuthen')
def categoryDelete(request, id):
    if not chkPermission(request):
        return redirect('home')
    category = get_object_or_404(Categories, id=id)
    form = CategoiesForm(data=request.POST or None, instance=category)
    if request.method == 'POST':
        category.delete()
        return redirect('categoryList')
    else:
        form.deleteForm()
        context = {'form':form, 'category':category}
        return render(request, 'crud/categoryDelete.html', context)

@login_required(login_url='userAuthen')
def productList(request):
    if not chkPermission(request):
        return redirect('home')
    products = Products.objects.all().order_by('pid')
    context = {'products':products}
    return render(request, 'crud/productList.html', context)

@login_required(login_url='userAuthen')
def productListPage(request, pageNo):
    if not chkPermission(request):
        return redirect('home')
    # page = request.GET.get('page', page)
    items_per_page = 5
    products = Products.objects.all().order_by('pid')
    items_page = Paginator(products, items_per_page)
    context = {'products': items_page.page(pageNo)}
    return render(request, 'crud/productListPage.html', context)

@login_required(login_url='userAuthen')
def productNew(request):
    if not chkPermission(request):
        return redirect('home')
    if request.method == 'POST':
        form = ProductsForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            newForm = form.save(commit=False)
            pid = newForm.pid
            # filename = newForm.picture.name
            filepath = newForm.picture.name
            # point = filename.rfind('.')
            # ext = filename[point:]
            point = filepath.rfind('.')
            ext = filepath[point:]
            filenames = filepath.split('/')
            filename = filenames[len(filenames)-1]
            # filename = filename
            newfilename = pid + ext
            newForm.save() # product_tmp/xxx.xxx
            product = get_object_or_404(Products, pid=pid)
            product.picture.name = '/products/'+newfilename # pxxx.xxx
            product.save()

            # บนเซิร์ฟเวอร์ต้องเป็น djangShopping/static/products/'
            # if os.path.exists('static/products/' + newfilename):
            #     os.remove('static/products/' + newfilename)  # file exits, delete it
            # os.rename('products_tmp/'+filename, 'static/products/' + newfilename)
            if os.path.exists('static/products/' + newfilename):
                os.remove('static/products/' + newfilename)  # file exits, delete it
            os.rename('static/products/'+filename, 'static/products/' + newfilename)
        else:
            product = get_object_or_404(Products, pid=request.POST['pid'])
            if product:
                messages.add_message(request, messages.WARNING, "รหัสสินค้าซ้ำกับที่มีอยู่แล้วในระบบ")
                context = {'form': form}
                return render(request, 'crud/productNew.html', context)
        return redirect('productList')
    else:
        form = ProductsForm()
        context = {'form':form }
        return render(request, 'crud/productNew.html', context)

@login_required(login_url='userAuthen')
def productUpdate(request, pid):
    if not chkPermission(request):
        return redirect('home')
    product = get_object_or_404(Products, pid=pid)
    picture = product.picture.name  # รูปสินค้าเดิม
    # form = ProductsForm(request.POST or None, instance=product, files=request.FILES)
    if request.method == 'POST':
        form = ProductsForm(request.POST or None, instance=product, files=request.FILES)
        if form.is_valid():
            newForm = form.save(commit=False)
            pid = newForm.pid
            print(newForm.picture.name)
            if newForm.picture.name != picture: #  หากเลือกรูปสินค้าใหม่
                newForm.save()
                filepath = newForm.picture.name
                point = filepath.rfind('.')
                ext = filepath[point:]
                filenames = filepath.split('/')
                filename = filenames[len(filenames) - 1]
                newfilename = pid + ext
                # filename = newForm.picture.name
                # point = filename.rfind('.')
                # ext = filename[point:]
                newfilename =  pid + ext
                product = get_object_or_404(Products, pid=pid)
                product.picture.name = '/products/' +newfilename
                product.save()
                # บนเซิร์ฟเวอร์ต้องเป็น djangShopping/static/products/'
                if os.path.exists('static/products/' + newfilename): # file exits, delete it
                    os.remove('static/products/' +newfilename)
                os.rename('static/products/'+ filename, 'static/products/' +newfilename)
            else:
                newForm.save()
        return redirect('productList')
    else:
        # form = ProductsForm(request.POST or None, instance=product, files=request.FILES)
        form = ProductsForm(instance=product)
        form.updateForm()
        context = {'form': form}
        return render(request, 'crud/productUpdate.html', context)

@login_required(login_url='userAuthen')
def productDelete(request, pid):
    if not chkPermission(request):
        return redirect('home')
    product = get_object_or_404(Products, pid=pid)
    picture = product.picture.name  # รูปสินค้าเดิม
    if request.method == 'POST':
        product.delete()
        # บนเซิร์ฟเวอร์ต้องเป็น djangShopping/static/products/'
        # ใน table db เก็บ /products/xxx.xx
        if os.path.exists('static'+picture):  # file exits, delete it
            os.remove('static'+picture)
        return redirect('productList')
    else:
        form = ProductsForm(instance=product)
        form.deleteForm()
        context = {'form': form, 'product':product}
        return render(request, 'crud/productDelete.html', context)

@login_required(login_url='userAuthen')
def employeeList(request):
    if not chkPermission(request):
        return redirect('home')
    employees = Employees.objects.all().exclude(Q(position='Administrator')).order_by('eid')
    context = {'employees': employees}
    return render(request, 'crud/employeeList.html', context)

# @login_required(login_url='userAuthen')
def employeeNew(request):
    if not chkPermission(request):
        return redirect('home')
    if request.method == 'POST':
        form = EmployeesForm(request.POST)
        if form.is_valid():
            form.save()
            # สร้าง user ในระบบ authen ของ Django ---
            eid = request.POST['eid']
            name = request.POST['name']
            email = 'none@gmail.com'
            password = request.POST['password']
            user = User.objects.create_user(eid, email, password)
            user.first_name = name
            user.is_staff = True
            user.save()
            # -------
            return redirect('employeeList')
        else:
            context = {'form': form}
            return render(request, 'crud/employeeNew.html', context)
    else:
        form = EmployeesForm()
        context = {'form': form}
        return render(request, 'crud/employeeNew.html', context)

@login_required(login_url='userAuthen')
def employeeUpdate(request, eid):
    if not chkPermission(request):
        return redirect('home')
    employee = get_object_or_404(Employees, eid=eid)
    if request.method == 'POST':
        form = EmployeesForm(request.POST or None, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employeeList')
        else:
            context = {'form': form}
            return render(request, 'crud/employeeUpdate.html', context)
    else:
        form = EmployeesForm(instance=employee)
        form.updateForm()
        context = {'form': form,}
        return render(request, 'crud/employeeUpdate.html', context)

def employeeDelete(request, eid):
    if not chkPermission(request):
        return redirect('home')
    employee = get_object_or_404(Employees, eid=eid)
    if request.method == 'POST':
        employee.delete()
        return redirect('employeeList')
    else:
        form = EmployeesForm(instance=employee)
        form.deleteForm()
        context = {'form': form, 'employee': employee}
        return render(request, 'crud/employeeDelete.html', context)

@login_required(login_url='userAuthen')
def customerList(request):
    if not chkPermission(request):
        return redirect('home')
    customers = Customers.objects.all().order_by('cid')
    context = {'customers':customers}
    return render(request, 'crud/customerList.html', context)

from django.contrib.auth.models import User
def customerRegistration(request):
    if request.method == 'POST':
        form = CustomersForm(request.POST)
        if form.is_valid():
            password = request.POST['password']
            confirmPassword = request.POST['confirmPassword']
            if password == confirmPassword:
                form.save()
                # สร้าง user ในระบบ authen ของ Django ---
                cid = request.POST['cid']
                name = request.POST['name']
                email = 'none@gmail.com'
                password = request.POST['password']
                user = User.objects.create_user(cid, email, password)
                user.first_name = name
                user.is_staff = False
                user.save()
                # -------
                return redirect('userAuthen')
            else:
                messages.add_message(request, messages.WARNING, "รหัสผ่านกับรหัสผ่านที่ยืนยันไม่ตรงกัน...")
                context = {'form': form}
                return render(request, 'crud/customerRegister.html', context)
        else:
            messages.add_message(request, messages.WARNING, "ป้อนข้อมูลไม่ถูกต้อง ไม่สมบูรณ์...")
            context = {'form': form}
            return render(request, 'crud/customerRegister.html', context)
    else:
        form = CustomersForm()
        context = {'form': form}
        return render(request, 'crud/customerRegister.html', context)

@login_required(login_url='userAuthen')
def customerUpdate(request, cid):
    customer = get_object_or_404(Customers, cid=cid)
    if request.method == 'POST':
        form = CustomersForm(request.POST or None, instance=customer)
        if form.is_valid():
            form.save()
            if request.session.get('userStatus') == 'customer':
                return redirect('home')
            else:
                return redirect('customerList')
        else:
            context = {'form': form}
            return render(request, 'crud/customerUpdate.html', context)
    else:
        form = CustomersForm(instance=customer)
        form.updateForm()
        context = {'form': form}
        return render(request, 'crud/customerUpdate.html', context)

#อัพเดทรหัสผ่านในระบบ Authen ของ Django
@login_required(login_url='userAuthen')
def userChangePassword(request):
    userId = request.session.get('userId')
    user = None
    if request.method == 'POST':
        form=ChangePasswordForm(request.POST or None)
        # if request.session.get('userStatus') == 'customer':
        #     user = get_object_or_404(Customers, cid=userId)
        # else:
        #     user = get_object_or_404(Employees, eid=userId)
        context = {'form': form}
        u = authenticate(username=userId, password=request.POST['oldPassword'])
        if u:
            if request.POST['newPassword'] == request.POST['confirmPassword']:
                u.set_password(request.POST['newPassword'])
                u.save()
                messages.add_message(request, messages.INFO, "เปลี่ยนรหัสผ่านเสร็จเรียบร้อย...")
                return redirect('home')

        # if request.POST['oldPassword'] == user.password:
        #     if request.POST['newPassword'] == request.POST['confirmPassword']:
        #         user.password = request.POST['newPassword']
        #         user.save()
        #         messages.add_message(request, messages.INFO, "เปลี่ยนรหัสผ่านเสร็จเรียบร้อย...")
        #         return redirect('home')
            else:
                messages.add_message(request, messages.WARNING, "รหัสผ่านใหม่กับรหัสที่ยืนยันไม่ตรงกัน...")
                return render(request, 'userChangePassword.html', context)
        else:
            messages.add_message(request, messages.ERROR, "รหัสผ่านเดิมที่ระบุไม่ถูกต้อง...")
            return render(request, 'userChangePassword.html', context)
    else:
        form=ChangePasswordForm(initial={'userId':userId})
        context ={'form':form}
        return render(request, 'userChangePassword.html', context)

def userResetPassword(request, userId):
    if not chkPermission(request):
        return redirect('home')
    user = None
    if request.method == 'POST':
        form=ResetPasswordForm(request.POST or None)
        context = {'form': form}
        if request.POST['newPassword'] == request.POST['confirmPassword']:
            #อัพเดทรหัสผ่าน ในระบบ authen ของ django
            user = User.objects.filter(username=userId).first()
            newPassword = request.POST['newPassword']
            user.set_password(newPassword)
            user.save()
            messages.add_message(request, messages.INFO, "เปลี่ยนรหัสผ่านเสร็จเรียบร้อย...")
            return redirect('home')

        # if request.session.get('userStatus') == 'customer':
        #     user = get_object_or_404(Customers, cid=userId)
        # else:
        #     user = get_object_or_404(Employees, eid=userId)
        # context = {'form': form}
        # if request.POST['newPassword'] == request.POST['confirmPassword']:
        #     user.password = request.POST['newPassword']
        #     user.save()
        #     messages.add_message(request, messages.INFO, "เปลี่ยนรหัสผ่านเสร็จเรียบร้อย...")
        #     return redirect('home')
        else:
            messages.add_message(request, messages.WARNING, "รหัสผ่านใหม่กับรหัสที่ยืนยันไม่ตรงกัน...")
            return render(request, 'userResetPassword.html', context)
    else:
        form=ResetPasswordForm(initial={'userId':userId})
        context ={'form':form}
        return render(request, 'userResetPassword.html', context)

def userAuthen(request):
    if request.method == 'POST':
        userName = request.POST.get("userName")
        userPass = request.POST.get("userPass")

        ## login ด้วย ระบบล็อกอินของ Django
        user = authenticate(username=userName, password=userPass)
        if user is not None:
            login(request, user)
            if user.is_staff == 0:
                user = Customers.objects.get(cid=userName)
                request.session['userId'] = user.cid
                request.session['userName'] = user.name
                request.session['userStatus'] = 'customer'
            else:
                emp = Employees.objects.get(eid=userName)
                request.session['userId'] = emp.eid
                request.session['userName'] = emp.name
                request.session['userStatus'] = emp.position
            messages.add_message(request, messages.INFO, "Login success..")
            if request.session.get('orderActive'):
                del request.session['orderActive']
                return redirect('checkout')
            else:
                return redirect('home')
        else:
            messages.error(request, "User Name or Password not correct..!!!")
            data = {'userName': userName}
            return render(request, 'userAuthen.html', data)
    #     user = Customers.objects.filter(cid=userName).filter(password=userPass).first()
    #     if user:
    #         request.session['userId'] = user.cid
    #         request.session['userName'] = user.name
    #         request.session['userStatus'] = 'customer'
    #         # messages.add_message(request, messages.INFO, "Login success..")
    #         if request.session.get('orderActive'):
    #             del request.session['orderActive']
    #             return redirect('checkout')
    #         else:
    #             return redirect('home')
    #     else:
    #         user = Employees.objects.filter(eid=userName).filter(password=userPass).first()
    #         if user:
    #             request.session['userId'] = user.eid
    #             request.session['userName'] = user.name
    #             request.session['userStatus'] = user.position
    #             # messages.add_message(request, messages.INFO, "Login success..")
    #             return redirect('home')
    #         else:
    #             messages.add_message(request, messages.ERROR, "User or Password not Correct!!!..")
    #             data={'userName':userName}
    #             return render(request, 'userAuthen.html', data)
    else:
         data = {'userName': ''}
         return render(request, 'userAuthen.html', data)

#ล็อกเอ๊าท์ผ่านระบบ Authen ของ Django
# @login_required(login_url='userAuthen')
def userLogout(request):
    del request.session["userId"]
    del request.session["userName"]
    del request.session["userStatus"]
    logout(request)
    return  redirect('home')

def productShop(request):
    if request.method == 'POST':
        pid = request.POST.get('pid')
        qnt = int(request.POST.get('qnt'))
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(pid)
            if quantity:
                cart[pid] = quantity + qnt
            else:
                cart[pid] = qnt
        else:
            cart = {}
            cart[pid] = qnt
        request.session['cart'] = cart
        request.session['count'] = len(cart)
        return redirect('productShop')
    else:
        products = Products.objects.all().order_by('pid')
        data = {'products':products}
        return render(request, 'productShop.html', data)

def showBasket(request):
    cart = request.session.get('cart')
    if request.method == 'POST':
        action = request.POST.get('action')
        pid = request.POST.get('pid')
        qnt = int(request.POST.get('qnt'))
        if action=="Update": #กดปุ่ม Update
            if cart[pid]:
                cart[pid] = qnt
        else: # กดปุ่มลบ
            del cart[pid]
        request.session['cart'] = cart
        request.session['count'] = len(cart)
    if len(cart) == 0:
        del request.session['cart']
        del request.session['count']
        del request.session['sum']
        return redirect('productShop')

    cart = request.session.get('cart')
    items = []
    sum=0.00
    for item in cart:
        product = Products.objects.get(pid=item)
        total=product.price * cart[item]
        sum+=total
        items.append({'product':product, 'quantity':cart[item], 'total':total})
    request.session['sum'] = sum
    data={'items':items}
    return render(request, 'showBasket.html',data)

@login_required(login_url='userAuthen')
def checkout(request):
    cart = request.session.get('cart')
    items = []
    sum = 0.00
    if cart:
        if not request.session.get('userId'):
            request.session['orderActive'] = True
            return redirect('userAuthen')
        cart = request.session.get('cart')
        date = datetime.datetime.now()
        # print("date:", date)
        customer = get_object_or_404(Customers, cid=request.session.get('userId'))
        order = Orders()
        order.odate = date.strftime('%Y-%m-%d %H:%M:%S')
        order.customer = customer
        for item in cart:
            # print(item, cart[item])
            product = Products.objects.get(pid=item)
            total=product.price * cart[item]
            sum+=total
            items.append({'product':product, 'quantity':cart[item], 'total':total})
        request.session['sum'] = sum
        data={'items':items, 'order':order}
        return render(request, 'checkout.html', data)
    else:
        messages.add_message(request, messages.WARNING, "No product in basket!!!..")
        return redirect('productShop')

@login_required(login_url='userAuthen')
def order(request):
    cart = request.session.get('cart')
    if cart is None:
        return redirect('productShop')
    items = []
    date = datetime.datetime.now()
    customer = get_object_or_404(Customers, cid=request.session.get('userId'))
    order = Orders()
    order.newOrderId()
    order.odate = date.strftime('%Y-%m-%d %H:%M:%S')
    order.customer = customer
    order.status = "1"
    order.save()
    for item in cart:  # get any key from cart
        product = Products.objects.get(pid=item)
        quantity = cart[item]
        total = product.price * cart[item]
        orderDetail = OrderDetails()
        orderDetail.order = order
        orderDetail.product=product
        orderDetail.oprice=product.price
        orderDetail.quantity = quantity
        orderDetail.save()
        items.append({'product': product, 'quantity': cart[item], 'total': total})
    count = request.session.get('count')
    sum = request.session.get('sum')
    data = {'items': items, 'order': order, 'count':count, 'sum':sum}
    del request.session['cart']
    del request.session['count']
    del request.session['sum']
    return render(request, 'summary.html', data)

@login_required(login_url='userAuthen')
def clearBasket(request):
    del request.session['cart']
    del request.session['count']
    del request.session['sum']
    return redirect('productShop')


def showAllOrder(request):
    orders = []
    if request.session.get("userStatus")=='customer':
        customer = get_object_or_404(Customers, cid=request.session.get('userId'))
        orders = None
        if customer:
            orders = Orders.objects.filter(customer=customer).order_by('odate').reverse()
        context = {'customer':customer, 'orders':orders}
        return render(request, 'showAllOrder.html', context)
    else: #employee
        orders = Orders.objects.filter(~Q(status='5')).exclude(status='6').exclude(status='7').order_by('odate').reverse() #อ่านใบสั่งซื้อที่ status 1-4
        context = {'orders': orders}
        return render(request, 'showAllOrder.html', context)

def showOrderDetail(request, oid):
    order = get_object_or_404(Orders, oid=oid)
    if request.method == 'POST':
        return redirect('home')
    else:
        context = {'order': order}
        return render(request, 'showOrderDetail.html', context)

@login_required(login_url='userAuthen')
def showHistoryOrder(request):
    orders = []
    orders = Orders.objects.filter(Q(status ='6') | Q(status='7') |Q(status='8'))
    context = {'orders': orders}
    return render(request, 'showHistoryOrder.html', context)

@login_required(login_url='userAuthen')
def orderConfirm(request, oid):
    order = get_object_or_404(Orders, oid=oid)
    employee = get_object_or_404(Employees, eid=request.session.get('userId'))
    confirm = Confirms()
    confirm.order = order
    confirm.employee = employee
    confirm.save()
    order.status = '2'
    order.save()
    return redirect('showAllOrder')

@login_required(login_url='userAuthen')
def moneyTransfer(request, oid):
    order = get_object_or_404(Orders, oid=oid)
    form = TranfersForm(request.POST or None, files=request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            order.status='3'
            order.save()
        return redirect('showAllOrder')
    else:
        form = TranfersForm(initial={'order':order})
        form.setup()
        context = {'form':form, 'order':order }
        return render(request, 'moneyTransfer.html', context)

@login_required(login_url='userAuthen')
def moneyAccept(request,oid):
    order = get_object_or_404(Orders, oid=oid)
    employee = get_object_or_404(Employees, eid=request.session.get('userId'))
    accept = Accepts()
    accept.order = order
    accept.employee = employee
    accept.save()
    order.status = '4'
    order.save()
    return redirect('showAllOrder')

@login_required(login_url='userAuthen')
def productSend(request, oid):
    order = get_object_or_404(Orders, oid=oid)
    employee = get_object_or_404(Employees, eid=request.session.get("userId"))
    form = SendForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            order.status = '5'
            order.save()
        return redirect('showAllOrder')
    else:
        form = SendForm(initial={'order': order, 'employee':employee})
        context = {'form': form, 'order': order}
        return render(request, 'productSend.html', context)

@login_required(login_url='userAuthen')
def orderCancel(request, oid):
    order = get_object_or_404(Orders, oid=oid)
    form = CancelForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            order.status = '6'
            order.save()
        return redirect('showAllOrder')
    else:
        form = CancelForm(initial={'order': order})
        context = {'form': form, 'order': order}
        return render(request, 'orderCancel.html', context)

@login_required(login_url='userAuthen')
def orderReject(request, oid):
    order = get_object_or_404(Orders, oid=oid)
    employee = get_object_or_404(Employees, eid=request.session.get("userId"))
    form = RejectForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            order.status = '7'
            order.save()
        return redirect('showAllOrder')
    else:
        form = RejectForm(initial={'order': order, 'employee': employee})
        context = {'form': form, 'order': order}
        return render(request, 'orderReject.html', context)

@login_required(login_url='userAuthen')
def testDateTimeStamp(request):
    # -- datetime to timestamp --
    dt = datetime.datetime.now()
    ts = dt.timestamp()
    # -- timestamp to datetime --
    db = datetime.datetime.fromtimestamp(ts, tz=None).strftime("%d-%m-%Y")
    return HttpResponse("date now: "+ str(dt)+  ", time stamp: "+ str(ts)+ " date back: "+ str(db)+", type timestamp: " )

#before coding install requests: pip install requests
import requests, json
def sendNotify(message):
    url = "https://notify-api.line.me/api/notify"
    LINE_ACCESS_TOKEN = "Lbk3vjzgD7fi9iicQKlxm0yciMwB4zlnR8i2J6pw41x"  # token from your line notify web
    LINE_HEADERS = {'Content-Type': 'application/x-www-form-urlencoded', "Authorization": "Bearer " + LINE_ACCESS_TOKEN}
    return requests.post(url, headers=LINE_HEADERS, data=message)

def sendLineMessage(request):
    sMessage = "Django Message for You"  # ข้อความที่ต้องการส่ง
    sendNotify(sMessage)
    messages.add_message(request, messages.INFO, "Send Message to Line Notify was Successfully.")
    return redirect('home')

def sendLineSticker(request):
    sSticker = {'message':'Sticker', 'stickerPackageId':789, 'stickerId':10855}
    sendNotify(sSticker)
    messages.add_message(request, messages.INFO, "Send Sticker to Line Notify was Successfully.")
    return redirect('home')

def sendLineImage(request):
    fileUrlThumb="https://media.geeksforgeeks.org/wp-content/cdn-uploads/20200221235734/Django-tutorial-learn-.png"
    fileUrlFull="https://media.geeksforgeeks.org/wp-content/cdn-uploads/20200221235734/Django-tutorial-learn-.png"
    sFile = {'message':'File', 'imageThumbnail':fileUrlThumb, 'imageFullsize':fileUrlFull}
    sendNotify(sFile)
    messages.add_message(request, messages.INFO, "Send Image to Line Notify was Successfully.")
    return redirect('home')

from xhtml2pdf import pisa
from io import BytesIO
from django.template.loader import get_template
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def pdfThaiReport(request):
    pdfmetrics.registerFont(TTFont('THSarabunNew', 'thsarabunnew-webfont.ttf'))
    template = get_template('pdfThaiReport.html')
    context = {"Name" : "อาจารย์พิชญะภาคย์  พิพิธพัฒน์ไพสิฐ"}
    html = template.render(context)
    response = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
    if not pdf.err:
        return HttpResponse(response.getvalue(), content_type='application/pdf')
    else:
        return HttpResponse("<h1><b>เกิดข้อผิดพลาด!!!</b> ไม่สามารถสร้างเอกสาร PDF ได้...</h2>", status=400)

def pdfProductReport(request):
    pdfmetrics.registerFont(TTFont('THSarabunNew', 'thsarabunnew-webfont.ttf'))
    pdfmetrics.registerFont(TTFont('THSarabunNew-Bold', 'thsarabunnew_bold-webfont.ttf'))
    template = get_template('pdfProductReport.html')
    products=Products.objects.all()
    context = {"products": products}
    html = template.render(context)
    response = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
    if not pdf.err:
        return HttpResponse(response.getvalue(), content_type='application/pdf')
    else:
        return HttpResponse("<h1><b>เกิดข้อผิดพลาด!!!</b> ไม่สามารถสร้างเอกสาร PDF ได้...</h2>", status=400)

# pip install plotly
# #pip install pandas
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px

def dashboardBarGraph(request):
    productsAll = Products.objects.all()
    products = []
    amounts = []
    for item in productsAll:
        products.append(item.name)
        amounts.append(item.getSaleAmount())
    # กรณีอ่านค่าจากบางฟิลด์ใน model มาใช้งาน
    # products = Products.objects.values_list('name', 'samplesale__amount')
    # df = pd.DataFrame(products,  columns=['Product', 'Amount'])
    df = pd.DataFrame({"Product":products, "Amount":amounts}, columns=['Product', 'Amount'])
    fig = px.bar(df, x='Product', y='Amount', title="แผนภูมิแท่งแสดงยอดขายแยกตามรายชื่อสินค้า")
    fig.update_layout(autosize = False, width = 600,  height = 400,
                      margin = dict(l=10, r=10, b=100, t=100, pad=5 ),
                      paper_bgcolor = "aliceblue",)
    chart = fig.to_html()
    context = {'chart':chart}
    return render(request, "dashboard.html", context)

def dashboardPieGraph(request):
    productsAll = Products.objects.all()
    products = []
    amounts = []
    for item in productsAll:
        products.append(item.name)
        amounts.append(item.getSaleAmount())
    df = pd.DataFrame({"Product": products, "Amount": amounts}, columns=['Product', 'Amount'])
    fig = px.pie(df, hole=.3, names='Product', values ='Amount', title="แผนภูมิวงกลมแสดงยอดขายแยกตามรายชื่อสินค้า")
    fig.update_layout(autosize=False, width=600, height=400,
                      margin = dict(l=10, r=10, b=100, t=100, pad=5 ),
                      paper_bgcolor = "aliceblue",)
    chart = fig.to_html()
    context = {'chart':chart}
    return render(request, 'dashboard.html', context)

def dashboardLineChart(request):
    saleAll = Samplesale.objects.all().order_by('datesale')
    sales = {}
    for sale in saleAll:
        preiod = str(sale.datesale.month) + "-" + str(sale.datesale.year)
        if preiod in sales.keys():
            sales[preiod] += sale.amount
        else:
            sales[preiod] = sale.amount
    df = pd.DataFrame({"Month_Year":sales.keys(), "Amount":sales.values()}, columns=['Month_Year', 'Amount'])
    fig = px.line(df, x='Month_Year', y='Amount',  title='กราฟเส้นแสดงยอดขายแยกตามเดือน-ปี')
    fig.update_layout(autosize = False, width = 600,  height = 400,
                      margin = dict(l=10, r=10, b=100, t=100, pad=5),
                      paper_bgcolor = "aliceblue",)
    chart = fig.to_html()
    context = {'chart':chart}
    return render(request, "dashboard.html", context)

def dashboardAreaChart(request):
    saleAll = Samplesale.objects.all().order_by('datesale')
    sales = {}
    for sale in saleAll:
        preiod = str(sale.datesale.month) + "-" + str(sale.datesale.year)
        if preiod in sales.keys():
            sales[preiod] += sale.amount
        else:
            sales[preiod] = sale.amount
    df = pd.DataFrame({"Month_Year": sales.keys(), "Amount": sales.values()}, columns=['Month_Year', 'Amount'])
    fig = px.area(df, x='Month_Year', y='Amount', title='กราฟพื้นที่แสดงยอดขายแยกตามเดือน-ปี')
    fig.update_layout(autosize=False, width=600, height=400,
                      margin = dict(l=10, r=10, b=100, t=100, pad=5),
                      paper_bgcolor = "aliceblue",)
    chart = fig.to_html()
    context = {'chart': chart}
    return render(request, "dashboard.html", context)

def dashboardAll(request):
    productsAll = Products.objects.all()
    products = []
    amounts = []
    productCount = len(productsAll)
    totalSale=0.00
    for item in productsAll:
        products.append(item.name)
        amounts.append(item.getSaleAmount())
        totalSale += item.getSaleAmount()
    df_product = pd.DataFrame({"Product": products, "Amount": amounts}, columns=['Product', 'Amount'])
    fig_bar = px.bar(df_product, x='Product', y='Amount', title="แผนภูมิแท่งแสดงยอดขายแยกตามรายชื่อสินค้า")
    fig_bar.update_layout(autosize=False, width=430, height=400,
                          margin=dict(l=10, r=10, b=100, t=100, pad=5),
                          paper_bgcolor="aliceblue", )
    chart_bar = fig_bar.to_html()

    fig_pie = px.pie(df_product, hole=.3, names='Product', values='Amount', title="แผนภูมิวงกลมแสดงยอดขายแยกตามรายชื่อสินค้า")
    fig_pie.update_layout(autosize=False, width=430, height=400,
                          margin=dict(l=10, r=10, b=100, t=100, pad=5),
                          paper_bgcolor="aliceblue", )
    chart_pie = fig_pie.to_html()

    saleAll = Samplesale.objects.all().order_by('datesale')
    sales = {}
    for sale in saleAll:
        preiod = str(sale.datesale.month) + "-" + str(sale.datesale.year)
        if preiod in sales.keys():
            sales[preiod] += sale.amount
        else:
            sales[preiod] = sale.amount
    df_sale = pd.DataFrame({"Month_Year": sales.keys(), "Amount": sales.values()}, columns=['Month_Year', 'Amount'])
    fig_line = px.line(df_sale, x='Month_Year', y='Amount', title='กราฟเส้นแสดงยอดขายแยกตามเดือน-ปี')
    fig_line.update_layout(autosize=False, width=430, height=400,
                           margin=dict(l=10, r=10, b=100, t=100, pad=5),
                           paper_bgcolor="aliceblue", )
    chart_line = fig_line.to_html()
    fig_area = px.area(df_sale, x='Month_Year', y='Amount', title='กราฟพื้นที่แสดงยอดขายแยกตามเดือน-ปี')
    fig_area.update_layout(autosize=False, width=430, height=400,
                           margin=dict(l=10, r=10, b=100, t=100, pad=5),
                           paper_bgcolor="aliceblue", )
    chart_area = fig_area.to_html()
    context = {'chart_bar': chart_bar, 'chart_pie': chart_pie,
               'chart_line':chart_line, 'chart_area':chart_area,
               "productCount":productCount, "totalSale":totalSale}
    return render(request, 'dashboardMultiple.html', context)