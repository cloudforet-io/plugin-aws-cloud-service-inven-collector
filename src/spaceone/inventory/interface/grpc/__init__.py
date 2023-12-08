from spaceone.core.pygrpc.server import GRPCServer
from .collector import Collector

_all_ = ["app"]

app = GRPCServer()
app.add_service(Collector)
