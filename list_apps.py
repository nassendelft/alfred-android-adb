import subprocess
import os
import alfred

adb_path = os.getenv('adb_path')


def list_apps(arg):
    apps = subprocess.check_output(
            "{0} shell 'pm list packages -f' | sed -e 's/.*=//' | sed 's/\r//g' | sort".format(adb_path),
            stderr=subprocess.STDOUT,
            shell=True)
    apps = apps.rstrip().split('\n')

    items = []
    for app in apps:
        if arg is '' or app.startswith(arg):
            items.append(alfred.Item({'arg': app}, app, ''))

    alfred.write(alfred.xml(items))

if __name__ == '__main__':
    list_apps(alfred.args()[0])
