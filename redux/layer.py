
class LayerManager:
    def __init__(self):
        self.layer_1 = {"layer":"1", "linetype":"CENTER"}
        self.layer_2 = {"layer":"2", "linetype":"HIDDEN"}
        self.layer_3 = {"layer":"3", "linetype":"Continuous"}
        self.layer_4 = {"layer":"4", "linetype":"Continuous"}
        self.layer_6 = {"layer":"6", "linetype":"PHANTOM"}


if __name__ == "__main__":
    layer = LayerManager()
    print(layer.layer_1)