import csv
from datetime import datetime


class Vacancy:
    def __init__(self, name, salary, area, time_publishing):
        self.area, self.salary, self.name, self.time_publishing = area, salary, name, time_publishing


class Salary:
    currencyToRub = {
        "GEL": 21.74,
        "KGS": 0.76,
        "RUR": 1,
        "UAH": 1.64,
        "AZN": 35.68,
        "BYR": 23.91,
        "EUR": 59.90,
        "USD": 60.66,
        "UZS": 0.0055,
        "KZT": 0.13,
    }

    def currency_converter(self, salary):
        return salary * self.currencyToRub[self.sal_currency]

    def to_get_average(self):
        temp = (int(float(self.salaryFrom)) + int(float(self.salaryTo))) / 2
        return self.currency_converter(temp)

    def __init__(self, salaryFrom, salaryTo, sal_currency):
        self.salaryFrom, self.salaryTo, self.sal_currency = salaryFrom, salaryTo, sal_currency


class InputConnect:
    def __init__(self):
        self.name_of_file, self.name_vac = self.to_get_data()

    def to_get_data(self):
        data = {}
        for request in self.get_input.keys():
            data[request] = input(request)
        return data.values()

    def print_data(self, data):
        for response in self.give_putput.items():
            print(f'{response[0]}{response[1](data)}')

    get_input = {"Введите название файла: ": lambda name_of_file: name_of_file,
                 "Введите название профессии: ": lambda name_vac: name_vac}

    give_putput = {"Динамика уровня зарплат по годам: ": lambda data: data.salaries_dinamic(),
                   "Динамика уровня зарплат по годам для выбранной профессии: ": lambda
                       data: data.vac_salary_for_prof_dinamics(),
                   "Динамика количества вакансий по годам: ": lambda data: data.amount_vac_statistics(),
                   "Динамика количества вакансий по годам для выбранной профессии: ": lambda
                       data: data.amount_vac_for_prof_statistics(),
                   "Уровень зарплат по городам (в порядке убывания): ": lambda data: data.salary_per_town_statistics(),
                   "Доля вакансий по городам (в порядке убывания): ": lambda data: data.what_part_vac_takes_per_town()}


class Data:
    columns = ["name", "salary_from", "area_name", "published_at"]

    def __init__(self, name_of_file, name_vac_param):
        self.name_of_file = name_of_file
        self.parser(name_of_file)
        self.vacans_by_year = self.by_year_vac_filter()
        self.name_vac_param = name_vac_param
        self.vac_by_year = self.by_year_vac_filter(self.name_vac_param)
        self.vacans_by_area = self.vac_filter_by_area()

    def parser(self, name_of_file):
        read_file, columns_name = self.read_csv(name_of_file)
        self.vacanciesObjects = self.filter_csv(read_file, columns_name)

    def read_csv(self, name_of_file):
        file = open(name_of_file, encoding='utf-8-sig', newline='')
        read_file = csv.DictReader(file)
        columns_name = read_file.fieldnames
        return read_file, columns_name

    def filter_csv(self, read_file, columns_name):
        vacancies = []
        for row in read_file:
            if all(row.values()) and len(columns_name) == len(row):
                temporary_row = {name: row[name] for name in columns_name}
                temporary_row['salary_from'] = Salary(temporary_row['salary_from'], temporary_row.pop('salary_to'),
                                                      temporary_row.pop("salary_currency"))
                vacancies.append(Vacancy(*[temporary_row[key] for key in self.columns]))
        return vacancies

    def vac_filter_by_area(self):
        vacans_by_area = {}
        for vacancy in self.vacanciesObjects:
            vacans_by_area.setdefault(vacancy.area, []).append(vacancy)
        vacans_by_area = self.by_area_clear(vacans_by_area)
        return vacans_by_area

    def by_area_clear(self, vacans_by_area):
        temporary_areas = vacans_by_area.copy()
        for keyArea in vacans_by_area.keys():
            if len(vacans_by_area[keyArea]) / len(self.vacanciesObjects) < 0.01:
                temporary_areas.pop(keyArea)
        return temporary_areas

    def salary_per_town_statistics(self):
        vacans_by_area = self.vacans_by_area.copy()
        for dataByArea in vacans_by_area.items():
            avg_sal_by_area = [vacancy.salary.to_get_average() for vacancy in dataByArea[1]]
            vacans_by_area[dataByArea[0]] = int(sum(avg_sal_by_area) / len(avg_sal_by_area))
        vacans_by_area = list(
            {k: v for k, v in sorted(vacans_by_area.items(), key=lambda item: item[1], reverse=True)}.items())
        vacans_by_area = {items[0]: items[1] for items in vacans_by_area[:10]}
        return vacans_by_area

    def amount_vac_statistics(self):
        amount_of_vac_by_year = self.vacans_by_year.copy()
        for objs_per_yeah in amount_of_vac_by_year.items():
            amount_of_vac_by_year[objs_per_yeah[0]] = len(objs_per_yeah[1])
        return amount_of_vac_by_year

    def vac_salary_for_prof_dinamics(self):
        salary_dinamics = self.vac_by_year.copy()
        if not salary_dinamics:
            return {key: 0 for key in self.currentKeys}
        for objs_per_yeah in salary_dinamics.items():
            avrg_by_year = [vacancy.salary.to_get_average() for vacancy in objs_per_yeah[1]]
            salary_dinamics[objs_per_yeah[0]] = int(sum(avrg_by_year) / len(avrg_by_year))
        return salary_dinamics

    def salaries_dinamic(self):
        salary_dinamics = self.vacans_by_year.copy()
        for objs_per_yeah in salary_dinamics.items():
            avrg_by_year = [vacancy.salary.to_get_average() for vacancy in objs_per_yeah[1]]
            salary_dinamics[objs_per_yeah[0]] = int(sum(avrg_by_year) / len(avrg_by_year))
        return salary_dinamics

    def amount_vac_for_prof_statistics(self):
        amount_of_vac_by_year = self.vac_by_year.copy()
        if not amount_of_vac_by_year:
            return {key: 0 for key in self.currentKeys}
        for objs_per_yeah in amount_of_vac_by_year.items():
            amount_of_vac_by_year[objs_per_yeah[0]] = len(objs_per_yeah[1])
        return amount_of_vac_by_year

    def what_part_vac_takes_per_town(self):
        vacans_by_area = self.vacans_by_area.copy()
        for dataByArea in vacans_by_area.items():
            vacans_by_area[dataByArea[0]] = round(len(dataByArea[1]) / len(self.vacanciesObjects), 4)
        vacans_by_area = list(
            {k: v for k, v in sorted(vacans_by_area.items(), key=lambda item: item[1], reverse=True)}.items())
        vacans_by_area = {items[0]: items[1] for items in vacans_by_area[:10]}
        return vacans_by_area

    def by_year_vac_filter(self, name_vac=None):
        salary_dinam = {}
        self.currentKeys = []
        for vacancy in self.vacanciesObjects:
            year = datetime.strptime(vacancy.time_publishing, '%Y-%m-%dT%H:%M:%S%z').year
            self.currentKeys.append(year)
            if name_vac is None or name_vac in vacancy.name:
                salary_dinam.setdefault(year, []).append(vacancy)
        return salary_dinam


get_input = InputConnect()
data = Data(get_input.name_of_file, get_input.name_vac)
get_input.print_data(data)
