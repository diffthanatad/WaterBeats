import faust

app = faust.App(
    'hello-world', # application id, needs to be unique per faust application per cluster
    broker='kafka://localhost:9092',
    value_serializer='raw',
)

greetings_topic = app.topic('greetings')

@app.agent(greetings_topic)
async def greet(greetings):
    async for greeting in greetings:
        print(greeting)

# faust -A hello_world send @greet "Hello Faust" 
# '@' prefix pushes messages to an agent
# faust -A hello_world send greetings "Hello Kafka topic"
# no '@' prefix makes it the name of a topic