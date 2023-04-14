import yaml
from Prometheus import Prometheus
from Run_script import Run_script
from Setting import ISROOT,INTERVAL,GAP
"""macro definition"""

"""configure and run prometheus server"""
server = Prometheus(value=404, hport=5001)
server.run_server()
Run_script(ISROOT=ISROOT, INTERVAL=INTERVAL, GAP=GAP, server=server).run()
