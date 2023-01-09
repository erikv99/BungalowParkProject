from enums.messageType import MessageType
from .viewModelBase import ViewModelBase

class AdminVM(ViewModelBase):
    """
        View model for the admmin.html view, 
        contains all possible data which can be used to construct the view.
    """
    
    message_type = MessageType.NONE
    message_content = ""