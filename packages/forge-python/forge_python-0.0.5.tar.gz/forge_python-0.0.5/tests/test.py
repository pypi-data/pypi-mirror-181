from forge_python import forge


sensor = forge.sensor()
sensor.authenticate("lozl101000000")
sensor.send({'temperature': 95})
