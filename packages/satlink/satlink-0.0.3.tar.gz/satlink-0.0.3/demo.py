from src.satlink import Satellite


sat = Satellite()


@sat.get("/")
def index(uplink, downlink):
    return downlink.text("Hello, World!")


sat.transmit(3000)
