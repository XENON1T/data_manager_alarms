from pagerduty_api import Alert
import subprocess
import os
import sys
import time

if os.environ.get('PAGERDUTY_API_KEY_STORAGE') is None:
    print("Set key!")
    sys.exit()

def storage(limit=60):
    my_key = 'PAGERDUTY_API_KEY_STORAGE'
    if os.environ.get(my_key) is None:
        print("Set environmental variable", my_key)
        sys.exit()
    
    output = subprocess.check_output("/srv/adm/gpfsquota")

    for line in str(output).split('\\n'):
        parts = line.split()
        if parts[0] == 'project-lgrandi': 
            if float(parts[3]) > limit:
                print("Triggered alarm", parts[3])
                alert = Alert(service_key=os.environ.get(my_key))
                
                alert.trigger(
                    description='Midway more than %d terabyte' % limit,
                    client='data_manager_alarms',
                    client_url='https://github.com/XENON1T/data_manager_alarms',
                    details={'Current storage': parts[3]}
                )

def cax_running():
    my_key = 'PAGERDUTY_API_KEY_CAX'
    if os.environ.get(my_key) is None:
        print("Set environmental variable", my_key)
        sys.exit()
    
    output = str(subprocess.check_output(["ps", "-A"]))
    if "massive-cax" not in output:
        print("Triggered alarm nocax")
        alert = Alert(service_key=os.environ.get(my_key))
        
        alert.trigger(
            description='Midway is not running massive cax',
            client='data_manager_alarms',
            client_url='https://github.com/XENON1T/data_manager_alarms',
            details={'ps output': output},
        )


while 1:
    
    cax_running()

    storage(limit=60)

    time.sleep(60*60)

