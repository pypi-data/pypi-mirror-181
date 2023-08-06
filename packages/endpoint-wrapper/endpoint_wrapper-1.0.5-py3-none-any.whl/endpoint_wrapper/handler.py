import base64
import io
import json
import time

import numpy as np
from PIL import Image

def frame_handler(payload):
    b64_img = payload['frame'].encode('ASCII')
    bin_img = base64.b64decode(b64_img)
    img = Image.open(io.BytesIO(bin_img))
    nd_arr = np.asarray(img)
    return nd_arr