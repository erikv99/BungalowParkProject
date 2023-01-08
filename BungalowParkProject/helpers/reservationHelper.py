import datetime

class ReservationHelper():

    def _divide_in_trios(self, bungalows):
        # Looping through a range of 0 -> len(bungalows) in steps of 3
        # notice we use yield, this means the function is a generator and can only by iterated once. 
        for i in range(0, len(bungalows), 3):
            yield bungalows[i:i + 3]

    def GetWeekNumber(self, dt):
        """
            Returns the weeknumber of the given datetime
        """
        return datetime.date(dt.year, dt.month, dt.day).isocalendar().week

    def GetGroupedBungalows(self, bungalows):

        # Getting a list containing multiple list containing each 3 list (or the remainer)
        return self._divide_in_trios(bungalows)
