from location import Location

from ..schemas import Location as ApiLocation


class LocationMapper:
    @staticmethod
    def request_to_location(location: ApiLocation) -> Location:
        return Location(name=location.name)
