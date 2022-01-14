class Jacht:
    jacht_id: str  # id
    name: str
    price: float
    desc: str
    reservation: list

    def __init__(self, jacht=None):
        self.jacht_id: str
        self.name: str
        self.price: float
        self.desc: str
        self.reservation: list

        if jacht is not None:
            self.jacht_id = jacht["jacht"] if jacht["jacht"].__contains__("index") else f"{str(jacht['jacht'])}-index"
            self.name = jacht["name"]
            self.price = jacht["price"]
            self.desc = jacht["desc"]
            self.reservation = jacht["reservation"]

    def set_example_values(self, jacht_id, name, price):
        self.jacht_id = jacht_id
        self.name = name
        self.price = price
        self.desc = "example desc, with some <b>html</b>"
        self.reservation = []

    def get_item(self):
        return {
            'jacht': self.jacht_id,
            'name': self.name,
            'price': self.price,
            'desc': self.desc,
            'reservation': self.reservation
        }

    def set_new_reservation(self, od, do, email):
        self.reservation.append({'od': od, 'do': do, 'email': email})

    def remove_reservation(self, reservation: dict):
        self.reservation.remove(reservation)
