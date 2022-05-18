class CarPollutionPermit:
    def __init__(self):
        self.permit = False

    def check_permit(self, year, mileage):
        if year < 2016:
            self.permit = False
            return False
        if mileage > 15:
            return True
        return False


class BikePollutionPermit:
    def __init__(self):
        self.permit = True
        self.new_permit = False
        self.no_permit = True

    def check_permit(self, year, mileage):
        if year < 2010:
            self.permit = False
            self.new_permit = False
            return False
        if mileage < 40:
            if year > 2016:
                return True
            self.permit = False
            return False
        self.permit = True
        tractor_pollutants_permit = TractorPollutionPermit()
        tractor_pollutants_permit.fetch_tractor(2018, True)
        return True


class TractorPollutionPermit:
    def fetch_tractor(self, year, is_farmer):
        if year > 2015 and is_farmer:
            return True
        if year > 2017:
            return True
        return False

    def fetch_lorry(self, year, is_farmer):
        if year > 2015 and is_farmer:
            return True
        if year > 2017:
            return True
        return False


class TractorPesticides(TractorPollutionPermit):
    def fetch_pesticides_permit(self, pesticide_effect):
        if pesticide_effect < 10:
            if self.fetch_tractor(2019, True):
                return True
            return False
        car_pollution_permit = CarPollutionPermit()
        return (car_pollution_permit.check_permit(2019, 16))
