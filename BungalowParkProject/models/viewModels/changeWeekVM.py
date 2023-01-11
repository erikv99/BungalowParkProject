from .baseVM import BaseVM
from enums.messageType import MessageType

class ChangeWeekVM(BaseVM):
    """
        View model for the changeWeek.html view, 
        contains all possible data which can be used to construct the view.
    """

    bungalow = None
    reservation = None