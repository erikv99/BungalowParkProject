from models.databaseModels.reservation import Reservation
from models.databaseModels.bungalow import Bungalow

class ReservationHelper():

    def GetGroupedBungalows(self):
        """
            Returns a list containing one or more list of each containing 3 bungalows (or the remainder.)
        """

        # Getting all id's of reserved bungalows using list extension on the result tuple to create a flat list
        reserved_bungalows_ids = [tuple_entry[0] for tuple_entry in Reservation.query.with_entities(Reservation.bungalow_id).all()]
    
        # Getting all bungalows which are not reserved
        bungalows = Bungalow.query.filter(Bungalow.id.not_in(reserved_bungalows_ids)).all()

        # Getting a list containing multiple list containing each 3 list (or the remainer)
        return self._divide_in_trios(bungalows)
        
    def _divide_in_trios(self, bungalows):
        # Looping through a range of 0 -> len(bungalows) in steps of 3
        # notice we use yield, this means the function is a generator and can only by iterated once. 
        for i in range(0, len(bungalows), 3):
            yield bungalows[i:i + 3]

    def GetWeekNumber():
        """
            Returns the weeknumber of the given datetime
        """
        pass