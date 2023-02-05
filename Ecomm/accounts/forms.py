from django import forms
from . models import Account,UserProfile


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
       'placeholder': 'Enter Password',
        'class': 'form-control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password',
        'class' : 'form-control',
    }))

    


    class Meta:
        model = Account
        fields = ['first_name', 'last_name','phone_number','email','password']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': ' First Name','class' : 'form-control'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name','class' : 'form-control'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email','class' : 'form-control'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone Number','class' : 'form-control'}),
                
        }
     
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "password does not match!"
            )

class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'phone_number')
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': ' First Name','class' : 'form-control'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name','class' : 'form-control'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone Number','class' : 'form-control'}),
                
        }
    


class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, error_messages = {'invalid':{"Image files only"}},widget=forms.FileInput)
    class Meta:
        model = UserProfile
        fields = ('address_line_1', 'address_line_2', 'city','state','country', 'profile_picture')
        widgets = {
            'address_line_1': forms.TextInput(attrs={'placeholder': 'Address Line 1','class' : 'form-control'}),
            'address_line_2': forms.TextInput(attrs={'placeholder': 'Address Line 2','class' : 'form-control'}),
            'city': forms.TextInput(attrs={'placeholder': 'City','class' : 'form-control'}),
            'state': forms.TextInput(attrs={'placeholder': 'State','class' : 'form-control'}),
            'country': forms.TextInput(attrs={'placeholder': 'State','class' : 'form-control'}),
            'profile_picture': forms.TextInput(attrs={'placeholder': 'Profile Picture','class' : 'form-control'}),    
        }
        

    
    

