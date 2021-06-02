from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Task

class SignupForm(UserCreationForm):
    def __init__(self,*args,**kwargs):
        super(UserCreationForm,self).__init__(*args,**kwargs)
        for field in ['first_name','last_name','password1','password2','username']:
            self.fields[field].help_text = None
            self.fields[field].required = True
    def clean_email(self):
        email = self.cleaned_data['email']
        check = User.objects.filter(email=email).exists()
        if check:
            raise ValidationError('Email already exists')
        return email
    class Meta():
        model=User
        fields=('first_name','last_name','username','email','password1','password2')
        
class TaskForm(forms.ModelForm):
    class Meta():
        model = Task
        fields = ('task_details','task_no','remarks')