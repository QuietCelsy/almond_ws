import os
import socket
import time

import psutil
HOST = "0.0.0.0"
PORT = 3000


# def wait_and_send_log (msg):
#     log_name = conn.recv(1024).decode()
#     while True:
#         if log_name == f'{msg}':
#             break
#         else:
#             continue
#     file = open(rf'~/.ros/log/latest/{msg}')
#     log = file.read()
#     conn.send(log.encode())
#     file.close()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen(5)
    conn, addr = server.accept()
    data_list = {"CPU": " ", "Disk": " ", "Process": ""}
    process_list = ''
    with conn:
        print(f"Connected by {addr}")
        while True:
            cpu_usage = 'CPU]' + str(psutil.cpu_percent(interval=0.5))
            disk_usage = 'DISK]' + str(psutil.disk_usage('/home'))
            # temperature = psutil.sensors_temperatures(fahrenheit=True)
            # print(temperature)
            # conn.send(f"Temperature - {temperature}".encode())
            for proc in psutil.process_iter(['pid', 'name', 'username']):
                try:
                    # print(proc.info['name'])
                    Process = proc.info['name']
                    path = proc.exe()
                    if Process[0] == 'R':
                        process_list += f'#' + Process + '  ' + path
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            process_send = 'PROC]' + process_list
            data = cpu_usage + '/' + disk_usage + '/' + process_send
            conn.send(data.encode())
            # wait_and_send_log('master.log')
            process_send = ''
            process_list = ''
            data = ''
            while True:
                cont = conn.recv(1024).decode()
                if cont == 'Continue':
                    break
                else:
                    continue


