from PIL import Image
import argparse
import nbtlib
import math

def getColor(color_id):
    mapColors = [0,8368696,16247203,13092807,16711680,10526975,10987431,31744,16777215,10791096, 9923917, 7368816, 4210943, 9402184, 16776437, 14188339, 11685080, 6724056, 15066419, 8375321, 15892389, 5000268, 10066329, 5013401, 8339378, 3361970, 6704179, 6717235, 10040115, 1644825, 16445005, 6085589, 4882687, 55610, 8476209, 7340544, 13742497, 10441252, 9787244, 7367818, 12223780, 6780213, 10505550, 3746083, 8874850, 5725276, 8014168, 4996700, 4993571, 5001770, 9321518, 2430480]
    shadeMultipliers = [180,220,255,135]
    if color_id < 0:
        color_id = color_id + 256
    color_shade =  color_id % 4
    color_base_id = int((color_id - color_shade) / 4)
    color_base_int = mapColors[color_base_id]
    b =  color_base_int & 255
    g = (color_base_int >> 8) & 255
    r = (color_base_int >> 16) & 255
    color_base = (r,g,b)
    color_real = tuple(math.floor(c * shadeMultipliers[color_shade] / 255) for c in color_base)
    color_alpha = (color_real[0],color_real[1],color_real[2], 0 if color_base_id == 0 else 255)
    return color_alpha

def datToPng(datfile,pngfile):
    nbt_file = nbtlib.load(datfile)

    im      = Image.new("RGBA", (128, 128), "white")
    pix     = im.load()
    
    for h in range(128):
        for w in range(128):
            color_id = nbt_file[""]["data"]["colors"][w+h*128]
            pix[(w,h)] = getColor(color_id)
    
    im.save(pngfile,"PNG")

parser = argparse.ArgumentParser(description='Converts Minecraft\'s map.dat format to a PNG') 
parser.add_argument('infile', type=str, help='.dat file in')
parser.add_argument('outfile', type=str, help='.png file out')
args = parser.parse_args()

datToPng(args.infile,args.outfile)