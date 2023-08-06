class DO_Behaivour:
    def __init__(self, bounce_from_borders_friction = -1, gravity = -1,
    air_friction = -1):
        self.bounce_from_borders_friction = bounce_from_borders_friction
        self.gravity = gravity
        self.air_friction = air_friction

    @classmethod
    def STANDART(cls):
        return cls()

class DO_Image:
    def __init__(self, shape_type: str = "circle", **kwargs):
        self.shape_type = shape_type

        self.color = kwargs["color"]
        if shape_type == "circle":
            self.dx = kwargs["d"] / 2
            self.dy = kwargs["d"] / 2
        elif shape_type == "rectangle":
            self.dx = kwargs["width"] / 2
            self.dy = kwargs["height"] / 2
        else:
            raise ValueError("shape_type must be 'rectangle' or 'circle'")

    @classmethod
    def STANDART(cls):
        return cls("circle", d = 10, color = "red")