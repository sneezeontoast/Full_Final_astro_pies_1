import sys
import numpy as np
import pandas as pd
#import orbit
from orbit import ISS
import cv2 as cv

print(sys.version)
print(*sys.path, sep='\n')

print('Numpy: ',np.__version__)
print('Pandas: ',pd.__version__)
#print(*dir(pd),sep='\n')

#print(pd.__doc__)
print(pd.__file__)
print(pd.__spec__)
print(pd.__package__)
print(pd.__path__)

#print(orbit.__spec__)
print('cv: ', cv.__version__)


import argparse
import time

import numpy as np
from PIL import Image
from pycoral.adapters import classify
from pycoral.adapters import common
from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter


