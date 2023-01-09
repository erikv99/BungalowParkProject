from enums.messageType import MessageType
from .viewModelBase import ViewModelBase

class BungalowsVM(ViewModelBase):
    """
        View model for the bungalows.html view, 
        contains all possible data which can be used to construct the view.
    """

    # Bungalows are grouped by 3 for ease of displaying.
    grouped_bungalows = []

    message_type = MessageType.NONE
    message_content = ""
