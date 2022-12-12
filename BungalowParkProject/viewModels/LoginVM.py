from BungalowParkProject.enums.MessageType import MessageType
from BungalowParkProjectviewModels.ViewModelBase import ViewModelBase

class LoginVM(ViewModelBase):
    """
        View model for the login.html view, 
        contains all possible data which can be used to construct the view.
    """

    message_type = MessageType.NONE
    message_content = ""




