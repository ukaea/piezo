import subprocess


def go_get_logs():
    result = subprocess.check_output("kubectl logs spark-pi-driver", shell=True)
    print(result)
    return(result)