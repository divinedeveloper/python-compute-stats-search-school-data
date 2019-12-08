import csv
import itertools
import time


class SchoolDetail(object):

    def __init__(self, school_name, city_name, state_name):
        self.school_name = school_name
        self.city_name = city_name
        self.state_name = state_name
        sorted_name_list = sorted([school_name, city_name, state_name])
        self.searchable_name_string = ' '.join(sorted_name_list)
        self.weighted_score = 0


class SchoolSearch:

    def __init__(self, school_data_file_name):
        # might use dict instead of tuplefor datarows
        self.school_detail_rows = list(self.read_school_file_data(school_data_file_name))

    def read_school_file_data(self, school_data_file_name):
        try:
            with open(school_data_file_name, 'r', newline='', encoding="ISO-8859-1") as school_file:
                csv_reader = csv.DictReader(school_file)
                for row in csv_reader:
                    yield SchoolDetail(row['SCHNAM05'], row['LCITY05'], row['LSTATE05'])
        except FileNotFoundError:
            print(f'{school_data_file_name} file not found')
            exit()

    def perform_search(self, query_list):

        self.search_results = []

        for school_detail in self.school_detail_rows:

            for query in query_list:
                if query in school_detail.searchable_name_string:

                    school_detail.weighted_score = school_detail.weighted_score + 5

            if school_detail.weighted_score > 0:
                self.search_results.append(school_detail)

    def print_results(self):
        if self.search_results:
            self.search_results.sort(key=lambda row: row.weighted_score, reverse=True)
            for index, school in enumerate(self.search_results[:3]):

                print(f'{index+1}. {school.school_name}')
                print(f'{school.city_name}, {school.state_name}')
        else:
            print('No results found')

    def sanitize_query_params(self, query):
        query = query.strip().upper()
        query = set(query.split())
        return sorted(query)


def search_schools(query):
    school_search = SchoolSearch('school_data.csv')
    query_list = school_search.sanitize_query_params(query)

    start_time = time.time()

    school_search.perform_search(query_list)

    end_time = time.time()

    print(f'Results for "{query}" (search took: {end_time-start_time:.3f}s)')

    school_search.print_results()


if __name__ == '__main__':
    search_schools("elementary school highland park")
    print()

    search_schools("jefferson belleville")
    print()

    search_schools("riverside school 44")
    print()

    search_schools("granada charter school")
    print()

    search_schools("foley high alabama")
    print()

    search_schools("KUSKOKWIM")
    print()
