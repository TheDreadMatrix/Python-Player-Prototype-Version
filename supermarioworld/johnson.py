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
            json.dump(data, f, indent=4)




