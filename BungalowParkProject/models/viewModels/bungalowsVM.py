from enums.messageType import MessageType
from .baseVM import BaseVM

class BungalowsVM(BaseVM):
    """
        View model for the bungalows.html view, 
        contains all possible data which can be used to construct the view.
    """

    # Bungalows are grouped by 3 for ease of displaying.
    grouped_bungalows = []
