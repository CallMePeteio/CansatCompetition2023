






import serial
import time


# Simple GPS module demonstration.
# Will wait for a fix and print a message every second with the current location

# and other details.

import time
import board
import busio
import adafruit_gps

# Define RX and TX pins for the board's serial port connected to the GPS.
# These are the defaults you should use for the GPS FeatherWing.
# For other boards set RX = GPS module TX, and TX = GPS module RX pins.
#RX = board.RX
#TX = board.TX

# Create a serial connection for the GPS connection using default speed and
# a slightly higher timeout (GPS modules typically update once a second).

#uart = busio.UART(TX, RX, baudrate=9600, timeout=30)

# for a computer, use the pyserial library for uart access
import serial
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=3000)
# Create a GPS module instance.
gps = adafruit_gps.GPS(uart, debug=False)


# Initialize the GPS module by changing what data it sends and at what rate.
# These are NMEA extensions for PMTK_314_SET_NMEA_OUTPUT and
# PMTK_220_SET_NMEA_UPDATERATE but you can send anything from here to adjust
# the GPS module behavior:
# https://cdn-shop.adafruit.com/datasheets/PMTK_A11.pdf

# Turn on the basic GGA and RMC info (what you typically want)
gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
# Turn on just minimum info (RMC only, location):
#gps.send_command(b'PMTK314,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
# Turn off everything:
#gps.send_command(b'PMTK314,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
# Tuen on everything (not all of it is parsed!)
#gps.send_command(b'PMTK314,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0')


# Set update rate to once a second (1hz) which is what you typically want.
gps.send_command(b'PMTK220,1000')
# Or decrease to once every two seconds by doubling the millisecond value.
# Be sure to also increase your UART timeout above!
#gps.send_command(b'PMTK220,2000')
# You can also speed up the rate, but don't go too fast or else you can lose
# data during parsing. This would be twice a second (2hz, 500ms delay):
#gps.send_command(b'PMTK220,500')

# Main loop runs forever printing the location, etc. every second.
last_print = time.monotonic()
while True:
    # Make sure to call gps.update() every loop iteration and at least twice
    # as fast as data comes from the GPS unit (usually every second).
    # This returns a bool that's true if it parsed new data (you can ignore it
    # though if you don't care and instead look at the has_fix property).
    gps.update()
    # Every second print out current location details if there's a fix.
    current = time.monotonic()

    if current - last_print >= 1.0:
        last_print = current

    if not gps.has_fix:
    # Try again if we don't have a fix yet.
        print('Waiting for fix...')
        continue

    # We have a fix! (gps.has_fix is true)
    # Print out details about the fix like location, date, etc.
    print('=' * 40) # Print a separator line.

    print('Fix timestamp: {}/{}/{} {:02}:{:02}:{:02}'.format(
    gps.timestamp_utc.tm_mon, # Grab parts of the time from the
    gps.timestamp_utc.tm_mday, # struct_time object that holds
    gps.timestamp_utc.tm_year, # the fix time. Note you might
    gps.timestamp_utc.tm_hour, # not get all data like year, day,
    gps.timestamp_utc.tm_min, # month!
    gps.timestamp_utc.tm_sec))
    print('Latitude: {0:.6f} degrees'.format(gps.latitude))
    print('Longitude: {0:.6f} degrees'.format(gps.longitude))
    print('Fix quality: {}'.format(gps.fix_quality))

    # Some attributes beyond latitude, longitude and timestamp are optional
    # and might not be present. Check if they're None before trying to use!
    if gps.satellites is not None:
        print('# satellites: {}'.format(gps.satellites))
    if gps.altitude_m is not None:
        print('Altitude: {} meters'.format(gps.altitude_m))
    if gps.speed_knots is not None:
        print('Speed: {} knots'.format(gps.speed_knots))
    if gps.track_angle_deg is not None:
        print('Track angle: {} degrees'.format(gps.track_angle_deg))
    if gps.horizontal_dilution is not None:
        print('Horizontal dilution: {}'.format(gps.horizontal_dilution))
    if gps.height_geoid is not None:
        print('Height geo ID: {} meters'.format(gps.height_geoid))





"""
ser = serial.Serial(
    port="/dev/ttyS0",
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)



while True: 
    print(gps.has_fix)
    print(gps.satellites)


    print()
    time.sleep(1)
    #print(ser.readline())

"""


var = """ ashmem           loop1         ram13    tty16  tty42      ttyS0     vcsu4
autofs           loop2         ram14    tty17  tty43      uhid      vcsu5
block            loop3         ram15    tty18  tty44      uinput    vcsu6
btrfs-control    loop4         ram2     tty19  tty45      urandom   vcsu7
bus              loop5         ram3     tty2   tty46      v4l       vga_arbiter
cachefiles       loop6         ram4     tty20  tty47      vchiq     vhci
char             loop7         ram5     tty21  tty48      vcio      vhost-net
console          loop-control  ram6     tty22  tty49      vc-mem    vhost-vsock
cpu_dma_latency  mapper        ram7     tty23  tty5       vcs       video0
cuse             media0        ram8     tty24  tty50      vcs1      video10
disk             media1        ram9     tty25  tty51      vcs2      video11
dma_heap         media2        random   tty26  tty52      vcs3      video12
dri              media3        rfkill   tty27  tty53      vcs4      video13
fb0              mem           serial0  tty28  tty54      vcs5      video14
fb1              mmcblk0       serial1  tty29  tty55      vcs6      video15
fd               mmcblk0p1     shm      tty3   tty56      vcs7      video16
full             mmcblk0p2     snd      tty30  tty57      vcsa      video18
fuse             mqueue        stderr   tty31  tty58      vcsa1     video19
gpiochip0        net           stdin    tty32  tty59      vcsa2     video20
gpiochip1        null          stdout   tty33  tty6       vcsa3     video21
gpiomem          port          tty      tty34  tty60      vcsa4     video22
hwrng            ppp           tty0     tty35  tty61      vcsa5     video23
i2c-1            ptmx          tty1     tty36  tty62      vcsa6     video31
initctl          pts           tty10    tty37  tty63      vcsa7     watchdog
input            ram0          tty11    tty38  tty7       vcsm-cma  watchdog0
kmsg             ram1          tty12    tty39  tty8       vcsu      zero
kvm              ram10         tty13    tty4   tty9       vcsu1
log              ram11         tty14    tty40  ttyAMA0    vcsu2
loop0            ram12         tty15    tty41  ttyprintk  vcsu3
"""

var2 = """ashmem           loop1         ram13    tty16  tty42      ttyS0     vcsu4
autofs           loop2         ram14    tty17  tty43      uhid      vcsu5
block            loop3         ram15    tty18  tty44      uinput    vcsu6
btrfs-control    loop4         ram2     tty19  tty45      urandom   vcsu7
bus              loop5         ram3     tty2   tty46      v4l       vga_arbiter
cachefiles       loop6         ram4     tty20  tty47      vchiq     vhci
char             loop7         ram5     tty21  tty48      vcio      vhost-net
console          loop-control  ram6     tty22  tty49      vc-mem    vhost-vsock
cpu_dma_latency  mapper        ram7     tty23  tty5       vcs       video0
cuse             media0        ram8     tty24  tty50      vcs1      video10
disk             media1        ram9     tty25  tty51      vcs2      video11
dma_heap         media2        random   tty26  tty52      vcs3      video12
dri              media3        rfkill   tty27  tty53      vcs4      video13
fb0              mem           serial0  tty28  tty54      vcs5      video14
fb1              mmcblk0       serial1  tty29  tty55      vcs6      video15
fd               mmcblk0p1     shm      tty3   tty56      vcs7      video16
full             mmcblk0p2     snd      tty30  tty57      vcsa      video18
fuse             mqueue        stderr   tty31  tty58      vcsa1     video19
gpiochip0        net           stdin    tty32  tty59      vcsa2     video20
gpiochip1        null          stdout   tty33  tty6       vcsa3     video21
gpiomem          port          tty      tty34  tty60      vcsa4     video22
hwrng            ppp           tty0     tty35  tty61      vcsa5     video23
i2c-1            ptmx          tty1     tty36  tty62      vcsa6     video31
initctl          pts           tty10    tty37  tty63      vcsa7     watchdog
input            ram0          tty11    tty38  tty7       vcsm-cma  watchdog0
kmsg             ram1          tty12    tty39  tty8       vcsu      zero
kvm              ram10         tty13    tty4   tty9       vcsu1
log              ram11         tty14    tty40  ttyAMA0    vcsu2
loop0            ram12         tty15    tty41  ttyprintk  vcsu3
"""


if var == var2: 
    print(True)
else: 
    print(False)