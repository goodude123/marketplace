from currency import Data, RandomData, Plot

class PlotTest(Plot):
    def show_rates_and_info(self):
        print(self.currency_rates)
        print(self.currency_info)


# make Data object
scrapped_data = Data()

# Scrap Data
scrapped_data.get_currencies()
scrapped_data.save_currencies()

rand = RandomData()
# Add random Data
rand.edit_currency()
print(rand.currencies)
# Save modified data to csv
rand.save_currencies()

plot = PlotTest()
plot.read_data()
plot.show_rates_and_info()
