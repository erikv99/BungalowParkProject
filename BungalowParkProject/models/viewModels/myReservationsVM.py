from enums.messageType import MessageType
from .viewModelBase import ViewModelBase

class MyReservationVM(ViewModelBase):
    """
        View model for the myReservations.html view, 
        contains all possible data which can be used to construct the view.
    """

    # reserverd bungalows are grouped by 3 for ease of displaying.
    grouped_bungalows = []
    has_reservations = True
    reservation_ids = {}
    message_type = MessageType.NONE
    message_content = ""