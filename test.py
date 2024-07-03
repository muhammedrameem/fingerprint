import time
import json
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

# Load the fingerprint database
fingerprint_data = {}
with open('fingerprint_database.json', 'r') as f_db:
    for line in f_db:
        try:
            data = json.loads(line)
            fingerprint_data.update(data)
        except json.JSONDecodeError:
            print("Error decoding JSON:", line)

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

        # Convert the obtained fingerprint template to a list
        sensor_template_data = list(f.downloadCharacteristics(0x01))

        # Compare the fingerprint template obtained from the sensor with templates from the JSON file
        for aadhaar, stored_template_data in fingerprint_data.items():
            if stored_template_data == sensor_template_data:
                print('Fingerprint matched with Aadhaar number:', aadhaar)
                return

        print('Fingerprint does not match with any Aadhaar number in the database.')

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))

# Verify the fingerprint
verify_fingerprint()
