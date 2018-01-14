from django import forms

class Register(forms.Form):
    user_name = forms.CharField(label = 'Please enter your name: ', max_length = 100)
    user_password = forms.CharField(label = 'Please enter your password: ', max_length = 100)
    #user_password_confirm = forms.PasswordField(label = 'Password confirm', max_length = 100)
    user_address = forms.CharField(label = 'Please enter your address or use the address generator', max_length = 200)
    user_age = forms.CharField(label = 'Enter your age', max_length = 25)
    user_disease = forms.CharField(label = 'Please enter patient current disease or describe it', max_length = 100)
    user_email = forms.CharField(label = 'Please enter a valid email to keep in touch', max_length = 100)
    user_description = forms.CharField(label = 'Please describe how will you use the product', max_length=70)
    user_chronic_disease = forms.CharField(label = 'Tell us if you have any chronic disease to help our doctors provide best service for you', max_length = 140)
    user_categoury = forms.CharField(label = 'Tell us where will you use the product to help our medical engineers provide best hints for you', max_length = 70)

class Login(forms.Form):
    user_name = forms.CharField(label = "Please enter your user name ", max_length = 100)
    user_password = forms.CharField(label = "Please enter your password", max_length = 100)


class Products(forms.Form):
    department = forms.CharField(max_length = 100)

