from collections import namedtuple
import requests
import bs4

InnerBlock = namedtuple(
    'Block',
    'jobTitle,companyLocation,companyName,c_url,salary,date,job,more')


class Block(InnerBlock):
    def __str__(self) -> str:
        return (
            f'{self.jobTitle}\n {self.companyLocation}\n {self.companyName}\n'
            f'{self.c_url}\n {self.salary}\n {self.job}\n {self.date}\n'
            f'{self.more}\n')


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

    """@staticmethod
    def parse_date(item: str):
        params = item.strip().split(' ')
        first, second = params
        if first == 'Just' and second == 'posted':
            date = datetime.date.today()
        elif second == 'days' and first != '30+':
            days_ago = type(int(first))
            date = datetime.date.today() - datetime.timedelta(days=days_ago)
        elif second == 'day':
            date = datetime.date.today() - datetime.timedelta(days=1)
        elif first == '30+':
            params = item.strip().split('+')
            first = int(params)
            date = datetime.date.today() - datetime.timedelta(days=first)
        else:
            raise Exception('Не удалось распарсить дату', item)
        time = datetime.datetime.strptime('%H:%M').time()
        return datetime.datetime.combine(date=date, time=time)"""

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
                companyName = companyName_block.get_text('\n')
                c_url = None

            companyLocation_block = item.select_one('div.company_location')
            if companyLocation_block is not None:
                companyLocation = companyLocation_block.get_text('\n')

            job = None
            job_block = item.select_one('div.job-snippet > ul > li')
            if job_block:
                job = job_block.get_text('\n')

            date_block = item.select_one('span.date')
            date = date_block.get_text('\n')
            """if absolute_date:
                date = IndeedParser.parse_date(item=absolute_date)"""

            """Get salary"""

            salary_block = item.select_one('span.salary-snippet')
            if salary_block is not None:
                salary = salary_block.get_text('\n')
            else:
                salary = None

            return Block(
                jobTitle=jobTitle,
                companyName=companyName,
                companyLocation=companyLocation,
                c_url=c_url,
                salary=salary,
                job=job,
                date=date,
                more=url
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


def main():
    p = IndeedParser()
    p.get_pagination_limit()


if __name__ == '__main__':
    main()
