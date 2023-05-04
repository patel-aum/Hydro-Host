import argparse
import time
import RPi.GPIO as GPIO
## Problem was using 5v instead of 3.3v

class ExternalDevice():
    """docstring for ExternalDevice. 
    name: (string) Identification for specific device.
    max_value: (int) Longest time in seconds that the device should ever be in its active state
    """
    def __init__(self, name, GPIO_pin_num, max_value):
        self.name = name
        self.pin_num = int(GPIO_pin_num)
        self.max_value = max_value
        self.state_file = '.{}_state'.format(self.name)
        self.state = self.get_state(verbose=True)
        
        
    def pin_off(self):
        print('running pin off class method and cleaning up.')
        GPIO.output(self.pin_num, GPIO.LOW) # turn device off
        GPIO.cleanup()
        
    def pin_on(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin_num)
        GPIO.output(self.pin_num, GPIO.HIGH) # turn device on
        pin_off()

    def get_state(self, verbose=True):
        try:
            with open(self.state_file, 'r') as f:
                device_state = f.read(1)
                if verbose:
                    print("Device state is: {}".format(device_state))
        except:
            with open(self.state_file, 'w+') as f:
                print("Creating device state file and setting to 0.")
                device_state = '0'
                f.write(device_state)
        return device_state
                
    
    def start_device(self, duration=0):
        if self.get_state() == '0':
            with open(self.state_file, 'w') as f:
                print('{} state set to start (1)'.format(self.name))
                f.write('1')
                self.state = '1'
                self.pin_on()
                time.sleep(duration)
                
        elif self.get_state() == '1':
            self.state = '1'
            print('{} already on. State file was set at 1.'.format(self.name).format(self.name))
            self.pin_on()
            time.sleep(duration)
            
            
        else:
            with open(self.state_file, 'w+') as f:
                f.write('1')
                self.state = '1'
                print('State for {} was not present.', '\n', 'Created state file and set to 1.')
                self.pin_on()
                time.sleep(duration)
                
            
    def stop_device(self):
        if self.get_state() == '0':
            self.state = '0'
            print('{} already off. State file was set at 0.'.format(self.name))
            self.pin_off()
        
        elif self.get_state() == '1':
            with open(self.state_file, 'w') as f:
                f.write('0')
                self.state = '0'
                print('Set file for {} to 0'.format(self.name))
                self.pin_off()
        else:
            with open(self.state_file, 'w+') as f:
                state.write('0')
                self.state = '0'
                print('State file for {} was not present.', '\n', 'Created state file and set to 1.'.format(self.name))
                self.pin_off()

if __name__ == '__main__':
    try:
        pump_parser = argparse.ArgumentParser(description='Setup devices to be controlled')
        pump_parser.add_argument('-d', '--Duration', required=True, type=int, help='Enter duration in secs for pump to run.')
        pump_parser.add_argument('-p', '--GPIO_pin', required=True, type=int, help='Enter the number of the GPIO pin (BOARD) to which the pump is attached.')
        pump_args = pump_parser.parse_args()
        pump_duration = pump_args.Duration
        gpio_pin_num = pump_args.GPIO_pin
        #GPIO.setmode(GPIO.BOARD)
        #GPIO.setup(gpio_pin_num, GPIO.OUT)
        print('Creating devices...')
        print('About to start pump for {} seconds on GPIO pin number {} (BOARD layout numbering scheme).'.format(pump_duration, gpio_pin_num))
        
        water_pump = ExternalDevice('water pump', gpio_pin_num, 600) # max duration is not implemented yet
        water_pump.start_device(pump_duration)
        
        print('Cycle complete, cleaning up.')
        GPIO.cleanup()
        print('Clean up complete.')
        
    except KeyboardInterrupt:
        GPIO.cleanup()
        print('Keyboard interrupt received, gracefully stopped.')
        