import xml.etree.ElementTree as ET

import xml.dom.minidom as minidom
import glob
import mercator
import os


def create_document(name):
    root = ET.Element('kml')
    root.set('xmlns', "http://www.opengis.net/kml/2.2")
    root.set('xmlns:gx', "http://www.google.com/kml/ext/2.2")
    root.set('xmlns:kml', "http://www.opengis.net/kml/2.2")
    root.set('xmlns:atom', "http://www.w3.org/2005/Atom")
    document = ET.SubElement(root, "Document")
    ET.SubElement(document, "name").text = name
    return root


def create_folder(elem: ET.Element, name:str ):
    fld = ET.SubElement(elem,"Folder")
    ET.SubElement(fld,"name").text = name
    return fld


def create_overlay(elem: ET.Element, zoom:int, x:int,y:int ):
    overlay = ET.SubElement(elem,"GroundOverlay")
    ET.SubElement(overlay, "name").text = "%s_%s"%(x,y)
    ET.SubElement(overlay, "visibility").text = "0"
    icon = ET.SubElement(overlay, "Icon")
    ET.SubElement(icon, "href").text = "%s/%s_%s.png" % (zoom,x,y)
    latlonbox = ET.SubElement(overlay, "LatLonBox")
    ET.SubElement(latlonbox, "north").text = "%s" % mercator.tile_lat(zoom,y)
    ET.SubElement(latlonbox, "south").text = "%s" % mercator.tile_lat(zoom,y+1)
    ET.SubElement(latlonbox, "west").text = "%s" % mercator.tile_lng(zoom,x)
    ET.SubElement(latlonbox, "east").text = "%s" % mercator.tile_lng(zoom,x+1)




def make_pretty_xml(fname: str):
    r = ET.parse(fname)
    doc2 = minidom.parseString(ET.tostring(r.getroot()))
    open(fname[:-4] + "_pretty." + fname[-3:], 'wb'  ).write(doc2.toprettyxml(encoding='UTF-8'))



def create_kml(path: str, zooms: tuple):
    local_path = path.replace("\\","/").split("/")[-1]
    root = create_document(local_path)
    document = root.find("Document")
    for zoom in zooms:
        l = glob.glob1( os.path.join(path,str(zoom)) ,"*.png")
        fld = create_folder(document, str(zoom))
        for fn in l:
            x,y =  [int(v) for v in  fn.split(".")[0].split('_') ]
            create_overlay(fld, zoom,x,y)
    return ET.tostring(root)

def get_point_koordinates(path: str):
    points = []
    etree = ET.parse(path)
    placemarks = [e for e in etree.getiterator() if e.tag.endswith("Placemark") ]
    for placemark in placemarks:
        point = [e for e in placemark.getiterator() if e.tag.endswith("Point")][0]
        coordinates = [e for e in point.getiterator() if e.tag.endswith("coordinates")][0]
        points.append(  [float(a) for a in coordinates.text.split(',')[0:2]])
    return points



# fld = create_folder(document,"my_folder")
# fld2 = create_folder(fld,"my_folder2")
# create_overlay(fld2,0,0)
#
# doc = minidom.parseString(ET.tostring(root))
# open("base.kml",'wb').write(doc.toprettyxml(encoding='UTF-8'))



# make_pretty_xml("C:\\Users\\HOME\\Downloads\\init.kml")
