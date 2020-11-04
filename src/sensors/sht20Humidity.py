from sht20 import SHT20

def run():
    sht = SHT20(1, resolution=SHT20.TEMP_RES_14bit)
    return sht.read_humid()