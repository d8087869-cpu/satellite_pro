import time
from space_network_lib import *

class Satellite(SpaceEntity):
    def __init__(self, name, distance_from_earth):
        super().__init__(name, distance_from_earth)

    def receive_signal(self, packet):
        print(f"[{self.name}] Received: {packet}.") 


class BrokenConnectionError(Exception):
    pass


def attempt_transmission(packet):
    valid = False
    while not valid :

        try:
            network.send(packet)
            valid =True

        except TemporalInterferenceError:
            print('interface, waiting...')
            time.sleep(2)
            
        except DataCorruptedError:
            print('data corrupted, retrying...')

        except LinkTerminatedError:
            print('link lost')
            raise BrokenConnectionError("Connection permanently broken")
        
        except OutOfRangeError:
            print('target out of range')
            raise BrokenConnectionError("Connection permanently broken")


network = SpaceNetwork(level=3)
sat1 = Satellite("sat1" , 100)
sat2 = Satellite("sat2" , 200)
packet = Packet("Hello from Sat1!", sat1, sat2)

try:
    attempt_transmission(packet)
except BrokenConnectionError:
    print("Transmission failed.")

