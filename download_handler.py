import settings
import os
import tileweb
import kml
import xml.dom.minidom as minidom


main_win_settings = ("proj_name", "north", "south", "west", "east", "zoom1", "zoom2", "proj_folder")


class DownloadHandler(object):
    def __init__(self,print_func = print):
        self.proj_name = ""
        self.north = 0
        self.south = 0
        self.west = 0
        self.east = 0
        self.zoom1 = 0
        self.zoom2 = 0
        self.proj_folder = ""
        self.printf = print_func

    def load(self, path="settings_.json"):
        s = settings.Settings()
        s.load(os.path.join(os.curdir, path))
        s.get(self, "main_win", main_win_settings)

    def save(self, path="settings_.json"):
        s = settings.Settings()
        s.put(self, "main_win", main_win_settings)
        s.save(path)

    def load_koordinates_from_kml(self, path:str):
        l = kml.get_point_koordinates(path)
        # if not len(l) == 2:
        #     QtGui.QMessageBox.critical(self, "Error", "NUmber of points is not 2")
        #     return
        zl = list(zip(*l))
        (self.west, *tmp, self.east) = sorted(zl[0])
        (self.south, *tmp, self.north) = sorted(zl[1])
        print(self.west, self.east, self.north,self.south)

    def download_tiles_and_make_kml(self):
        box = tileweb.Lonlatbox(self.west,self.north,self.east,self.south)
        prj_fld = os.path.join(self.proj_folder, self.proj_name)

        scale_range = tuple([z for z in range(self.zoom1,self.zoom2+1) ])
        for scale in scale_range:
            fld = os.path.join(prj_fld, str(scale))
            tileweb.download_scale(scale, fld, box,printf = self.printf)
        kml_text = kml.create_kml(prj_fld,scale_range)
        doc = minidom.parseString(kml_text)
        f = open(os.path.join(prj_fld,"%s.kml" % self.proj_name),'wb')
        f.write(doc.toprettyxml(encoding='UTF-8'))
        f.close()
        self.printf('Complete')

    def print_tilecount(self):
        box = tileweb.Lonlatbox(self.west, self.north, self.east, self.south)
        self.printf("Coordinates %s" %  box )
        for zoom in range(self.zoom1,self.zoom2+1):
            tileweb.calculate_tile_count(zoom,box,print_func = self.printf   )



