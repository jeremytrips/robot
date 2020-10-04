from .infraredsensor import InfraRedSensor
from pubsub import pub


class JunctionInfraRedSensor(InfraRedSensor):

    def __init__(self, position, pin):
        super(JunctionInfraRedSensor, self).__init__(position, pin)
    
    def _ir_sensor_event(self):
        pub.sendMessage("junction_ir_sensor_event", position=self._position)
