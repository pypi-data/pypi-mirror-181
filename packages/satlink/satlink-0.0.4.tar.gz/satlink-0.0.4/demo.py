from src.satlink import Satellite, Uplink, Downlink


sat = Satellite()


@sat.get("/")
def index(uplink: Uplink, downlink: Downlink):
    return downlink.text("Hello, World!")


sat.transmit(3000)
