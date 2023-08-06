from src.satlink import Satellite


api = Satellite()


@api.get("/")
def index(uplink, downlink):
    return downlink.text("Hello, World!")


api.transmit(3000)
