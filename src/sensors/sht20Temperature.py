from SHT20 import SHT20

def run():
    sht = SHT20(1)
    return sht.temperature_f()