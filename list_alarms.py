import subprocess
import os
import alfred
import datetime

adb_path = os.getenv('adb_path')


def list_apps(arg):
    pattern = '{ print $1 " " $7 " " substr($8, 1, length($8)-2) }'
    apps = subprocess.check_output(
            "{0} shell dumpsys alarm | awk '/^ +(RTC_WAKEUP|ELAPSED_WAKEUP|RTC|ELAPSED)/ {1}'".format(adb_path, pattern),
            stderr=subprocess.STDOUT,
            shell=True)
    apps = apps.rstrip().split('\n')

    items = []
    for app in apps:
        values = app.split(' ')
        if arg is '' or values[2].startswith(arg):
            type = values[0]
            time = timestamp_to_time(type, float(values[1]))
            item = "{0} {1} {2}".format(type, time, values[2])
            items.append(alfred.Item({'arg': time}, item, ''))

    alfred.write(alfred.xml(items))


def timestamp_to_time(type, timestamp):
    format = '%Y-%m-%d %H:%M:%S'
    if type == 'RTC_WAKEUP' or type == 'RTC':
        return datetime.datetime.utcfromtimestamp(timestamp / 1000).strftime(format)
    elif type == 'ELAPSED_WAKEUP' or type == 'ELAPSED':
        c = datetime.timedelta(milliseconds=timestamp)
        return str(datetime.timedelta(seconds=c.seconds))
    return 'test'


if __name__ == '__main__':
    list_apps(alfred.args()[0])
