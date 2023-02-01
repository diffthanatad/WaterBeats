import faust

app = faust.App(
    'sensor_streaming', # application id, needs to be unique per faust application per cluster
    broker='kafka://localhost:9092',
    value_serializer='raw',
)

humidity_readings = app.topic('humidity')
temperature_readings = app.topic('temperature')
soil_moisture_readings = app.topic('soil-moisture')

@app.agent(humidity_readings)
async def greet(greetings):
    async for greeting in greetings:
        print(greeting)

# faust -A hello_world send @greet "Hello Faust" 
# '@' prefix pushes messages to an agent
# faust -A hello_world send greetings "Hello Kafka topic"
# no '@' prefix makes it the name of a topic