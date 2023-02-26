import base_station as bs

async def calculateActuatorInstruction(event):
    if type(event) == bs.HumidityReading:
        print('HumidityReading')
    elif type(event) == bs.TemperatureReading:
        print('TemperatureReading')
    elif type(event) == bs.SoilMoistureReading:
        if int(event.reading_value) < 10:
            message = bs.ActuatorInstruction('someActuatorID', 'ON')
            await bs.actuator_instructions.send(value=message)
        elif int(event.reading_value) > 20:
            message = bs.ActuatorInstruction('someActuatorID', 'OFF')
            await bs.actuator_instructions.send(value=message)