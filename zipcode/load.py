import os
from django.contrib.gis.utils import LayerMapping
from .models import Zipcode

usborder_mapping = {
    'zipcode' : 'ZCTA5CE10',
    'affgeoid10' : 'AFFGEOID10',
    'census_bureau_codes' : 'GEOID10',
    'aland10' : 'ALAND10',
    'awater10' : 'AWATER10',
    'geom' : 'MULTIPOLYGON25D',
}

us_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data', 'cb_2014_us_zcta510_500k.shp'))

def run(verbose=True):
    lm = LayerMapping(Zipcode, us_shp, usborder_mapping,
                      transform=False, encoding='iso-8859-1')

    lm.save(strict=True, verbose=verbose)