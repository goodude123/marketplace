from plot import Plot
from currency_files import CurrenciesFile, CurrenciesRandomCoursesFile


class TestsPlot(Plot):
    def __init__(self, abbr):
        super().__init__(abbr)
        self.path = 'test_currencies/'
        self.currency_directory_path = self.path + self.abbr + '/'


class TestsCurrencies(CurrenciesFile):
    def set_path_to_save_all_files(self):
        return 'test_currencies/'


# make Data object
scrapped_data = TestsCurrencies()

# Scrap Data
scrapped_data.get_currencies()
scrapped_data.save_currencies()

random_currency_course = CurrenciesRandomCoursesFile()
# Add random Data
random_currency_course.random_edit_course_value()
print(random_currency_course.currencies)
# Save modified data to csv
random_currency_course.save_currencies()

tested_plot = TestsPlot('AUD')
tested_plot.create_graph()
