import paramiko
import threading

sshs = []
ips = ["10.0.1.24", "10.0.1.25"]
for ip in ips:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(
        paramiko.AutoAddPolicy())

    ssh.connect(ip,  username="pi",
                password="B!um3nBo+")
    sshs.append(ssh)


def exe(ssh):
    ssh_stdin, ssh_stouz, ssh_stderr = ssh.exec_command(
        'python json2blinkt-time.py')
    print("bambam lights on")
    ssh.close()


threads = set()
for ssh in sshs:
    threads.add(threading.Thread(target=exe, args=[ssh]))

for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
