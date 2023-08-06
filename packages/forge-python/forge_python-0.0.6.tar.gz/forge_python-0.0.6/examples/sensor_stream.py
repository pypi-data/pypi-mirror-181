import numpy as np
from forge_python import forge

sensor = forge.sensor()
sensor.authenticate("d1805592-64d8-4b70-8420-65276da5e37c")
sensor.send({'temperature': 95.5})


for value in np.linspace(95, 99.5, 10):
    sensor.send({'temperature': value})
