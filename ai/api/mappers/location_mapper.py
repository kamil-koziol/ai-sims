from api import Location as ApiLocation
from location import Location


class LocationMapper:
    @staticmethod
    def request_to_location(location: ApiLocation) -> Location:
        return Location(name=location.name)

