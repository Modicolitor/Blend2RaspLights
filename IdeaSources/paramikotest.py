import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(
    paramiko.AutoAddPolicy())

# ssh.load_host_keys()

# print(key)
ssh.connect("10.0.1.20",  username="pi",
            password="B!um3nBo+")  # password error
# ssh.start_client()

ssh_stdin, ssh_stouz, ssh_stderr = ssh.exec_command('cd /BLEND2BLINK/')
# "ls -l")  # cd /BLEND2BLINK/")
ssh_stdin, ssh_stouz, ssh_stderr = ssh.exec_command(
    'python json2blinkt-time.py')

ssh.close()
