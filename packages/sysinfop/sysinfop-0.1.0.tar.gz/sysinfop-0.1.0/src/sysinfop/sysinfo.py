import platform
import socket
import re
import uuid
import psutil

icon_map = {
    "Windows": "windows-logo-here",
    "Linux": "tux-logo-here",
    "Darwin": "macos-logo-here",
    "Java": "java-logo-here"
}

def getASCII(platf):
    icon = icon_map[platf]
    return icon

def getSystemInfo():
    try:
        info={}
        info['platform']=platform.system()
        info['platform-release']=platform.release()
        info['platform-version']=platform.version()
        info['architecture']=platform.machine()
        info['hostname']=socket.gethostname()
        info['ip-address']=socket.gethostbyname(socket.gethostname())
        info['mac-address']=':'.join(re.findall('..', '%012x' % uuid.getnode()))
        info['processor']=platform.processor()
        info['ram']=str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"
        info['logo']=getASCII(info['platform'])
        return info
    except Exception as e:
        print(f"[red]ERROR: {e}[/red]")
