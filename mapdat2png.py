from PIL import Image
import argparse
import nbtlib
import math

def getColor(color_id):
    mapColors = [
        0,          # Index 0: Transparent (#000000)
        8368696,    # Index 1: Grass (#7FB238)
        16247203,   # Index 2: Sand (#F7E9A3)
        13092807,   # Index 3: Wool (#C7C7C7)
        16711680,   # Index 4: Fire (#FF0000)
        10526975,   # Index 5: Ice (#A0A0FF)
        10987431,   # Index 6: Metal (#A7A7A7)
        31744,      # Index 7: Plant (#007C00)
        16777215,   # Index 8: Snow (#FFFFFF)
        10791096,   # Index 9: Clay (#A4A8B8)
        9923917,    # Index 10: Dirt (#976D4D)
        7368816,    # Index 11: Stone (#707070)
        4210943,    # Index 12: Water (#4040FF)
        9402184,    # Index 13: Wood (#8F7748)
        16776437,   # Index 14: Quartz (#FFD8BE)
        14188339,   # Index 15: Color Orange (#D87F33)
        11685080,   # Index 16: Color Magenta (#B24CD8)
        6724056,    # Index 17: Color Light Blue (#6699D8)
        15066419,   # Index 18: Color Yellow (#E5E533)
        8375321,    # Index 19: Color Light Green (#7FCC19)
        15892389,   # Index 20: Color Pink (#F27FA5)
        5000268,    # Index 21: Color Gray (#4C4C4C)
        10066329,   # Index 22: Color Light Gray (#999999)
        5013401,    # Index 23: Color Cyan (#4C7F99)
        8339378,    # Index 24: Color Purple (#7F3FB2)
        3361970,    # Index 25: Color Blue (#334CB2)
        6704179,    # Index 26: Color Brown (#664C33)
        6717235,    # Index 27: Color Green (#667F33)
        10040115,   # Index 28: Color Red (#993333)
        1644825,    # Index 29: Color Black (#191919)
        16445005,   # Index 30: Gold (#FAEE4D)
        6085589,    # Index 31: Diamond (#5CDBD5)
        4882687,    # Index 32: Lapis Lazuli (#4A80FF)
        55610,      # Index 33: Emerald (#00D93A)
        8476209,    # Index 34: Podzol (#815631)
        7340544,    # Index 35: Nether (#700200)
        13742497,   # Index 36: Terracotta White (#D1B1A1)
        10441252,   # Index 37: Terracotta Orange (#9F5224)
        9787244,    # Index 38: Terracotta Magenta (#95576C)
        7367818,    # Index 39: Terracotta Light Blue (#706C8A)
        12223780,   # Index 40: Terracotta Yellow (#BA8524)
        6780213,    # Index 41: Terracotta Light Green (#677535)
        10505550,   # Index 42: Terracotta Pink (#A04D4E)
        3746083,    # Index 43: Terracotta Gray (#392923)
        8874850,    # Index 44: Terracotta Light Gray (#876B62)
        5725276,    # Index 45: Terracotta Cyan (#575C5C)
        8014168,    # Index 46: Terracotta Purple (#7A4958)
        4996700,    # Index 47: Terracotta Blue (#4C3E5C)
        4993571,    # Index 48: Terracotta Brown (#4C3223)
        5001770,    # Index 49: Terracotta Green (#4C522A)
        9321518,    # Index 50: Terracotta Red (#8E3C2E)
        2430480,    # Index 51: Terracotta Black (#251610)
        12398641,   # Index 52: Crimson Nylium (#BD3031)
        9715553,    # Index 53: Crimson Stem (#943F61)
        6035741,    # Index 54: Crimson Hyphae (#5C191D)
        1474182,    # Index 55: Warped Nylium (#167E86)
        3837580,    # Index 56: Warped Stem (#3A8A8C)
        5647422,    # Index 57: Warped Hyphae (#562C3E)
        1356933,    # Index 58: Warped Wart Block (#14B485)
        6579300,    # Index 59: Deepslate (#646464)
        14200723,   # Index 60: Raw Iron (#D8AF93)
        8365974,    # Index 61: Glow Lichen (#7FA796)
    ]
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
            color_id = nbt_file.get("",nbt_file)["data"]["colors"][w+h*128]
            pix[(w,h)] = getColor(color_id)
    
    im.save(pngfile,"PNG")

parser = argparse.ArgumentParser(description='Converts Minecraft\'s map.dat format to a PNG') 
parser.add_argument('infile', type=str, help='.dat file in')
parser.add_argument('outfile', type=str, help='.png file out')
args = parser.parse_args()

datToPng(args.infile,args.outfile)
