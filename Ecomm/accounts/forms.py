from django import forms
from . models import Account


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
       'placeholder': 'enter password',
        'class': 'form-control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'confirm password',
        'class' : 'form-control',
    }))

    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'placeholder': 'email'})
        self.fields['phone_number'].widget.attrs.update({'placeholder': 'phone'})
        self.fields['first_name'].widget.attrs.update({'placeholder': 'first name'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'last_name'}) 


    class Meta:
        model = Account
        fields = ['first_name', 'last_name','phone_number','email','password']
     
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "password does not match!"
            )
