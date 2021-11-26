from chaos.workloads.writes import writes
from chaos.workloads.reads_writes import reads_writes

import logging

logger = logging.getLogger("chaos")

def kafka_clients_workload(nodes_path):
    writing_java = writes.Control()
    writing_java.launch = "/mnt/vectorized/control/writes.java.start.sh"
    writing_java.alive = "/mnt/vectorized/control/writes.java.alive.sh"
    writing_java.kill = "/mnt/vectorized/control/writes.java.stop.sh"
    writing_java.name = "writes / java"
    return writes.Workload(writing_java, nodes_path)

def concurrency_workload(nodes_path):
    writing_java = writes.Control()
    writing_java.launch = "/mnt/vectorized/control/concurrency.java.start.sh"
    writing_java.alive = "/mnt/vectorized/control/concurrency.java.alive.sh"
    writing_java.kill = "/mnt/vectorized/control/concurrency.java.stop.sh"
    writing_java.name = "writes / concurrency"
    return writes.Workload(writing_java, nodes_path)

def confluent_kafka_workload(nodes_path):
    writing_python = writes.Control()
    writing_python.launch = "/mnt/vectorized/control/writes.python.start.sh"
    writing_python.alive = "/mnt/vectorized/control/writes.python.alive.sh"
    writing_python.kill = "/mnt/vectorized/control/writes.python.stop.sh"
    writing_python.name = "writes / python"
    return writes.Workload(writing_python, nodes_path)

def list_offsets_workload(nodes_path):
    writing_java = writes.Control()
    writing_java.launch = "/mnt/vectorized/control/list-offsets.java.start.sh"
    writing_java.alive = "/mnt/vectorized/control/list-offsets.java.alive.sh"
    writing_java.kill = "/mnt/vectorized/control/list-offsets.java.stop.sh"
    writing_java.name = "list-offsets / java"
    return writes.Workload(writing_java, nodes_path)

def reads_writes_workload(nodes_path):
    control = reads_writes.Control()
    control.launch = "/mnt/vectorized/control/reads-writes.java.start.sh"
    control.alive = "/mnt/vectorized/control/reads-writes.java.alive.sh"
    control.kill = "/mnt/vectorized/control/reads-writes.java.stop.sh"
    control.name = "reads-writes / java"
    return reads_writes.Workload(control, nodes_path)

WORKLOADS = {
    "reads-writes / java": reads_writes_workload,
    "list-offsets / java": list_offsets_workload,
    "writes / java": kafka_clients_workload,
    "writes / python": confluent_kafka_workload,
    "writes / concurrency": concurrency_workload
}

def wait_all_workloads_killed(nodes_path):
    for key in WORKLOADS:
        logger.debug(f"stopping workload {key} everywhere (if running)")
        workload_cluster = WORKLOADS[key](nodes_path)
        workload_cluster.kill_everywhere()
        workload_cluster.wait_killed(timeout_s = 10)