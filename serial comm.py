from fingerprint import FingerprintIO
from time import sleep
import pickle

print("    ____            ____           __      __  ___                                 \n"
      "   / __ \____ _____/ / /___  _____/ /__   /  |/  /___ _____  ____ _____ ____  _____\n"
      "  / /_/ / __ `/ __  / / __ \/ ___/ //_/  / /|_/ / __ `/ __ \/ __ `/ __ `/ _ \/ ___/\n"
      " / ____/ /_/ / /_/ / / /_/ / /__/ ,<    / /  / / /_/ / / / / /_/ / /_/ /  __/ /    \n"
      "/_/    \__,_/\__,_/_/\____/\___/_/|_|  /_/  /_/\__,_/_/ /_/\__,_/\__, /\___/_/     \n"
      "                                                                /____/             \n"
      ">> Hello Guyz ;) <<\n"
      "Welcome to Fingerprint Padlock interface.\n"
      "Software ver alpha 0.1\n"
      "Credits: Fikri Rida Pebriansyah (@friansh)\n")

serial = FingerprintIO()

padDevice = serial.scanPort( )

device = []
while len(padDevice) == 0:
    input("There is no padlock device connected.\n"
          "Please connect the device, then press enter to rescan...\n")
    padDevice = serial.scanPort()

if (len(padDevice) == 1):
    device = padDevice[0]
else:
    print("Possible more than 1 devices connected. User override required.\n")
    inputDevice = int(input("Which is your device?\n>>> ")) - 1
    device = padDevice[inputDevice]

print("\nPossible padlock device port: " + str(device) );
serial.connect_port( device )

user = []

def listen():
    while True:
        if (serial.data == "Done!" or serial.data == "Failed, ready to try again." ):
            sleep(.2)
            serial.flush()
            sleep(.2)
            mainMenu()
            break

        serial.read()

def mainMenu():
    while True:
        command = input(">>> ")
        if ( command == "exit" ):
            serial.close_port()
            exit()
            break

        if ( command == "help" ):
            print("Padlock Manager Interface Command list. \n"
                  "Commands available for use:\n"
                  "\thelp\t\tshow this help\n"
                  "\tstatus\t\tcheck status of your fingerprint padlock\n"
                  "\tregister\tregister new user to database\n"
                  "\tdelete\t\tdelete exisitng user from database\n"
                  "\tscan\t\tdebug the fingerprint scanning activity\n"
                  "\tclean\t\twipe out the registered fingerprint database\n"
                  "\texit\t\texit this program\n")
            mainMenu()

        serial.write(command)
        serial.read()

        recvd = " request received."
        if (serial.data == "Registration" + recvd or
            serial.data == "Deletion" + recvd or
            serial.data == "Entering biometric scan debug mode."):
            listen()
            break

if (serial.data == "aingmacan;)"):
    print("\nPadlock confirmed at " + str(padDevice) + ".\n"
          "Ready for another instructions, enter 'help' to show the manual...")
    mainMenu()
