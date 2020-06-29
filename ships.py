class Ship:
    def __init__(self, name, size, ship_id):
        self.name = name
        self.id = ship_id
        self.size = size
        self.location = []
        self.alive = True

    def in_place(self, gird):
        for loc in self.location:
            gird[loc[0]][loc[1]] = loc[2]
