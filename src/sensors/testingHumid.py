from sht20 import SHT20

sht = SHT20(1, resolution=SHT20.TEMP_RES_14bit)
print(sht.read_humid())
