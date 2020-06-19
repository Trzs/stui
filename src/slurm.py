import subprocess
import re


class Cluster(object):
    def __init__(self):
        super().__init__()

        self.me = None

        # self.nodes = get_nodes()
        self.partitions = None

        self.config = self.get_config()

    def get_config(self):
        cmd = "ssh yarin scontrol show config"
        process = subprocess.run(cmd.split(" "), capture_output=True)
        o = process.stdout.decode("utf-8").splitlines()

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
        command = "ssh yarin squeue"
        squeue_process = subprocess.run(command.split(" "), capture_output=True)

        o = squeue_process.stdout.decode("utf-8").splitlines()

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
        self.state = string["ST"]
        # self.time

    def __repr__(self):
        return f"{self.job_id} User: {self.user} State: {self.state}"


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
