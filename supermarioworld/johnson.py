import json
from pathlib import Path



class Johnson:
    def __init__(self, json_path):
        self.path = Path(json_path)
        if not self.path.exists():
            raise FileNotFoundError(f"File not found: {str(self.path)}")

    def readData(self) -> dict[str]:
        return readData(self.path)
    
    def saveData(self, data: dict[str]):
        saveData(self.path, data)



def readData(path: str) -> dict:
    try: 
        with open(path, "r", encoding="utf-8") as f: 
            data = json.load(f)
    except json.JSONDecodeError:
        data = {}
    return data


def saveData(path: str, data: dict) -> None: 
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    except TypeError:
        return