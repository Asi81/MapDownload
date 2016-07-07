import PIL.Image
import PIL.PngImagePlugin
import PIL
import glob
import os




def make_puzzle(path: str):

    l = glob.glob1(path,"*.png")
    xl = sorted([ int(v.split(".")[0].split('_')[0]) for v in l])
    yl = sorted([ int(v.split(".")[0].split('_')[1]) for v in l])
    print("%s %s %s %s" % (xl[0],yl[0],xl[-1],yl[-1]))
    width = (xl[-1] - xl[0] + 1)*256
    height = (yl[-1] - yl[0]+1)*256
    x0  = xl[0]*256
    y0 = yl[0]*256
    im = PIL.Image.new('RGB', (width,height))
    for fn in l:
        pair =  [int(v)*256 for v in  fn.split(".")[0].split('_') ]
        x,y = (pair[0] - x0, pair[1] - y0)
        sub = PIL.Image.open( os.path.join(path,fn))
        im.paste(sub,(x,y,x+256,y+256))
    return im

for scale in range(13,16):
    im = make_puzzle(r'C:\Temp\opentopomap\kazbek\%s' % scale  )
    im.save(r'C:\Temp\opentopomap\kazbek\%s.png' % scale)

# im = make_puzzle(r'C:\Temp\opentopomap\caucausus\13')
# im.save(r'C:\Temp\opentopomap\caucausus\13.png')

def create_map(scale :int , path: str ):
    sz = 256 * (2 ** scale)
    print(sz)
    im = PIL.Image.new('RGB', (sz,sz))  # create the image
    for x in range(0,2**scale):
        for y in range (0,2**scale):
            sub = PIL.Image.open(  "%s/%s/%s_%s.png" % (path,scale,x,y))
            box = (x*256,y*256,(x+1)*256,(y+1)*256)
            im.paste(sub,box)
    return im

# im = create_map(5,"C:/temp/opentopomap")
# im.show()
# im.save('C:/temp/opentopomap/5/full.png')
