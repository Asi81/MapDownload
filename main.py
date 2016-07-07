
import sys
import download_handler



if len(sys.argv) < 2:
    print("At least one filename expected")

fname = sys.argv[1]
h = download_handler.DownloadHandler()
if fname.endswith(".json"):
    h.load(fname)

h.download_tiles_and_make_kml()
