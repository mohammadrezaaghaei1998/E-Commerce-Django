from django import forms
from .models import UserInfo,Payment



class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        exclude = [ 'user','cart_item']


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        # fields = '__all__'
        exclude = [ 'userinfo']






   



 





