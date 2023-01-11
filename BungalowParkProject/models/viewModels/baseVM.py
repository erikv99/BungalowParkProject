from enums.messageType import MessageType

class BaseVM():
    """
        Base class for all viewModels. 

        Contains for example data all view models should have.
    """

    is_logged_in = False
    user_id = -1
    message_type = MessageType.NONE
    message_content = ""