from django.db import models
from django.db.models import constraints


class Vacancy(models.Model):
    jobTitle = models.TextField(verbose_name='Vacancy name')
    companyName = models.TextField(verbose_name='Employing Company')
    companyLocation = models.TextField(verbose_name='Company address')
    c_url = models.URLField(
        verbose_name='Company URL',
        max_length=1000,
        db_index=True,
        unique=False,
        null=True,
        blank=True
    )
    salary = models.TextField()
    p_date = models.TextField(verbose_name='Vacancy posting date')
    details = models.TextField(verbose_name='Job details')
    informLink = models.URLField(
        verbose_name='additional information',
        max_length=1000,
        db_index=True,
        unique=True,
        null=True,
        blank=True
        )

    class Meta:
        verbose_name = 'All junior python developer vacancies'
        constraints = [constraints.UniqueConstraint(
            fields=['jobTitle', 'companyName', 'details'],
            name='Vacancy_must_be_unique'),
        ]

    def __str__(self) -> str:
        return f'{self.companyName} employing {self.jobTitle}'
