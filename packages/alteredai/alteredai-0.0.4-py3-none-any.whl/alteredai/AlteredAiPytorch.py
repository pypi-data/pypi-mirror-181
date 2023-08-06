from .AlteredAiDataLoader import AlteredAiDataLoader


class AlteredAiPytorch(AlteredAiDataLoader):
    def __init__(self):
        print("AlteredAiPytorch Loaded Successfully")

    def funPytorch(self):
        print("This is function from Pytorch Class")
