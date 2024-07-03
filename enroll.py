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

# Link Aadhaar number to the fingerprint template
aadhaar_number = input('Enter Aadhaar number to link with the fingerprint template: ')

## Tries to enroll a new fingerprint
try:
    print('Waiting for finger...')

    ## Wait until finger is read
    while not f.readImage():
        pass

    ## Convert read image to characteristics and store it in charbuffer 1
    f.convertImage(0x01)

    ## Check if finger is already enrolled
    result = f.searchTemplate()
    positionNumber = result[0]

    if positionNumber >= 0:
        print('Template already exists at position #' + str(positionNumber))
        exit(0)

    print('Remove finger...')
    time.sleep(2)

    print('Waiting for the same finger again...')
    print(f.readImage())
    ## Wait until finger is read again
    while not f.readImage():
        pass

    ## Convert read image to characteristics and store it in charbuffer 2
    f.convertImage(0x02)

    ## Create a template
    f.createTemplate()

    ## Save template at a new position number
    positionNumber = f.storeTemplate()
    print('Fingerprint enrolled successfully!')
    print('New template position #' + str(positionNumber))

    # Get the enrolled fingerprint template data
    template_data = f.downloadCharacteristics(0x01)

    # Store the fingerprint template data along with the Aadhaar number in a dictionary
    fingerprint_data = {aadhaar_number: template_data}

    # Write the dictionary to a JSON file
    with open('fingerprint_database.json', 'a') as f_db:
        json.dump(fingerprint_data, f_db)
        f_db.write('\n')

    print('Fingerprint template linked with Aadhaar number successfully!')

except Exception as e:
    print('Operation failed!')
    print('Exception message: ' + str(e))
    exit(1)
