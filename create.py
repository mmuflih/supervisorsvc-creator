import pathlib
import os.path
from os import path

service_name = input("Service Name: ").lower()
app_name = input("APP Name: ").lower()
restart_sh = "restart_" + service_name + ".sh"
start_sh = service_name + ".sh"
conf_d = service_name + ".conf"

app_path = pathlib.Path().absolute()
app_path = str(app_path) + "/" + app_name


def create_app_folder():
    if not(path.exists(app_path)):
        pathlib.Path(app_path).mkdir(parents=True)


def create_restart_script():
    f_restart_sh = open(app_path + "/" + restart_sh, "a")
    restart_sources = [
        '#!/bin/sh',
        '',
        'supervisorctl stop '+service_name+':'+service_name+'_00',
        'supervisorctl start '+service_name+':'+service_name+'_00',
    ]
    restart_src = "\n".join(restart_sources)
    f_restart_sh.write(restart_src)
    f_restart_sh.close()


def create_star_script():
    f_start_sh = open(app_path + "/" + start_sh, 'a')
    start_sources = [
        'cd ' + app_path + '/bin',
        '/usr/bin/sh appservice.sh start',
    ]
    start_src = "\n".join(start_sources)
    f_start_sh.write(start_src)
    f_start_sh.close()


def create_supervisord_conf():
    f_conf_d = open("/etc/supervisor/conf.d/" + conf_d, 'a')
    conf_sources = [
        '[program:'+service_name+']',
        'process_name=%(program_name)s_%(process_num)02d',
        'command=/usr/bin/sh ' + app_path + '/' + start_sh,
        'autostart=true',
        'autorestart=true',
        'user=root',
        'numprocs=1',
        'redirect_stderr=true',
        'stdout_logfile=' + app_path + '/' + start_sh + '.log',
    ]
    conf_src = "\n".join(conf_sources)
    f_conf_d.write(conf_src)
    f_conf_d.close()


create_app_folder()
create_restart_script()
create_star_script()
create_supervisord_conf()
