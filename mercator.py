import math

def get_tile_box(zoom, x, y):
    """convert Google-style Mercator tile coordinate to
    (minlat, maxlat, minlng, maxlng) bounding box"""

    minlat, minlng = get_tile_lat_lng(zoom, x, y + 1)
    maxlat, maxlng = get_tile_lat_lng(zoom, x + 1, y)

    return (minlat, maxlat, minlng, maxlng)


def tile_lat(zoom, y):

    # "map-centric" latitude, in radians:
    lat_rad = math.pi - 2*math.pi*y/(2**zoom)
    # true latitude:
    lat_rad = gudermannian(lat_rad)
    lat = lat_rad * 180.0 / math.pi

    return lat

def tile_lng(zoom, x):
    return -180.0 + 360.0*x/(2**zoom)


def get_tile_lat_lng(zoom, x, y):
    """convert Google-style Mercator tile coordinate to
    (lat, lng) of top-left corner of tile"""

    # "map-centric" latitude, in radians:
    lat_rad = math.pi - 2*math.pi*y/(2**zoom)
    # true latitude:
    lat_rad = gudermannian(lat_rad)
    lat = lat_rad * 180.0 / math.pi

    # longitude maps linearly to map, so we simply scale:
    lng = -180.0 + 360.0*x/(2**zoom)

    return (lat, lng)

def get_lat_lng_tile(lat, lng, zoom):
    """convert lat/lng to Google-style Mercator tile coordinate (x, y)
    at the given zoom level"""

    lat_rad = lat * math.pi / 180.0
    # "map-centric" latitude, in radians:
    lat_rad = inv_gudermannian(lat_rad)

    x = 2**zoom * (lng + 180.0) / 360.0
    y = 2**zoom * (math.pi - lat_rad) / (2 * math.pi)

    return (x, y)

def gudermannian(x):
    return 2*math.atan(math.exp(x)) - math.pi/2

def inv_gudermannian(y):
    return math.log(math.tan((y + math.pi/2) / 2))
