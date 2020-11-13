
# This file is executed on every boot (including wake-boot from deepsleep)

from esp import check_fw, flash_size
from uos import statvfs

print("\n\nmicro python 8266. FRIGO")
check_fw()
print('\nflash size in Mbytes: ', flash_size()/(1024.0*1024.0))

#esp.osdebug(None)

# display flash size
#import port_diag

# do not include for 512k port
# free file system
i= statvfs('/')
fs = i[1]*i[2]/(1024.0*1024.0)
free= i[0]*i[4]/(1024.0*1024.0)
per = (float(free)/float(fs))
print('file system size %0.1f, free %0.1f, used in percent %0.1f' %(fs, free, per))

#uos.dupterm(None, 1) # disable REPL on UART(0)

# start webrepl after wifi. will be on 192.168.1.4:8266 (connect to wemos ssid) 
# and on local IP on home router as well
#WebREPL daemon started on ws://192.168.4.1:8266
#WebREPL daemon started on ws://192.168.1.5:8266
#Started webrepl in #ormal mode


# does not work on 512K, no file system ?
# need to import once webrepl_setup from a usb/ttl connection to set password
# creates webrepl_cfg.py (not visible in uPyCraft, visible w: os.listdir()
# cannot just browse to IP, need client http://micropython.org/webrepl/
"""
# only is wifi started
import webrepl # passwd 38112
print('start webrepl: use http://micropython.org/webrepl/ to access or use local webrepl.html')
webrepl.start()
"""















