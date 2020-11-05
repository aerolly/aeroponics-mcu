from sht20 import SHT20
import sys

def run():
    sht = SHT20(1, resolution=SHT20.TEMP_RES_14bit)
    humidity = sht.read_humid()
    if humidity < 0:
        sys.exit("failed to access sht20")
    else:
        return humidity