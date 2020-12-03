from sht20 import SHT20

def run(param=None):
    sht = SHT20(1, resolution=SHT20.TEMP_RES_14bit)
    # reading in celsius, convert to F
    return (sht.read_temp() * (9/5)) + 32