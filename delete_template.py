import json
from pyfingerprint.pyfingerprint import PyFingerprint

# Function to delete fingerprint template from sensor
def delete_fingerprint_template(position_number):
    try:
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
        if not f.verifyPassword():
            raise ValueError('The given fingerprint sensor password is wrong!')
        
        if f.deleteTemplate(position_number):
            print(f'Fingerprint template at position {position_number} deleted successfully!')
        else:
            print('Failed to delete the fingerprint template.')
    
    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))


# Function to delete Aadhaar ID and corresponding fingerprint template from JSON file
def delete_from_json(aadhaar_id):
    try:
        with open('fingerprint_database.json', 'r') as f_db:
            data = f_db.readlines()
        
        with open('fingerprint_database.json', 'w') as f_db:
            for line in data:
                fingerprint_data = json.loads(line)
                if isinstance(fingerprint_data, list) and len(fingerprint_data) > 0:
                    fingerprint_data = fingerprint_data[0]
                if aadhaar_id in fingerprint_data:
                    position_number = fingerprint_data[aadhaar_id]
                    delete_fingerprint_template(position_number)
                else:
                    f_db.write(line)

    except FileNotFoundError:
        print('Database file not found.')

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))


# Main function
def main():
    aadhaar_id = input('Enter Aadhaar number to delete its fingerprint template: ')
    delete_from_json(aadhaar_id)


if __name__ == "__main__":
    main()
