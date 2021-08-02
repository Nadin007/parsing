from collections import namedtuple
import requests
import bs4
from django.core.management.base import BaseCommand

from job_parser.models import Vacancy

InnerBlock = namedtuple(
    'Block',
    ('jobTitle,companyLocation,companyName,'
     'c_url,salary,date,details,informLink')
    )


class Block(InnerBlock):
    def __str__(self) -> str:
        return (
            f'{self.jobTitle}\n {self.companyLocation}\n {self.companyName}\n'
            f'{self.c_url}\n {self.salary}\n {self.details}\n {self.date}\n'
            f'{self.informLink}\n')


class IndeedParser:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers = {
            'User-Aget': (
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
                ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164'
                ' Safari/537.36'
                ),
            'Accept-Language': 'en',
        }

    def get_page(self, page: int = None):
        params = {
            'q': 'junior python',
            'l': "Toronto, ON",
        }
        if page and page > 1:
            params['start'] = page

        url = 'https://ca.indeed.com/jobs'
        r = self.session.get(url, params=params)
        return r.text

    def parse_block(self, item):
        url_block = item
        href = url_block.get('href')
        if href:
            url = 'https://ca.indeed.com' + href
        else:
            url = None

        try:
            """Get block with a title."""

            jobTitle_block = item.select_one(
                'h2.jobTitle > span')
            jobTitle = jobTitle_block.string.strip()

            """Get job information"""
            companyName_block = item.select_one('a.companyOverviewLink')
            if companyName_block:
                companyName = companyName_block.get_text('\n')
                company_url = companyName_block.get('href')
                if company_url:
                    c_url = 'https://ca.indeed.com' + company_url
            else:
                companyName_block = item.select_one('span.companyName')
                companyName = companyName_block.get_text(' ')
                c_url = None

            companyLocation_block = item.select_one('div.company_location')
            if companyLocation_block is not None:
                companyLocation = companyLocation_block.get_text(' ')

            job = 'Details are not specified'
            job_block = item.select_one('div.job-snippet > ul > li')
            if job_block:
                job = job_block.get_text('\n')

            date_block = item.select_one('span.date')
            date = date_block.get_text('\n')

            """Get salary"""

            salary_block = item.select_one('span.salary-snippet')
            if salary_block is not None:
                salary = salary_block.get_text('\n')
            else:
                salary = "Not provided."
            try:
                p = Vacancy.objects.get(
                    jobTitle=jobTitle, companyName=companyName, details=job)
                p.informLink = url
                p.companyLocation = companyLocation
                p.c_url = c_url
                p.salary = salary
                p.p_date = date
                p.save()
            except Vacancy.DoesNotExist:
                p = Vacancy(
                    jobTitle=jobTitle,
                    companyName=companyName,
                    companyLocation=companyLocation,
                    c_url=c_url,
                    salary=salary,
                    p_date=date,
                    details=job,
                    informLink=url,
                ).save()

            print(f'Vacancies {p}')

            return Block(
                jobTitle=jobTitle,
                companyName=companyName,
                companyLocation=companyLocation,
                c_url=c_url,
                salary=salary,
                details=job,
                date=date,
                informLink=url
            )

        except Exception as e:
            raise Exception(
                f'Не удалось распарсить вакансии: {e}')

    def get_pagination_limit(self):
        page_list = range(0, 300, 10)
        for page in page_list:
            if self.get_block(page):
                break

    def get_block(self, page):
        text = self.get_page(page=page)
        soup = bs4.BeautifulSoup(text, 'lxml')
        vacancy_list = soup.select('a.result')
        for item in vacancy_list:
            block = self.parse_block(item=item)
            print(block)
        return soup.select('p.dupetext') is not None


class Command(BaseCommand):
    help = 'Vacancies parsing'

    def handle(self, *args, **options):
        p = IndeedParser()
        p.get_pagination_limit()
