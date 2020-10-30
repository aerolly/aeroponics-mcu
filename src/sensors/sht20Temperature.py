from SHT20 import SHT20

def run():
    sht = SHT20()
    return sht.temperature()