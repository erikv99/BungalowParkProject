from __main__ import db

class PopulateHelper():

    def Populate(self):
        """
            Will populate the database with initial values needed for funcitoning.
        """

        self._populate_bungalow_types()
        self._populate_bungalows()

    def _populate_bungalow_types(self):
        """
            Makes sure that on first creation of the db the bungalow types are populated
        """

        from models.databaseModels.bungalowType import BungalowType
        result = BungalowType.query.all()

        # There are 3 types of bungalows, if not found in db we will create them.
        if len(result) != 3:
            
            print("Populating bungalow types...")
            type_small = BungalowType(week_price=199.99, size=4)
            type_medium = BungalowType(week_price=299.99, size=6)
            type_large = BungalowType(week_price=399.99, size=8)
            db.session.add_all([type_small, type_medium, type_large])
            db.session.commit()

    def _populate_bungalows(self):
        """
            Makes sure that on first creation of the db the available bungalow types are populated.

            Note: at one point the creation of new available bungalows will become responsibility of admins.
        """

        from models.databaseModels.bungalow import Bungalow
        result = Bungalow.query.all()

        if len(result) == 0:
            
            print("Populating available bungalows...")

            bugalows = \
                [\
                Bungalow(type_id=1, unique_name="Sea side small",  img_file_name="bungalow_01.jpg"),\
                Bungalow(type_id=1, unique_name="Mountain side small",  img_file_name="bungalow_02.jpg"),\
                Bungalow(type_id=2, unique_name="Sea side medium",  img_file_name="bungalow_03.jpg"),\
                Bungalow(type_id=2, unique_name="Mountain side medium",  img_file_name="bungalow_04.jpg"),\
                Bungalow(type_id=3, unique_name="Sea side large",  img_file_name="bungalow_05.jpg"),\
                Bungalow(type_id=3, unique_name="Mountain side large",  img_file_name="bungalow_06.jpg"),\
                ]

            db.session.add_all(bugalows)
            db.session.commit()