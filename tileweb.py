import urllib.request
import os
import mercator
import itertools


class Lonlatbox(object):
    def __init__(self, x0, y0, x1, y1):
        self.west = x0
        self.north = y0
        self.east = x1
        self.south = y1
    def __str__(self):
        return str(self.__dict__).replace("{","").replace("}","").replace("\'","")


def lonrange(scale: int, bbox: Lonlatbox):
    return [x for x in range(0, 2 ** scale) if bbox.west < mercator.tile_lng(scale, x+1) and mercator.tile_lng(scale, x) < bbox.east]


def latrange(scale: int, bbox: Lonlatbox):
    return [x for x in range(0, 2 ** scale) if bbox.north > mercator.tile_lat(scale, x+1) and mercator.tile_lat(scale,x)> bbox.south]


def download_scale(scale: int, path: str, bbox: Lonlatbox, printf = print  ):
    printf("downloading scale %s to %s" % (scale, path))
    if not os.path.exists(path):
        os.makedirs(path)

    r = list(itertools.product(lonrange(scale, bbox), latrange(scale, bbox)))
    lr = len(r)
    printf("total tiles to download: %s" % lr)

    for num ,(x, y)  in enumerate(r):
        if not os.path.exists(os.path.join(path, "%s_%s.png" % (x, y))):
            response = urllib.request.urlopen('https://c.tile.opentopomap.org/%s/%s/%s.png' % (scale, x, y))
            png = response.read()
            open(os.path.join(path, "%s_%s.png" % (x, y)), 'wb').write(png)
        printf("\r%s/%s" % (num,lr), end="")
    printf("\ndownloaded\n")


def calculate_tile_count(scale: int, bbox: Lonlatbox, print_func = print):
    r = list(itertools.product(lonrange(scale, bbox), latrange(scale, bbox)))
    print_func("Zoom %s: Total tiles to download: %s" % (scale ,len(r)))



g_mapbox_token = "pk.eyJ1IjoiYXNpODEiLCJhIjoiZDg1MjUxYTM2Y2RlNmU3ZGM4NjZhZmIxMTAxNDg0OWEifQ.CptV8UPpRwKkm1MM8-t4Lw"


# mapbox://styles/mapbox/streets-v9
# mapbox://styles/mapbox/outdoors-v9
# mapbox://styles/mapbox/light-v9
# mapbox://styles/mapbox/dark-v9
# mapbox://styles/mapbox/satellite-v9
# mapbox://styles/mapbox/satellite-streets-v9

def get_mapbox_tile(zoom, x, y):
    mabbox_ref = 'http://a.tiles.mapbox.com/v4/mapbox.mapbox-streets-v7/%s/%s/%s.mvt?access_token=%s' % (
        zoom, x, y, g_mapbox_token)
    return mabbox_ref


