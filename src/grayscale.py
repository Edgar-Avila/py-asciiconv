from enum import Enum
import numpy as np
from typing import List

class Grayscale(Enum):
    BINARY = 'binary'
    NORMAL = 'normal'
    EXTENDED = 'extended'

    def __str__(self) -> str:
        return self.value
    
    def ascii(self) -> str:
        if self == Grayscale.BINARY:
            return ' @'
        if self == Grayscale.NORMAL:
            return ' .:-=+*#%@'
        if self == Grayscale.EXTENDED:
            return ' .`^",:;Il!i><~+_-?][1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B$@'
        raise f'{self} is not a valid grayscale'

    def asciimap(self) -> List[str]:
        a = self.ascii()
        return [a[int(np.interp(i, [0, 255], [0, len(a)-1]))] for i in range(256)]


