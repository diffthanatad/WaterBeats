import pytest
from base_station_app import app

@pytest.mark.asyncio()
@pytest.fixture(scope='package', autouse=True)
def event_loop():
    yield app.loop

@pytest.fixture()
def test_app(event_loop):
    """passing in event_loop helps avoid 'attached to a different loop' error"""
    app.finalize()
    app.conf.store = 'memory://'
    app.flow_control.resume()
    return app