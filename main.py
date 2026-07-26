import time
from space_network_lib import *

class Satellite(SpaceEntity):
    def __init__(self, name, distance_from_earth):
        super().__init__(name, distance_from_earth)

    def receive_signal(self, packet):
        print(f"[{self.name}] Received: {packet}.")


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
            

network = SpaceNetwork(level=2)
sat1 = Satellite("sat1" , 100)
sat2 = Satellite("sat2" , 200)
packet = Packet("Hello from Sat1!", sat1, sat2)
attempt_transmission(packet)