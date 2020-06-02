import paramiko

ssh = paramiko.SSHClient()
ssh.connect("10.0.1.20:24",  username="pi",
            password="B!um3nBo+")  # password error


ssh_stdin, ssh_stouz, ssh_stderr = ssh.exec_command("cd /BLEND2BLINK/")
ssh_stdin, ssh_stouz, ssh_stderr = ssh.exec_command(
    "python json2blinkt-time.py")

ssh.close()
