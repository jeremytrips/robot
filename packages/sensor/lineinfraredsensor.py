from .infraredsensor import InfraRedSensor
import pubsub.pub as pub

from ..logger.logger import LOG


class LineInfraRedSensor(InfraRedSensor):

    def __init__(self, position, pin):
        self.__type = "Line"
        super(LineInfraRedSensor, self).__init__(position, pin)

    def _ir_sensor_event(self, pin):
        pub.sendMessage("line_ir_sensor_event", position=self._position)

    def get_state(self):
        return f"ir sensor {self._position} {self.__type} \t\t {self.state}"
