import time
from space_network_lib import *

class Satellite(SpaceEntity):
    def __init__(self, name, distance_from_earth):
        super().__init__(name, distance_from_earth)

    def receive_signal(self, packet):
        print(f"[{self.name}] Received: {packet}.") 

        if isinstance(packet,RelayPacket):
            inner_packet = packet.data 
            print('Unwrapping and forwarding to {inner_packet.receiver}')
            attempt_transmission(inner_packet)
        else:
            print("Final destination reached: {packet.data}")


class Earth(SpaceEntity):
    def __init__(self, name, distance_from_earth):
        super().__init__(name, distance_from_earth)

    def receive_signal(self, packet):
        pass





class BrokenConnectionError(Exception):
    pass

class RelayPacket(Packet):
    def __init__(self, packet_to_realy, sender,proxy):
        super().__init__(packet_to_realy, sender,proxy)

    def __repr__(self):
        return f"RelayPacket(Relaying [{self.data}] to {self.receiver} from {self.sender})"
    


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

earth = Earth('earth', 0)

sat1 = Satellite("sat1" , 100)
sat2 = Satellite("sat2" , 200)
#packet = Packet("Hello from Sat1!", sat1, sat2)

p_final = Packet('Hello from Earth !!',sat1, sat2)
p_earth_to_sat1=RelayPacket(p_final,earth,sat1)

try:
    attempt_transmission(p_earth_to_sat1)
except BrokenConnectionError:
    print("Transmission failed.")

