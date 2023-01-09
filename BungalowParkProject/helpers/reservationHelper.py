import datetime
from flask import session
from models.dataTransferObjects.reservationBungalowDto import ReservationBungalowDto
from models.databaseModels.reservation import Reservation


class ReservationHelper():

    def _divide_in_trios(self, bungalows):
        # Looping through a range of 0 -> len(bungalows) in steps of 3
        # notice we use yield, this means the function is a generator and can only by iterated once. 
        for i in range(0, len(bungalows), 3):
            yield bungalows[i:i + 3]

    def _get_reservations(self):
        """
            Returns a list containing all reservations for the current logged in user.
        """

        return Reservation.query.filter(Reservation.user_id == session["user_id"]).all()

    def GetWeekNumber(self, dt):
        """
            Returns the weeknumber of the given datetime
        """
        return datetime.date(dt.year, dt.month, dt.day).isocalendar().week

    def GetGroupedBungalows(self, bungalows):

        # Getting a list containing multiple list containing each 3 list (or the remainer)
        return self._divide_in_trios(bungalows)

    def GetGroupedReservations(self):
        """
            Returns the grouped (by 3) list of bungalowDto's
            Used to build the view for the myReservations.html view
        """
        bungalowDtos = []
        reservations = self._get_reservations()

        # Each bungalow here is a data transfer object which has a slight modification on the the original bungalow database model,
        # Reason for this is we need the reservation id for each displayed bungalow so we can use cancel functionalitity
        for reservation in reservations:

            reservation_bungalow_dto = ReservationBungalowDto()
            reservation_bungalow_dto.id = reservation.bungalow.id
            reservation_bungalow_dto.img_file_name = reservation.bungalow.img_file_name
            reservation_bungalow_dto.type = reservation.bungalow.type
            reservation_bungalow_dto.type_id = reservation.bungalow.type_id
            reservation_bungalow_dto.unique_name = reservation.bungalow.unique_name
            reservation_bungalow_dto.reservation_id = reservation.id
            reservation_bungalow_dto.week_number = reservation.reserveration_week_number
            bungalowDtos.append(reservation_bungalow_dto)

        # Making sure the bungalow dto's are grouped by groups of 3 for displaying purposes.
        return ReservationHelper().GetGroupedBungalows(bungalowDtos)

