from enum import Enum

class Level(Enum):
    HIGH = 3
    MEDIUM = 2
    LOW = 1
    NONE = 0
    
class Category(Enum):
    Personal = 1
    Work = 2
    Health = 3
    Others = 4