import sys
import ping3
import random
import threading


# TODO: make this smarter (all ips
def generate_ip():
    ip_pattern = r'^(?:\d{1,3}\.){3}(?!10\.|172\.(1[6-9]|2\d|3[01])\.|192\.168\.)(?:\d{1,3}\.){1}\d{1,3}$'
    return ".".join([str(random.randint(1,254)) for _ in range(4)])


def ping_one(hostname):
    print(f'pinging {hostname}')
    response = ping3.ping(hostname)
    if response is not False and response is not None:
        print(f"{hostname} is alive (response time: {response} ms)")


def ping_n_rand(n):
    threads = []
    hosts = [generate_ip() for _ in range(n)]
    for hostname in hosts:
        t = threading.Thread(target=ping_one, args=(hostname,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
    return n


if len(sys.argv) != 3:
    print("usage: python3 myscan.py NUMBER_OF_THREADS TOTAL_IPS")
    print("e.g.: python3 myscan.py 10 1000")
    exit(1)

pinged_ips = 0
while pinged_ips < int(sys.argv[2]):
    pinged_ips += ping_n_rand(int(sys.argv[1]))

