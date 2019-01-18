import subprocess

def delete():
    result = subprocess.check_output("kubectl delete sparkapplications spark-pi", shell=True)
    return result