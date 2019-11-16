import subprocess
import re

stat_data = [r"(?P<stat_name>\S+)", r"(?P<stat_value>\S+)"]
pattern = re.compile(r'\s+'.join(stat_data)+r'\s*\Z')

stats = subprocess.Popen(['/usr/bin/mysql', '--execute=show status'], stdout=subprocess.PIPE)
lines = stats.stdout.readlines()
print('{ "data": [')
for line in lines:
    m = pattern.match(line)
    try:
        stat = m.groupdict()
        try:
            a = int(stat['stat_value'])
            b = float(stat['stat_value'])
            if a == b:
                print(' { "{{#MYSQLSTAT}}": "{0}" },'.format(b))
            else:
                print(' { "{{#MYSQLSTAT}}": "{0}" },'.format(a))
        except:
            pass
    except:
        pass
print(' ] }')
