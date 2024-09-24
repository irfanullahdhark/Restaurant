from django import forms
from admin_site.models import Customer, PostComments, CustomerReview, AddToCart, OrderAddress
import re
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.contrib.auth.forms import UserCreationForm


class AddToCartForm(forms.ModelForm):
    class Meta:
        model = AddToCart
        fields = ['quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'value': 1, 'min': 1, 'max': 10, 'name': "quantity"})
        }


class CustomerReviewForm(forms.ModelForm):
    class Meta:
        model = CustomerReview
        fields = ['comment']

        widgets={
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Message', 'rows': 8, 'name': 'comment'})
        }


class ContactForm(forms.Form):
    email = forms.EmailField(max_length=164,widget=forms.EmailInput(attrs={"class":"form-control","name":'email','placeholder':"Email",'required':True}),error_messages={'required': "please enter your email."})
    subject = forms.CharField(max_length=500, widget=forms.TextInput(attrs={"class":"form-control","name":'subject','placeholder':"Subject",'required':True}),error_messages={"required":'please enter your subject.'})
    phone = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control","name":'phone','placeholder':"Phone",'required':True}),error_messages={'required': "please enter your phone NO."})
    
    message = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control",'placeholder':'Message','name':'message','required':True}), error_messages={'required': "please enter your message."})

    field_order = ['email','subject','phone','message']


class PostCommentsForm(forms.ModelForm):
    class Meta:
        model = PostComments
        fields = ['message']

        widgets={
            'message': forms.Textarea(attrs={'class':"form-control", 'name': 'message', 'placeholder': 'write your message here', 'rows':5})
        }

        error_messages = {
            'message': {
                'required': 'please enter your message before leaving message.'
            }
        }


class CustomerAuthentication(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={"class": 'form-control', 'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", 'autocomplete': 'current-password'}))


class CustomerForm(UserCreationForm):
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Confirm Password*'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password*'}))
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email*'}))

    class Meta:
        model = Customer
        fields = ['first_name','username','email','phone','password1','password2','photo']

        widgets = {
            'first_name' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Name*','required':True}),
            'username' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username*'}),
            'phone': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Phone*'}),
            'photo' : forms.ClearableFileInput(attrs={'class':'form-control', 'placeholder':'Photo*'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        print(f' cleanded:  {cleaned_data}')

        phone = cleaned_data.get('phone')

        if phone:
            pattern = r'07[98764320][0-9]{7}'
            result = re.match(pattern, str(phone))
            if result and len(phone) == 10:
                print('matched')
            else:
                self.add_error('phone', 'this is not afghanistan phone no.')

        return cleaned_data

    def exclude_fields(self, excluded_fields):
        for field_name in excluded_fields:
            if field_name in self.fields:
                self.fields.pop(field_name)


class OrderAddressForm(forms.ModelForm):
    class Meta:
        model = OrderAddress
        fields = ['area','street','shop_home','address','phone','order_note']

        widgets = {
            'area': forms.TextInput(attrs={'class': 'form-control', 'required': True,'readonly':True}),
            'street': forms.TextInput(attrs={'class': 'form-control'}),
            'shop_home': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'order_note': forms.Textarea(attrs={'class': 'form-control','rows':5}),
        }

        labels = {
            'area':'Area*',
            'street':'Street*',
            'shop_home':'Shop/Home No*',
            'address':'More Explain Address',
            'phone':'Phone No*',
            'order_note':'Order Note',
        }

    def clean(self):
        cleaned_data = super().clean()
        print(f' cleanded:  {cleaned_data}')

        phone = cleaned_data.get('phone')

        if phone:
            pattern = r'07[98764320][0-9]{7}'
            result = re.match(pattern, str(phone))
            if result and len(phone) == 10:
                print('matched')
            else:
                self.add_error('phone', 'this is not afghanistan phone no.')

        return cleaned_data


class AddressAreaForm(forms.ModelForm):
    class Meta:
        model = OrderAddress
        fields = ['area']

        widgets = {
            'area': forms.Select(attrs={'class': 'form-control'}),
        }


class AddressUpdateForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput,required=True)

    class Meta:
        model = OrderAddress
        fields = ['id','phone', 'area', 'street', 'shop_home', 'address','current_address']
        widgets = {
            'phone': forms.TextInput(attrs={'style':'border-width:0px;'}),
            'area': forms.TextInput(attrs={'readonly':True, 'class':"text-muted",'style':'border-width:0px;'}),
            'street': forms.TextInput(attrs={'style':'border-width:0px;'}),
            'shop_home': forms.TextInput(attrs={'style':'border-width:0px;'}),
            'address': forms.Textarea(attrs={'class':"form-control",'style':'border-width:0px;','rows':2}),

        }
        labels = {
            'phone':'Phone No',
            'Area': 'Area',
            'street': 'Street',
            'shop_home': 'Shop/Home No',
            'address': 'Address',
            'current_address': 'Use As Current Address'
        }

        def clean(self):
            cleaned_data = super().clean()
            print(f' cleanded:  {cleaned_data}------------------------------')

            phone = cleaned_data.get('phone')

            if phone:
                pattern = r'07[98764320][0-9]{7}'
                result = re.match(pattern, str(phone))
                if result and len(phone) == 10:
                    print('matched')
                else:
                    self.add_error('phone', 'this is not afghanistan phone no.')

            return cleaned_data
