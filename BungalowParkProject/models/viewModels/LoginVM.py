from enums.messageType import MessageType
from .viewModelBase import ViewModelBase

class LoginVM(ViewModelBase):
    """
        View model for the login.html view, 
        contains all possible data which can be used to construct the view.
    """

    message_type = MessageType.NONE
    message_content = ""