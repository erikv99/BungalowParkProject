from .baseVM import BaseVM

class MyReservationVM(BaseVM):
    """
        View model for the myReservations.html view, 
        contains all possible data which can be used to construct the view.
    """

    # reserverd bungalows are grouped by 3 for ease of displaying.
    grouped_bungalows = []