from django import forms
from .models import *
from django.contrib.admin.widgets import AdminDateWidget

class CategoiesForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = ('name', 'desc')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',  'size':55, 'maxlength':50}),
            'desc': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
        labels = {
            'name': 'ประเภทสินค้า',
            'desc': 'รายละเอียด',
        }
    def deleteForm(self):
        self.fields['name'].widget.attrs['readonly'] = True
        self.fields['desc'].widget.attrs['readonly'] = True


class ProductsForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ('pid', 'name', 'category', 'price', 'net', 'picture', )
        widgets = {
            'pid': forms.TextInput(attrs={'class': 'form-control',  'size':15, 'maxlength':13}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'size':55, 'maxlength':50}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'Min': 1}),
            'net': forms.NumberInput(attrs={'class': 'form-control', 'Min': 0}),
            'picture':forms.FileInput(attrs={'class': 'form-control', 'accept':'image/*'}),
        }
        labels = {
            'pid': 'รหัสสินค้า',
            'name': 'ชื่อสินค้า',
            'category': 'ประเภทสินค้า',
            'price': 'ราคาต่อหน่วย',
            'net': 'คงเหลือ',
            'picture': 'ภาพสินค้า',
        }

    def updateForm(self):
        self.fields['pid'].widget.attrs['readonly'] = True
        self.fields['pid'].label = 'รหัสสินค้า [ไม่อนุญาตให้แก้ไขได้]'

    def deleteForm(self):
        self.fields['pid'].widget.attrs['readonly'] = True
        self.fields['name'].widget.attrs['readonly'] = True
        self.fields['category'].widget.attrs['readonly'] = True
        self.fields['price'].widget.attrs['readonly'] = True
        self.fields['net'].widget.attrs['readonly'] = True
        self.fields['picture'].widget.attrs['readonly'] = True

class EmployeesForm(forms.ModelForm):
    class Meta:
        STATUS_CHOICES = (
            ("Manager", "Manager"),
            ("Employee", "Employee"),
            ("Store", "Store"),
        )
        model = Employees
        fields = ('eid', 'name', 'birthdate', 'position')
        widgets = {
            'eid': forms.TextInput(attrs={'class': 'form-control', 'size':15, 'maxlength':13}),
            'name': forms.TextInput(attrs={'class': 'form-control',  'size':55, 'maxlength':50}),
            'birthdate':forms.NumberInput(attrs={'class': 'form-control',   'type': 'date'}),
            'position': forms.Select(choices=STATUS_CHOICES, attrs={'class': 'form-control'}),
         }

        labels = {
            'eid': 'รหัสพนักงาน',
            'name': 'ชื่อพนักงาน',
            'birthdate': 'วันเดือนปีเกิด',
            'position': 'ตำแหน่ง',
         }

    def updateForm(self):
        self.fields['eid'].widget.attrs['readonly'] = True
        self.fields['eid'].label = 'รหัสพนักงาน [ไม่อนุญาตให้แก้ไขได้]'

    def deleteForm(self):
        self.fields['eid'].widget.attrs['readonly'] = True
        self.fields['name'].widget.attrs['readonly'] = True
        self.fields['birthdate'].widget.attrs['readonly'] = True
        self.fields['position'].widget.attrs['readonly'] = True

class CustomersForm(forms.ModelForm):
    class Meta:
        model = Customers
        fields = ('cid','name', 'address', 'tel',)
        widgets = {
            'cid': forms.TextInput(attrs={'class': 'form-control', 'size':15, 'maxlength':13}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'size':55, 'maxlength':50}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'tel': forms.TextInput(attrs={'class': 'form-control','size':13, 'maxlength':10}),

        }
        labels = {
            'cid': 'รหัสประจำตัว (User Name)',
            'name': 'ชื่อลูกค้า',
            'address': 'ที่อยู่',
            'tel': 'เบอร์โทรศัพท์',

         }

    def updateForm(self):
        self.fields['cid'].widget.attrs['readonly'] = True
        self.fields['cid'].label='รหัสประจำตัว (User Name) [ไม่อนุญาตให้แก้ไขได้]'

class ChangePasswordForm(forms.Form):
    userId = forms.CharField(label='รหัสประจำตัวผู้ใช้', max_length=50,
                             widget=forms.TextInput(attrs={'class':'form-control', 'readonly':True}))
    oldPassword = forms.CharField(label='รหัสผ่านเดิม', max_length=100, 
                                  widget=forms.PasswordInput(attrs={'class':'form-control'}))
    newPassword = forms.CharField(label='รหัสผ่านใหม่', max_length=100, 
                                  widget=forms.PasswordInput(attrs={'class':'form-control'}))
    confirmPassword = forms.CharField(label='ยืนยันรหัสผ่านใหม่',  max_length=100,
                                      widget=forms.PasswordInput(attrs={'class':'form-control'}))

class ResetPasswordForm(forms.Form):
    userId = forms.CharField(label='รหัสประจำตัวผู้ใช้', max_length=50,
                             widget=forms.TextInput(attrs={'class':'form-control', 'readonly':True}))
    newPassword = forms.CharField(label='รหัสผ่านใหม่', max_length=100,
                                  widget=forms.PasswordInput(attrs={'class':'form-control'}))
    confirmPassword = forms.CharField(label='ยืนยันรหัสผ่านใหม่',  max_length=100,
                                      widget=forms.PasswordInput(attrs={'class':'form-control'}))

class TranfersForm(forms.ModelForm):
    class Meta:
        model = Transfers
        fields = ('order','reference', 'bank', 'bill', 'comment')      
        widgets = {
            'order': forms.HiddenInput(attrs={'class': 'form-control'}),
            'reference': forms.TextInput(attrs={'class': 'form-control','size': 40, 'maxlength': 35}),
            'bank': forms.TextInput(attrs={'class': 'form-control','size': 55, 'maxlength': 50}),
            'bill': forms.FileInput(attrs={'class': 'form-control', 'accept':'image/*'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
        labels = {
            'order': 'ใบสั่งซื้อสินค้า',
            'reference': 'หมายเลขใบโอนเงิน',
            'bank': 'จากธนาคาร',
            'bill': 'ไฟล์สลิปใบโอน',
            'comment': 'หมายเหตุ ',
        }
    def setup(self):
        self.fields['comment'].required = False


class SendForm(forms.ModelForm):
    class Meta:
        model = Send
        fields = ('order','employee', 'company', 'tag', 'comment')
        widgets = {
            'order': forms.HiddenInput(attrs={'class': 'form-control'}),
            'employee': forms.HiddenInput(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control', 'size': 55, 'maxlength': 50}),
            'tag': forms.TextInput(attrs={'class': 'form-control', 'size': 55, 'maxlength': 50}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
        labels = {
            'order': 'ใบสั่งซื้อสินค้า',
            'employee': 'พนักงาน',
            'company': 'บริษัทขนส่ง',
            'tag': 'หมายเลขพัสดุ',
            'comment': 'หมายเหตุ',
        }

class CancelForm(forms.ModelForm):
    class Meta:
        model = Cancel
        fields = ('order','reason')
        widgets = {
            'order': forms.TextInput(attrs={'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
        labels = {
            'order': 'ใบสั่งซื้อสินค้า',
            'reason': 'เหตุผลในการยกเลิกใบสั่งซื้อ',
        }

class RejectForm(forms.ModelForm):
    class Meta:
        model = Reject
        fields = ('order','employee', 'reason')
        widgets = {
            'order': forms.HiddenInput(attrs={'class': 'form-control'}),
            'employee': forms.HiddenInput(attrs={'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
        labels = {
            'order': 'ใบสั่งซื้อสินค้า',
            'employee': 'พนักงาน',
            'reason': 'เหตุผลในการปฏิเสธการสั่งซื้อ',
        }
