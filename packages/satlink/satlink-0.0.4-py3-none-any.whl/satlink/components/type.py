from typing import Callable, Tuple
from .downlink import Downlink
from .uplink import Method, Uplink


Handler = Callable[[Uplink, Downlink], Downlink]
Endpoint = Tuple[Method, str, Handler]
