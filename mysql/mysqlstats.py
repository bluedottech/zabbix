import subprocess
import re
from tempfile import NamedTemporaryFile

# zabbix_sender -c /etc/zabbix/zabbix_agentd.conf -i input-file

# get hostname from config file

with open("/etc/zabbix/zabbix_agentd.conf") as agentfile:
    lines = agentfile.readlines()

for line in lines:
    if not line.lstrip().startswith('#'):
        if "Hostname=" in line:
            print(line)
            hostname = line.split("=")[1]
            hostname = hostname.rstrip()

stat_data = [r"(?P<stat_name>\S+)", r"(?P<stat_value>\S+)"]
pattern = re.compile(r'\s+'.join(stat_data)+r'\s*\Z')

tmpfile = "/tmp/zabbix_sender_mysqlstats"
stats = subprocess.Popen(['/usr/bin/mysql', '--execute=show status'], stdout=subprocess.PIPE)
lines = stats.stdout.readlines()
with open(tmpfile, "w") as f:
    for line in lines:
        m = pattern.match(line)
        try:
            stat = m.groupdict()
            f.write("{0} {1} {2}\n".format(hostname, stat['stat_name'], stat['stat_value']))
        except:
            pass

