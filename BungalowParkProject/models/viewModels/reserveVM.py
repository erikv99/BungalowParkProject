from .viewModelBase import ViewModelBase
from enums.messageType import MessageType

class ReserveVM(ViewModelBase):
    """
        View model for the reserve.html view, 
        contains all possible data which can be used to construct the view.
    """

    message_type = MessageType.NONE
    message_content = ""
    bungalow = None
    bungalow_type = None

