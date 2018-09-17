from plot import Plot
from currency import Currencies, CurrenciesRandomCourses


class TestsPlot(Plot):
    def __init__(self, abbr):
        super().__init__(abbr)
        self.path = 'test_currencies/'
        self.currency_directory_path = self.path + self.abbr + '/'

    def show_rates_and_info(self):
        print(self.currency_directory_path)
        print(self.path)
        print(self.abbr)
        print(self.currency_rates)
        print(self.currency_info)


class TestsCurrencies(Currencies):
    def set_path_to_save_all_files(self):
        return 'test_currencies/'


# make Data object
scrapped_data = TestsCurrencies()

# Scrap Data
scrapped_data.get_currencies()
scrapped_data.save_currencies()

random_currency_course = CurrenciesRandomCourses()
# Add random Data
random_currency_course.random_edit_course_value()
print(random_currency_course.currencies)
# Save modified data to csv
random_currency_course.save_currencies()

tested_plot = TestsPlot('USD')
tested_plot.if_main_dir_assign_()
tested_plot.show_rates_and_info()
