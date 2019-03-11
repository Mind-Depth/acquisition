import abc
import sip

class IGraphicalUpdateHandlerFinalMeta(sip.wrappertype, abc.ABCMeta):
    pass

class IGraphicalUpdateHandler(abc.ABC):
    @abc.abstractmethod
    def onGraphUpdate(self):
        pass