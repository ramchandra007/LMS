from django import forms
from .models import HomeNav
from django import forms
from django.forms.widgets import DateInput, TextInput

from .models import *


class FormSettings(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormSettings, self).__init__(*args, **kwargs)
        # Here make some changes such as:
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'





class NavForm(forms.Form):
    class Meta:
        model = HomeNav
        fields='__all__'

class Teacherform(forms.Form):
    class Meta:
        model = Teachers
        fields='__all__'


       

class CourseForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)

    class Meta:
        fields = ['name']
        model = Course       


class SubjectForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(SubjectForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Subject
        fields = ['name']

from django import forms
from .models import UploadedFile

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ('file','subjectname','parent_category','chapter_no')



class Teacherform(forms.Form):
    class Meta:
        model = Teachers
        fields='__all__'

class CourseForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)

    class Meta:
        fields = ['name']
        model = Course       

class SubjectForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(SubjectForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Subject
        fields = ['name']

from django import forms
from .models import LateLoginRequest

class LateLoginRequestForm(forms.ModelForm):
    class Meta:
        model = LateLoginRequest
        fields = ['reason']  # Only include the reason in the form
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Provide the reason for your late login...'}),
        }




