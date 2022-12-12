from BungalowParkProject.enums.MessageType import MessageType
from BungalowParkProjectviewModels.ViewModelBase import ViewModelBase

class RegisterVM(ViewModelBase):
    """
        View model for the register.html view, 
        contains all possible data which can be used to construct the view.
    """

    message_type = MessageType.NONE
    message_content = ""