class ReservationBungalowDto():

    id = None
    type_id = None
    unique_name = None
    img_file_name = None
    type = None
    reservation_id = None

    def __repr__(self):
        return "Bungalow\nid: {}\ntype_id: {}\nunique_name: {}\nimg_file_name: {}" \
            .format(self.id, self.type_id, self.unique_name, self.img_file_name)