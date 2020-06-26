import subprocess
import re
import shutil

import paramiko


STATE_MAPPING = {
    "BF": "Boot Fail",
    "CA": "Cancelled",
    "CD": "Completed",
    "CF": "Configuring",
    "CG": "Completing",
    "DL": "Deadline",
    "F": "Failed",
    "NF": "Node Fail",
    "OOM": "Out Of Memory",
    "PD": "Pending",
    "PR": "Preempted",
    "R": "Running",
    "RD": "Resv Del Hold",
    "RF": "Requeue Fed",
    "RH": "Requeue Hold",
    "RQ": "Requeued",
    "RS": "Resizing",
    "RV": "Revoked",
    "SI": "Signaling",
    "SE": "Special Exit",
    "SO": "Stage Out",
    "ST": "Stopped",
    "S": "Suspended",
    "TO": "Timeout",
}


class Cluster(object):
    def __init__(self, remote):
        super().__init__()

        if not remote:
            if shutil.which("sinfo") is None:
                raise SystemExit("Slurm binaries not found.")
        else:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.load_system_host_keys()
            self.ssh_client.connect(remote)


        self.remote = remote

        self.me = None

        # self.nodes = get_nodes()
        self.partitions = None

        self.config = self.get_config()

    def run_command(self, cmd: str):
        if self.remote:
            stdin, stdout, stderr = self.ssh_client.exec_command(cmd)
            o = stdout.readlines()
        else:
            process = subprocess.run(cmd.split(" "), capture_output=True)
            o = process.stdout.decode("utf-8").splitlines()

        return o

    def get_config(self):
        o = self.run_command("scontrol show config")

        pattern = "(\S+)\s*=(.*)"

        config = {}
        for line in o[1:]:
            try:
                match = re.search(pattern, line)
                config[match.group(1)] = match.group(2)
            except:
                continue

        return config

    def get_jobs(self):
        cmd = 'squeue --all --format="%.18i %.10P %.30j %.8u %.2t %.10M %.6D %.5y %.20R %.15b"'
        o = self.run_command(cmd)

        jobs = []
        fields = o[0].split()
        for line in o[1:]:
            job = {k: v for k, v in zip(fields, line.split())}
            jobs.append(Job(job))

        return jobs


class Partition(object):
    def __init__(self):
        super().__init__()


class Job(object):
    def __init__(self, string):
        super().__init__()

        self.job_id = string["JOBID"]
        self.nodes = string["NODES"]
        self.partition = string["PARTITION"]
        self.name = string["NAME"]
        self.user = string["USER"]
        self.state = STATE_MAPPING[string["ST"]]
        self.time = string["TIME"]

    def __repr__(self):
        return f"{self.job_id} - {self.user} - {self.name} - {self.time} - {self.state}"


class JobStep(object):
    def __init__(self):
        super().__init__()


class Node(object):
    def __init__(self):
        super().__init__()


if __name__ == "__main__":
    jobs = get_jobs()
    for j in jobs:
        print(j)
