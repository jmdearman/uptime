import datetime
import os
import socket
import time

INTERVAL = 30
TIMEOUT = 5
HOST = ('8.8.8.8', 53)
LOGFILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'uptime_log.txt')


def log(message):
    with open(LOGFILE, 'a') as f:
        print('{} {}'.format(datetime.datetime.now().isoformat(), message), file=f)


def connected():
    try:
        socket.setdefaulttimeout(TIMEOUT)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(HOST)
        return True
    except Exception as ex:
        return False


def daemon():
    start_time = datetime.datetime.utcnow()
    log('DAEMON started with test interval={} and timeout={} against host={}'.format(INTERVAL, TIMEOUT, HOST))
    disconnected_start_time = start_time
    up = True
    while True:
        current_time = datetime.datetime.utcnow()
        if connected():
            if not up:
                delta = current_time - disconnected_start_time
                log('RECONNECTED after {:.0f} seconds'.format(delta.total_seconds()))
                up = True
        else:
            if up:
                log('DISCONNECTED')
                disconnected_start_time = current_time
                up = False
        delta = current_time - start_time
        time.sleep((INTERVAL - delta.total_seconds()) % INTERVAL)


if __name__ == "__main__":
    daemon()
