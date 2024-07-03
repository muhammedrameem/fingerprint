import time
from pyfingerprint.pyfingerprint import PyFingerprint

## Tries to initialize the sensor
try:
    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

    if not f.verifyPassword():
        raise ValueError('The given fingerprint sensor password is wrong!')

except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    print('Exception message: ' + str(e))
    exit(1)

## Gets some sensor information
print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

# Function to verify fingerprint
def verify_fingerprint():
    try:
        print('Waiting for finger...')

        ## Wait until finger is read
        while not f.readImage():
            pass

        ## Convert read image to characteristics and store it in charbuffer 1
        f.convertImage(0x01)

        ## Search for the template
        result = f.searchTemplate()
        positionNumber = result[0]

        if positionNumber == -1:
            print('No match found!')
            return

        print('Fingerprint found at position #' + str(positionNumber))
        print('Please remove the finger.')

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))

# Verify the fingerprint
verify_fingerprint()
