from location import Location

from ..schemas import Location as ApiLocation


class LocationMapper:
    @staticmethod
    def request_to_location(location: ApiLocation) -> Location:
        return Location(name=location.name)

    @staticmethod
    def location_to_request(location: Location) -> ApiLocation:
        return ApiLocation(name=location.name)
