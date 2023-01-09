from .viewModelBase import ViewModelBase
from enums.messageType import MessageType

class ChangeTypeVM(ViewModelBase):
    """
        View model for the changeType.html view, 
        contains all possible data which can be used to construct the view.
    """

    message_type = MessageType.NONE
    message_content = ""
    bungalow = None
    reservation = None
    available_bungalows = None