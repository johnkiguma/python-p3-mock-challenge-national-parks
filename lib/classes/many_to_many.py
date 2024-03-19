import re

class NationalPark:
    _all_parks = []

    def __init__(self, name):
        if not isinstance(name, str):
            raise ValueError("Name must be a string")
        if len(name) < 3:
            raise ValueError("Name length must be at least 3 characters")
        self._name = name
        self._trips = []
        self.__class__._all_parks.append(self)

    @property
    def name(self):
        return self._name

    def trips(self):
        return self._trips

    def visitors(self):
        return list(set(trip.visitor for trip in self._trips))

    def add_trip(self, trip):
        self._trips.append(trip)

    def total_visits(self):
        return len(self._trips)

    def best_visitor(self):
        if not self._trips:
            return None
        visitor_count = {}
        for trip in self._trips:
            visitor = trip.visitor
            if visitor in visitor_count:
                visitor_count[visitor] += 1
            else:
                visitor_count[visitor] = 1
        return max(visitor_count, key=visitor_count.get)

    @classmethod
    def most_visited(cls):
        parks = cls._all_parks
        if not parks:
            return None
        return max(parks, key=lambda park: park.total_visits())


class Trip:
    def __init__(self, visitor, national_park, start_date, end_date):
        self._visitor = visitor
        self._national_park = national_park
        self._validate_date(start_date)
        self._validate_date(end_date)
        self._start_date = start_date
        self._end_date = end_date
        visitor.add_trip(self)
        national_park.add_trip(self)

    @property
    def start_date(self):
        return self._start_date

    @property
    def end_date(self):
        return self._end_date

    @property
    def visitor(self):
        return self._visitor

    @property
    def national_park(self):
        return self._national_park

    def _validate_date(self, date_str):
        if not re.match(r"^\w+ \d{1,2}(st|nd|rd|th)$", date_str):
            raise ValueError("Invalid date format. Date should be in the format 'Month Dayth'.")

class Visitor:
    def __init__(self, name):
        if not isinstance(name, str):
            raise ValueError("Name must be a string")
        if not 1 <= len(name) <= 15:
            raise ValueError("Name length must be between 1 and 15 characters")
        self._name = name
        self._trips = []

    @property
    def name(self):
        return self._name

    def trips(self):
        return self._trips

    def national_parks(self):
        return list(set(trip.national_park for trip in self._trips))

    def add_trip(self, trip):
        self._trips.append(trip)

if __name__ == "__main__":
    try:
        visitor1 = Visitor("John")
        visitor2 = Visitor("Alice")
        park1 = NationalPark("Yellowstone")
        park2 = NationalPark("Yosemite")
        trip1 = Trip(visitor1, park1, "May 5th", "May 6th")
        trip2 = Trip(visitor1, park2, "May 7th", "May 8th")
        trip3 = Trip(visitor2, park1, "May 9th", "May 10th")

        print("Visitor:", visitor1.name)
        print("Trips:", [trip.start_date for trip in visitor1.trips()])
        print("National Parks:", [park.name for park in visitor1.national_parks()])

        print("Park:", park1.name)
        print("Trips:", [trip.start_date for trip in park1.trips()])
        print("Visitors:", [visitor.name for visitor in park1.visitors()])
        print("Total Visits:", park1.total_visits())
        print("Best Visitor:", park1.best_visitor().name)

        print("Most Visited Park:", NationalPark.most_visited().name)
    except Exception as e:
        print("An error occurred:", str(e))
