from .baseVM import BaseVM

class ReserveVM(BaseVM):
    """
        View model for the reserve.html view, 
        contains all possible data which can be used to construct the view.
    """

    bungalow = None
    bungalow_type = None

