from django import forms

from .models import Vacancy


class VacancyForm(forms.ModelForm):

    class Meta:
        model = Vacancy
        fields = (
            'jobTitle',
            'companyName',
            'companyLocation',
            'c_url',
            'salary',
            'p_date',
            'details',
            'informLink',
        )
        widgets = {
            'jobTitle': forms.TextInput,
        }
