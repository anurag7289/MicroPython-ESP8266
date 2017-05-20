import network
import ubinascii
import machine
import time
import ssd1306
import dht

wssid = "Unavailable_V2"
password = "megagame00007"
ledpin = 2

i2c = machine.I2C(-1, scl=machine.Pin(5), sda=machine.Pin(4))
oled=ssd1306.SSD1306_I2C(128, 64, i2c)
oled.poweron()
oled.init_display()
oled.fill(0)
d = dht.DHT11(machine.Pin(13))
time.sleep(2)
temp=''
hum=''
cdisp=temp+' / '+hum
count=0


def blinkStatus():
    led = machine.Pin(ledpin, machine.Pin.OUT)
    for i in range(ledpin):
        led.low()
        time.sleep_ms(500)
        led.high()
        time.sleep_ms(500)

def wifiScan():
    print('Scanning  wifi..')
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    print("MAC Address :")
    mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
    print(mac)
    print()
    list=sta.scan()
    print(".... SSID and BSSID .....")
    for i in list:
        print(i[0])    
        print(i[1])
        print()
    blinkStatus()
    print("Scan Completed")    

def wifiConnect():
    print('Connecting to wifi..')
    sta = network.WLAN(network.STA_IF)
    sta.active(False)
    time.sleep(3)
    sta.active(True)
    sta.connect(wssid, password)
    time.sleep(5)
    if sta.isconnected():
        print('Connected to ')
        print(wssid)
        blinkStatus()
		
def tempHum():
    while True:
        oled.scroll(0, count)
        if count== -5:
            d.measure()
            temp='T: '+str(d.temperature())+' C'
            hum='H: '+str(d.humidity())+' % RH'
            cdisp=temp+' / '+hum
            print(cdisp)    # eg. 41 (% RH)        
            oled.text(str(cdisp), 0, 30)            
            count=0    
        oled.show()
        time.sleep(5)
        print(count)
        count=count-1

wifiScan()
wifiConnect()
tempHum()
