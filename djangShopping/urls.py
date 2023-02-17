from shoppingapp import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),

    path('categoryList', views.categoryList, name='categoryList'),
    path('categoryNew', views.categoryNew, name='categoryNew'),
    path('<id>/categoryUpdate', views.categoryUpdate, name='categoryUpdate'),
    path('<id>/categoryDelete', views.categoryDelete, name='categoryDelete'),

    path('productList', views.productList, name='productList'),
    path('<pageNo>/productListPage', views.productListPage, name='productListPage'),
    path('productNew', views.productNew, name='productNew'),
    path('<pid>/productUpdate', views.productUpdate, name='productUpdate'),
    path('<pid>/productDelete', views.productDelete, name='productDelete'),

    path('employeeList', views.employeeList, name='employeeList'),
    path('employeeNew', views.employeeNew, name='employeeNew'),
    path('<eid>/employeeUpdate', views.employeeUpdate, name='employeeUpdate'),
    path('<eid>/employeeDelete', views.employeeDelete, name='employeeDelete'),

    path('customerList', views.customerList, name='customerList'),
    path('customerRegister', views.customerRegistration, name='customerRegistration'),
    path('<cid>/customerUpdate', views.customerUpdate, name='customerUpdate'),


    path('userAuthen', views.userAuthen, name='userAuthen'),
    path('userLogout', views.userLogout, name='userLogout'),
    path('userChangePassword', views.userChangePassword, name='userChangePassword'),
    path('<userId>/userResetPassword', views.userResetPassword, name='userResetPassword'),

    path('productShop', views.productShop, name='productShop'),
    path('showBasket', views.showBasket, name='showBasket'),
    path('checkout', views.checkout, name='checkout'),
    path('order', views.order,name='order'),
    path('clearBasket', views.clearBasket, name='clearBasket'),

    path('showAllOrder', views.showAllOrder, name='showAllOrder'),
    path('showHistoryOrder', views.showHistoryOrder, name='showHistoryOrder'),
    path('<oid>/showOrderDetail', views.showOrderDetail, name='showOrderDetail'),
    path('<oid>/orderConfirm', views.orderConfirm, name='orderConfirm'),
    path('<oid>/moneyTransfer', views.moneyTransfer, name='moneyTransfer'),
    path('<oid>/moneyAccept', views.moneyAccept, name='moneyAccept'),
    path('<oid>/productSend', views.productSend, name='productSend'),
    path('<oid>/orderCancel', views.orderCancel, name='orderCancel'),
    path('<oid>/orderReject', views.orderReject, name='orderReject'),

    path('dtstamp', views.testDateTimeStamp, name='dtstamp'),
    # sample Line Notify
    path('sendLineMessage', views.sendLineMessage, name='sendLineMessage'),
    path('sendLineSticker', views.sendLineSticker, name='sendLineSticker'),
    path('sendLineImage', views.sendLineImage, name='sendLineImage'),
    #sample Generate Thai PDF Report
    path('pdfThaiReport', views.pdfThaiReport, name='pdfThaiReport'),
    path('pdfProductReport', views.pdfProductReport, name='pdfProductReport'),
    #sample Dashboard Chart
    path('dashboardBarGraph', views.dashboardBarGraph, name='dashboardBarGraph'),
    path('dashboardPieGraph', views.dashboardPieGraph, name='dashboardPieGraph'), path('dashboardBarGraph', views.dashboardBarGraph, name='dashboardBarGraph'),
    path('dashboardLineChart', views.dashboardLineChart, name='dashboardLineChart'),
    path('dashboardAreaChart', views.dashboardAreaChart, name='dashboardAreaChart'),
    path('dashboardAll', views.dashboardAll, name='dashboardAll'),


]
