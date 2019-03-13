import abc

class IAIBehaviourHandler(abc.ABC):
    @abc.abstractmethod
    def onIaHasPredicted(self, segmentBuff):
        pass
