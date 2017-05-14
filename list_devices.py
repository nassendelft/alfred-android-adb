import subprocess
import os
import alfred
import datetime

adb_path = os.getenv('adb_path')


def list_apps(args):
    apps = subprocess.check_output(
            adb_path + " devices -l | sed -n '1!p' | tr -s ' '",
            stderr=subprocess.STDOUT,
            shell=True)
    apps = apps.rstrip().split('\n')

    items = []
    for app in apps:
        arg = args[0] if args else ''
        if arg == '' or arg in app:
            values = app.split(' ')
            name = values[0]
            items.append(alfred.Item({'arg': name}, name, ''))

    alfred.write(alfred.xml(items))


if __name__ == '__main__':
    args = alfred.args()
    list_apps(args)
