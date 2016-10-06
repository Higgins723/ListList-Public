def distance_from(location, distance):
    products = []
    for z in Zipcode.objects.filter(geom__distance_lt=(location, D(mi=distance))):
        for i in Product.objects.all():
            if z == i.zipcode:
                products.append(i)
    return products


def distance_from(location, distance):
    products = []
    for z in Zipcode.objects.filter(geom__distance_lt=(location, D(mi=distance))):
        products.append(Product.objects.filter(zipcode__zipcode__in=z))
    return products

from geopy.geocoders import Nominatim
geolocator = Nominatim()
from zipcode.models import Zipcode
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
location = geolocator.geocode("83442")
rigby = Point(location.longitude, location.latitude)
def distance_from(location, distance):
    products = []
    for z in Zipcode.objects.filter(geom__distance_lt=(location, D(mi=distance))):
        products.append(Product.objects.filter(zipcode__zipcode__in=z))
    return products

distance_from(rigby, 10)

#distance
zipcodes = [92530, 93530]
Product.objects.filter(zipcode__zipcode__in=zipcodes)

def get_location_zip(location, distance):
    zipcodes = []
    for zipcode in Zipcode.objects.filter(geom__distance_lt(location, D(mi=distance))):
        zipcodes.append(zipcode)
    return zipcodes