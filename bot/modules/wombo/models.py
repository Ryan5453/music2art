from copy import copy

class Dream:
    def __init__(self, payload: dict) -> None:
        self.payload = payload

    @property
    def image(self) -> str:
        return self.payload["result"]

    @property
    def creation_images(self) -> list:
        return self.payload["photo_url_list"]
