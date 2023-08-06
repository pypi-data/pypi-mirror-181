from src.satlink import Satellite


api = Satellite()


@api.get("/[id]")
def index(uplink, downlink):
    return downlink.json(uplink.query)


@api.get("/")
def index(uplink, downlink):
    return downlink.text("Hello, World!")


api.transmit(3000)
