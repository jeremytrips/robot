from .infraredsensor import InfraRedSensor
from pubsub import pub


class JunctionInfraRedSensor(InfraRedSensor):

    def __init__(self, position, pin):
        self.__type = "junction"
        super(JunctionInfraRedSensor, self).__init__(position, pin)
    
    def _ir_sensor_event(self, pin):
        pub.sendMessage("junction_ir_sensor_event", position=self._position)

    def get_state(self):
        return f"\033[92mir sensor {self._position} {self.__type}\033[0m\t\t {self.state}"
