from .baseVM import BaseVM

class ErrorVM(BaseVM):
    """
        View model for the error.html view, 
        contains all possible data which can be used to construct the view.
    """

    message = ""
    error_code = None
    