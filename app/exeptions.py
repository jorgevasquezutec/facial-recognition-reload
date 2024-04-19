class FaceNotFound(Exception):
    def __init__(self, message = "Face not found in the image"):
        self.message = message
        super().__init__(self.message)


class FaceNotMatched(Exception):
    def __init__(self, message = "Face not matched"):
        self.message = message
        super().__init__(self.message)

class ManyFacesFound(Exception):
    def __init__(self, message = "Many faces found in the image"):
        self.message = message
        super().__init__(self.message)

