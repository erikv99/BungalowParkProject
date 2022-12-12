
from abc import ABC, abstractmethod

class ViewModelABC(ABC):
    """
        Abstract base class for all viewModels. 

        Tells the ViewModels which ... they should always have.
    """

    # Abstract property, this means every ViewModel should have this property.
    @property
    @abstractmethod
    def isLoggedIn(self) -> bool:
        pass
