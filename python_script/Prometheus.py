from prometheus_client import Gauge, start_http_server

class Prometheus:
    def __init__(self,value,hport):
        self.value = value
        self.hport = hport

        # initial dashboard
        self.cpu_usage = Gauge('cpu_usage', 'CPU USAGE', ['IP', 'card', 'system_name', 'owner_name'])
        self.mem_usage = Gauge('mem_usage', 'MEM USAGE', ['IP', 'card', 'system_name', 'owner_name'])
        self.core_file_times = Gauge('corefile', 'corefile times', ['IP', 'card', 'system_name', 'owner_name'])
        self.new_core_file_flag = Gauge('new_core_flag','new core flag', ['IP', 'card', 'system_name', 'owner_name'])
        self.crash_process = Gauge('crash_process', 'CRASH process', ['IP', 'card', 'system_name', 'owner_name'])
        self.alarm_active = Gauge('alarm_active', 'alarm active', ['IP', 'mode', 'system_name', 'owner_name'])
        self.ont_active = Gauge('ont_active', 'alarm event ont', ['IP', 'mode', 'system_name', 'owner_name'])
        self.port_rate = Gauge('port_rate', 'all port rates', ['IP', 'port_name', 'rate_type', 'system_name', 'owner_name'])
        self.disk_usage = Gauge('disk_usage', 'DISK USAGE', ['IP', 'mode', 'system_name', 'owner_name'])
        self.sensors_temp = Gauge('sensors_temperature', 'SENSORS TEMPERATURE', ['IP', 'card', 'sensor', 'system_name', 'owner_name'])
        self.reboot_times = Gauge('reboot_times', 'REBOOT TIMES', ['IP', 'card', 'system_name', 'owner_name'])
        self.main_process_mem = Gauge('main_process_mem','MAIN PROCESS MEM',['IP','mode', 'system_name', 'owner_name'])
        # self.mem_top = Gauge('mem_top','MEM TOP',['IP','rank','process_name','system_name'])

        self.vm_cpu_usage = Gauge('vm_cpu_usage', 'VM CPU USAGE', ['IP', 'card', 'system_name', 'owner_name'])
        self.vm_mem_usage = Gauge('vm_mem_usage', 'VM MEM USAGE', ['IP', 'card', 'system_name', 'owner_name'])
        self.vm_disk_usage = Gauge('vm_disk_usage', 'VM DISK USAGE', ['IP', 'card', 'system_name', 'owner_name'])


    def run_server(self):
        # Gauge monitor items，http_code，only inis once or it'll report“ValueError：Duplicated timeseries in
        # CollectorRegistry”
        http_code = Gauge('http_code', 'HTTP CODE')
        http_code.set(self.value)

        # start http server
        start_http_server(self.hport)