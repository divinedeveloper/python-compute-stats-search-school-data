import csv
import itertools


class SchoolDetail(object):

    def __init__(self, city, state, metro_locale):
        self.city = city
        self.state = state
        self.metro_locale = metro_locale


class CountSchools:

    def __init__(self, school_data_file_name):
        self.school_detail_rows = tuple(self.read_school_file_data(school_data_file_name))

    def read_school_file_data(self, school_data_file_name):
        try:
            with open(school_data_file_name, 'r', newline='', encoding="ISO-8859-1") as school_file:
                csv_reader = csv.DictReader(school_file)
                for row in csv_reader:
                    yield SchoolDetail(row['LCITY05'], row['LSTATE05'], row['MLOCALE'])
        except FileNotFoundError:
            print(f'{school_data_file_name} file not found')
            exit()

    def each_state_schools(self):
        state_schools_iterator = self.sort_and_group(key=lambda row: row.state)
        self.print_state_or_metro_school_count(state_schools_iterator)

    def each_metro_centric_locale_schools(self):
        metro_locale_schools_iterator = self.sort_and_group(key=lambda row: row.metro_locale)
        self.print_state_or_metro_school_count(metro_locale_schools_iterator)

    def city_with_most_schools(self):
        city_schools_iterator = self.sort_and_group(key=lambda row: row.city)
        city_with_most_schools = ''
        city_max_schools_count = cities_with_atleast_one_school = 0
        for city, schools in city_schools_iterator:
            city_school_count = sum(1 for school in schools)
            if city_school_count >= 1:
                cities_with_atleast_one_school += 1
            if city_school_count > city_max_schools_count:
                city_max_schools_count = city_school_count
                city_with_most_schools = city

        print(f'City with most schools: {city_with_most_schools} ({city_max_schools_count} schools)')
        print(f'Unique cities with at least one school: {cities_with_atleast_one_school}')

    def sort_and_group(self, key=None):
        """Group sorted `iterable` on `key`."""
        sorted_rows = sorted(self.school_detail_rows, key=key)
        return itertools.groupby(sorted_rows, key=key)

    def print_state_or_metro_school_count(self, state_or_metro_schools_iterator):
        for state_or_metro_locale, schools in state_or_metro_schools_iterator:
            print(f'{state_or_metro_locale}: {len(list(schools))}')


def print_counts():
    count_schools = CountSchools('school_data.csv')
    print(f'Total Schools: {len(count_schools.school_detail_rows)}')
    print('Schools by State:')
    count_schools.each_state_schools()
    print('Schools by Metro-centric locale:')
    count_schools.each_metro_centric_locale_schools()
    count_schools.city_with_most_schools()


if __name__ == '__main__':
    print_counts()
