import requests
from datetime import timedelta, datetime
import re


class Parser():

    def last_workday(self):
        today = datetime.now()
        offset = max(1, (today.weekday() + 6) % 7 - 3)
        delta = timedelta(offset)
        last_workday = today - delta
        return str(last_workday).split(' ')[0]

    def vacancies(self):
        workday = self.last_workday()

        params = {
            'text': 'специалист по информационной безопасности',
            'date_from': workday,
            'date_to': workday,
        }

        resp = requests.get('https://api.hh.ru/vacancies', params=params)
        return resp.json()

    def vacancy_info(self, vacancy_id: str):
        resp = requests.get(f'https://api.hh.ru/vacancies/{vacancy_id}')
        return resp.json()

    def parse_vacancies(self):
        vacanciesList = []
        counter = 0
        for vacancy in self.vacancies()['items']:
            if counter == 10:
                break
            data = self.vacancy_info(vacancy['id'])

            name = data['name']

            skills = ''
            for skill in data['key_skills']:
                skills += f"{skill['name']}, "
            skills = skills[:-2]

            try:
                salary = data['salary']['from']
                currency = data['salary']['currency']
            except TypeError:
                salary = 'Не указано'
                currency = ''

            if skills == '':
                skills = 'Не указано'

            if salary is None:
                salary = 'Не указано'
                currency = ''

            region = data['area']['name']

            template = re.compile('<.*?>')
            description = re.sub(template, '', data['description'])

            template = re.compile('&.*?;')
            description = re.sub(template, '', description)

            company = data['employer']['name']

            date_published = data['published_at'].split('T')[0]

            # Добавление в главный список словарей с данными вакансии
            vacanciesList.append(
                {
                    'name': name,
                    'description': description,
                    'skills': skills,
                    'company': company,
                    'price': f"{salary} {currency}",
                    'region': region,
                    'date_published': date_published
                }
            )
            counter += 1
        return vacanciesList


if __name__ == '__main__':
    hh = Parser()
    print(hh.parse_vacancies())
