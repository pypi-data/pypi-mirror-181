import paramiko
from io import StringIO

def ssh_command(host,username,port,privatekey,command):

    ssh_privatekey = f"""\
-----BEGIN OPENSSH PRIVATE KEY-----
{privatekey}
-----END OPENSSH PRIVATE KEY-----"""

    pkey = paramiko.RSAKey.from_private_key(StringIO(ssh_privatekey))
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, pkey=pkey)
    stdin, stdout, stderr = ssh.exec_command(command)
    lines= stdout.readlines()
    print(lines)
    ssh.close()