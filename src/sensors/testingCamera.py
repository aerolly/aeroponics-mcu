from dotenv import load_dotenv
import camera as c

load_dotenv()

try:
     c.run('video1')
except:
    pass
try:
     c.run('video2')
except:
    pass
try:
     c.run('video3')
except:
    pass
try:
     c.run('video4')
except:
    pass
