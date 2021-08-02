from .forms import VacancyForm
from django.contrib import admin
from .models import Vacancy


class VacancyAdmin(admin.ModelAdmin):
    ordering = ['jobTitle']
    list_display = (
        'jobTitle', 'companyName', 'companyLocation',
        'c_url', 'salary', 'p_date', 'details', 'informLink')
    list_filter = ('companyName', 'p_date')
    search_fields = ('companyName', 'companyLocation')
    empty_value_display = '-empty-'
    form = VacancyForm

    class Media:
        css = {
            'all': ('admin/css/mymodel_list.css',)
        }


admin.site.register(Vacancy, VacancyAdmin)
