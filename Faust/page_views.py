import faust
import ast

app = faust.App(
    'page_views',
    broker='kafka://localhost:9092',
    value_serializer='json',
    topic_partitions=4,
)

class PageView(faust.Record):
    id: str
    user: str

page_view_topic = app.topic('page_views', value_type=PageView)
page_views = app.Table('page_views', default=int)

@app.agent(page_view_topic)
async def count_page_views(views):
    async for view in views.group_by(PageView.id):
        page_views[view.id] += 1

# faust -A page_views send page_views '{"id": "foo", "user": "bar"}'
# original json format string
# faust -A page_views send page_views "{"""id""": """foo""", """user""": """bar"""}"
# triple quote escapes for windows cmdln 
