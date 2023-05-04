class ExternalDevice():
    """docstring for ExternalDevice"""
    def __init__(self, name, max_value):
        self.name = name
        self.max_value = max_value

    def get_state(self, filepath):
        try:
            with open(filepath) as state:
                device_state = state.read(1)
                assert device_state is in set(int(0,1)),
                'State must consist of a single 0 or 1'

                print("Device state is: {}".format(device_state))
                return state
        except:
            with open(filepath, 'a') as state:
                print("Creating device state file and setting to 0.")
                state.
