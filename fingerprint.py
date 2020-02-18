import datetime as dt
import serial as s
import serial.tools.list_ports as listPorts
from time import sleep

class FingerprintIO:
    vid          = "1003"
    pid          = "28264"
    greetings    = "who are you?"
    serialConn   = s.Serial
    baud         = 9600
    data         = ""
    device       = ""

    def printWithTime(self, text):
        print("[" + str(dt.datetime.now().strftime("%X")) + "] " + text)

    def scanPort(self):
        print("Please wait while we are scanning for your device...\n")
        ports = listPorts.comports()
        devices = []
        print("Found " + str( len(ports) ) + " device(s):")
        n = 0
        for p in ports:
            try:
                print(str(n + 1) + ". " + p.device + " - " + p.description + " (" + str(p.vid) + ":" + str(p.pid) + ")")
                if (str(p.vid) == self.vid and str(p.pid) == self.pid):
                    devices.append(p.device)
            except:
                print(str(n + 1) + ". " + "Device is busy")
            n += 1
        return devices

    def connect_port(self, devices):
        self.device = devices
        print("Connecting to " + devices + "...")
        try:
            self.serialConn = s.Serial(devices, self.baud)
            if not self.serialConn.isOpen():
                self.serialConn.open()
            print("Port opened. Sleep 3s, waiting for device...\n")
            sleep(3)
            self.call(devices)
        except:
            print("The device is busy, retrying in 5 secs...\n")
            sleep(5)
            self.connect_port(devices)

    def close_port(self):
        self.serialConn.close()
        print("\nGood bye :*, exiting...")

    def write(self, command):
        self.serialConn.write( command.encode() )

    def call(self, device):
        print("Initializing transmission.\n"
              ">> " + self.greetings)
        self.serialConn.write( self.greetings.encode() )
        self.read()

    def read(self):
        self.data = self.serialConn.readline().decode().strip()
        self.printWithTime(self.data)

    def flush(self):
        self.serialConn.flush()
