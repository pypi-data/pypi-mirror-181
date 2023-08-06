# forge-python

[forge-python](https://www.theforge.bio/) enables you to create, change, and develop industrial process simulations. It is an open source tool that codifies APIs into declarative configuration files that can be shared amongst team members, treated as code, edited, reviewed, and versioned.

# how to use

## installment requirements

```{.python }
pip install forge-python colorama
```

## example: sending sensor data

```{.python }
from forge_python import forge
sensor = forge.sensor()
sensor.authenticate('device6ef0e2a6f88f481ea81e388d8be91a1c')
sensor.send({'temperature': 95.5})
```
