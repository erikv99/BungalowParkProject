from .baseVM import BaseVM
from enums.messageType import MessageType

class ChangeTypeVM(BaseVM):
    """
        View model for the changeType.html view, 
        contains all possible data which can be used to construct the view.
    """

    bungalow = None
    reservation = None
    grouped_available_bungalows = None