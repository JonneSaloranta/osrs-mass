from django import forms
from django.contrib.auth import authenticate, get_user_model

class UserLoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):

        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        
        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError("This user does not exist")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect password")
            if not user.is_active:
                raise forms.ValidationError("This user is not longer active.")
        return super(UserLoginForm, self).clean(*args, **kwargs)
    
user = get_user_model()


class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(label='Email Address')
    email2 = forms.EmailField(label='Confirm Email')
    name = forms.CharField(label='Name')
    lastname = forms.CharField(label='Lastname')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = user
        fields = [
            'email',
            'email2',
            'name',
            'lastname',
            'password',
            'password2',
        ]
    
    def clean(self):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
        name = self.cleaned_data.get('name')
        lastname = self.cleaned_data.get('lastname')
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if email != email2:
            raise forms.ValidationError("Emails must match")        
        
        email_qs = user.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("This email has already been registered")
        
        if password != password2:
            raise forms.ValidationError("Passwords must match")
        return super(UserRegisterForm, self).clean()
    
class RequestActivationEmailForm(forms.Form):
    email = forms.EmailField(label='Email Address')
    