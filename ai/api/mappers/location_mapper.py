from location import Location
from api import Location as ApiLocation

class LocationMapper:
    def request_to_location(location_request: ApiLocation) -> Location:
        return Location(
            name=location_request.name
        )