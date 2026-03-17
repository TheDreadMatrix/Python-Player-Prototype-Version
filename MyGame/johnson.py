import json
from pathlib import Path



class Johnson:
    def __init__(self, json_path):
        self.path = Path(json_path)
        if not self.path.exists():
            raise FileNotFoundError(f"File not found: {str(self.path)}")

    def readData(self):
        with open(self.path, "r") as f:
            data = json.load(f)
        return data
    
    def saveData(self, data):
        with open(self.path, "w") as f:
            json.dump(data)




def readShader(path: str) -> str:
    return (Path("shaders") / path).read_text()





def getDD(path: str) -> Path:
    file = Path("data") / path
    if not file.exists():
        raise FileNotFoundError(f"Data file not found: {file}")
    return file


def getAD(path: str) -> Path:
    file = Path("assets") / path
    if not file.exists():
        raise FileNotFoundError(f"Asset file not found: {file}")
    return file


def getSD(path: str) -> Path:
    file = Path("soundtracks") / path
    if not file.exists():
        raise FileNotFoundError(f"Soundtrack file not found: {file}")
    return file