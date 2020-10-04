from .infraredsensor import InfraRedSensor
import pubsub.pub as pub

from ..logger.logger import LOG


class LineInfraRedSensor(InfraRedSensor):

    def __init__(self, position, pin):
        super(LineInfraRedSensor, self).__init__(position, pin)

    def _ir_sensor_event(self):
        self._state = True
        pub.sendMessage("line_ir_sensor_event", position=self._position)
