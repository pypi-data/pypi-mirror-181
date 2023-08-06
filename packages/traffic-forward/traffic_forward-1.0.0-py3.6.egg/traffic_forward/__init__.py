import socket
import select
import logging
import threading
import argparse
import time

total_connect = 0
PKT_BUFF_SIZE = 10240
udp_source =0 
udp_source_list = []


class Trans():
    def __init__(self,debug_level):
        self.debug_level = debug_level
        self.log = self.logger(self.debug_level)
        

    def logger(self, debug_level):
        logger = logging.getLogger()
        fh = logging.FileHandler('test.log')  
        ch = logging.StreamHandler() 
        fm = logging.Formatter('%(asctime)s %(message)s')
        fh.setFormatter(fm)
        ch.setFormatter(fm)
        logger.addHandler(fh)
        logger.addHandler(ch)
        logger.setLevel(debug_level)
        return logger


    def data_tran(self, socket_list):
        global total_connect
        #print(socket_list)
        t=[]
        t.append(socket_list[0]) # socket s   A-B
        t.append(socket_list[1]) # socket s1  B-C
        try:
            t[0].getpeername()
            t[1].getpeername()
        except Exception as e:
            self.log.error("[-] Get Remote Host Failed")
        #inputs = [t[0], t[1]]
        OK = 1
        while(OK):
            '''
            readable, writable, exceptional= select.select(t, output, t)
            if len(exceptional)!=0:
                self.log.error("socket error")
                break
            if len(readable)==0:
                break
            '''
            #for i in range(2):#0
            try:
                recv_data = t[0].recv(PKT_BUFF_SIZE)
                self.log.info("[+] recv data %s:%d <--- %s:%d"%(t[0].getpeername()[0],t[0].getpeername()[1],t[1].getpeername()[0],t[1].getpeername()[1]))
            except Exception as e:
                print(e)
                self.log.error('[-]: Connection closed')
                break

            if not recv_data:
                self.log.error('[-]: Connection closed')
                break
            try:
                t[1].sendall(recv_data)
                self.log.info("[+] send data %s:%d ---> %s:%d"%(t[1].getpeername()[0],t[1].getpeername()[1],t[0].getpeername()[0],t[0].getpeername()[1]))
            except Exception as e:
                print(e)
                self.log.error('[-]: Connection closed')
                break
            #else:
                #    OK = 0
                #    self.log.info("[+]  Connection <Total %d> Cutdown, Total : %d Bytes"%(total_connect,total_byte))
                #    break
        t[0].close()
        t[1].close()
        return -1 
         
    def tcp_mapping_request(self, socket_list):
        threading.Thread(target=self.data_tran, args=(socket_list, )).start()
        threading.Thread(target=self.data_tran, args=(socket_list[::-1], )).start()

    def tran(self , ip1 , port1, ip2, port2):
        s = socket.socket()
        flag = 0
        if(s!=-1):
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
            ip_port = (ip1,port1)
            if(s.bind(ip_port)==None):
                if(s.listen(1024)==None):
                    flag = 1
                    self.log.info("[+] listen on %d"%(port1))
                else:
                    self.log.error("[-] listen error")
            else:
                self.log.error('[-] bind error')
        else:
            self.log.error("[-] Create socket error")
        
        if( flag==0 ):
            s.close()
            return
        socket_list=[]
        ac = -1
        while(1):
            try:
                ip_con = socket.gethostbyname(ip2)
            except Exception as e:
                self.log.error(e)
                break
            self.log.info("[+] Waiting Connect On Port %d"%(port1))
            try:
                clientsock,clientaddr=s.accept()
            except Exception as e:
                self.log.error("[-] listen error")
                break
            client = clientsock.getpeername()
            self.log.info("[+] connection from %s, Now connect to %s"%(client[0], ip2))
            s1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            ip_port2 = (ip2, port2)
            s1.connect(ip_port2)
            socket_list = [clientsock,s1]
            self.log.info("[+] Connect %s:%d Success, Start Transfer...."%(ip2,port2))
            #if(self.run(socket_list)==-1 or self.run(socket_list.reverse())==-1):
            #    self.log.error("[-] Connect %s Failed...."%(ip2))
            #    clientsock.close()
            #    s1.close()
            #    break
            #threading.Thread(target=self.data_tran, args=(socket_list).start()
            #threading.Thread(target=self.data_tran, args=(socket_list.reverse()).start()
            #print(socket_list[::-1])
            try:
                self.tcp_mapping_request(socket_list)
            except Exception as e:
                break
                             
        clientsock.close()
        s1.close()
        return 
    
    
    def listen(self, port1, port2):
        def compare(num):
            if num ==0:
                return 1
            else:
                return 0
        listen_socket = []
        port_list = []
        port_list.append(port1)
        port_list.append(port2)
        for i in range(2):
            OK = 0
            s1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
            listen_socket.append(s1)
            if (s1 != -1):
                self.log.info("[+] create socket %d"%(i))
                flag = 1
                ip_port1 = ('0.0.0.0',port_list[i])
                if(s1.bind(ip_port1)==None):
                    self.log.info("[+] bind on port %d success"%(port_list[i]))
                    if(s1.listen() == None):
                        self.log.info("[+] listen on port %d success"%(port_list[i]))
                        OK =1 
                    else:
                        self.log.error("[-] listen %d error"%(port_list[i]))
                else:
                    self.log.error("bind %d error"%(port_list[i]))
            else:
                self.log.error("create socket 1 error")
        if(OK!=1):
            listen_socket[0].close()
            listen_socket[1].close()
            return -1
        i=0
        t=[]
        while(1):
            self.log.info("[+] waiting connect on port %u",port_list[i])
            t1,clientaddr = listen_socket[i].accept()
            t.append(t1)
            if (t1 != None):
                self.log.info("[+] connect from %s"%(clientaddr[0]))
                if(i==1):
                    self.tcp_mapping_request(t)
                    t=[]
                i = compare(i)
            else:
                self.log.error("[-] Accept Failed on %d"%(port_list[i]))
                i = 0
        return 


    def slave(self, ip1, port1, ip2 ,port2):
        while(1):
            try:
                socket.gethostbyname(ip1)
                socket.gethostbyname(ip2)
            except:
                self.log.error("Reslove Host Failed")
            
            socket_list=[]
            s1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            
            if (s1 != None and s2 != None):
                    self.log.info("[+] connect %s please wait",ip1)
                    try:
                        s1.connect((ip1,port1))
                        self.log.info("[+] connect %s success"%(ip1))
                        socket_list.append(s1)
                        try:
                            self.log.info("[+] connect %s please wait",ip2)
                            s2.connect((ip2,port2))
                            self.log.info("[+] connect %s success"%(ip2))
                            socket_list.append(s2)
                            self.tcp_mapping_request(socket_list)
                        except:
                            self.log.error("[-] connect %s faile"%(ip2))
                    except:
                        self.log.error("[-] connect %s faile"%(ip1))
                        s1.close()
                        s2.close()
            else:
                self.log.error("create socket error")
            time.sleep(10)
        return

    def Utran(self, ip1 ,port1, ip2, port2):
        global udp_source
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        flag = 0
        if(s!=-1):
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
            ip_port = (ip1,port1)
            if(s.bind(ip_port)==None):
                flag = 1
                self.log.info("[+] bind on %d"%(port1))
            else:
                self.log.error('[-] bind error')
        else:
            self.log.error("[-] Create socket error")
        
        if( flag==0 ):
            s.close()
            return
        socket_list=[]
        ac = -1
        while(1):
            try:
                ip_con = socket.gethostbyname(ip2)
            except Exception as e:
                self.log.error(e)
                break
            self.log.info("[+] Waiting Connect On Port %d"%(port1))
            try:
                clinetdata,clientaddr=s.recvfrom(PKT_BUFF_SIZE)
                udp_source = clientaddr
                print(udp_source)
            except Exception as e:
                self.log.error("[-] listen error")
                break
            self.log.info("[+] connection from %s, Now connect to %s"%(clientaddr[0], ip2))
            s1 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            ip_port2 = (ip2, port2)
            s1.sendto(clinetdata, ip_port2)
            socket_list = [s,s1]
            self.log.info("[+] Connect %s:%d Success, Start Transfer...."%(ip2,port2))
            #if(self.run(socket_list)==-1 or self.run(socket_list.reverse())==-1):
            #    self.log.error("[-] Connect %s Failed...."%(ip2))
            #    clientsock.close()
            #    s1.close()
            #    break
            #threading.Thread(target=self.data_tran, args=(socket_list).start()
            #threading.Thread(target=self.data_tran, args=(socket_list.reverse()).start()
            #print(socket_list[::-1])
            try:
                self.udp_mapping_request(socket_list, ip2 ,port2)
            except Exception as e:
                print(e)
                break
                             
        s.close()
        s1.close()
        return 
    
    def U_data_tran(self, socket_list, ip, port):
        t = []
        t.append(socket_list[0]) # socket s   A-B
        t.append(socket_list[1]) # socket s1  B-C
        OK =1
        while(OK):
            try:
                recv_data, recvaddr = t[0].recvfrom(PKT_BUFF_SIZE)
                print(recv_data)
                self.log.info("[+] recv data from %s:%d"%(recvaddr[0],recvaddr[1]))
            except Exception as e:
                print(e)
                self.log.error('[-]: Connection closed')
                break
            if not recv_data:
                self.log.error('[-]: Connection closed')
                break
            try:
                ip_port = (ip,port)
                t[1].sendto(recv_data,ip_port)
                self.log.info("[+] send data to %s:%d"%(ip, port))
                
            except Exception as e:
                print(e)
                self.log.error('[-]: Connection closed')
                break
        
        t[0].close()
        t[1].close()
        return -1
    
    
    def Ulisten(self, port1, port2):
        global udp_source_list
        def compare(num):
            if num ==0:
                return 1
            else:
                return 0
        listen_socket = []
        port_list = []
        port_list.append(port1)
        port_list.append(port2)
        for i in range(2):
            OK = 0
            s1 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            s1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
            listen_socket.append(s1)
            if (s1 != -1):
                self.log.info("[+] create socket %d"%(i))
                flag = 1
                ip_port1 = ('0.0.0.0',port_list[i])
                if(s1.bind(ip_port1)==None):
                    OK=1
                    self.log.info("[+] bind on %d"%(port_list[i]))
                else:
                    self.log.error("[-] bind %d error"%(port_list[i]))
            else:
                self.log.error("[-] create socket error")
        if(OK!=1):
            listen_socket[0].close()
            listen_socket[1].close()
            return -1
        i = 0
        t = []
        while(1):
            try:
                self.log.info("[+] waiting connect on port %u",port_list[i])
                recv_data, recvaddr = listen_socket[i].recvfrom(PKT_BUFF_SIZE)
                udp_source_list.append(recvaddr)
                print(recvaddr)
                print(recv_data)
                if  recv_data!=None:
                    self.log.info("[+] connect from %s"%(recvaddr[0]))
                    if(i == 1):
                        print("doudou")
                        self.udp_mapping_request_for_salve(listen_socket, udp_source_list)
                    i = compare(i)
                else:
                    self.log.error("[-] recvdata fail")
            except Exception as e:
                print(e)
        
        return
    
    def udp_mapping_request(self, socket_list, ip ,port):
        threading.Thread(target=self.U_data_tran, args=(socket_list, ip, port, )).start()
        threading.Thread(target=self.U_data_tran, args=(socket_list[::-1], udp_source[0], udp_source[1], )).start()
        return
        
    def udp_mapping_request_for_salve(self, socket_list, udp_list):
        threading.Thread(target=self.U_data_tran, args=(socket_list, udp_list[0][0], udp_list[0][1], )).start()
        threading.Thread(target=self.U_data_tran, args=(socket_list[::-1], udp_list[1][0], udp_list[1][1], )).start()
        return

'''
    def Usalve(self, ip1, port1, ip2, port2):
        while(1):
            socket_list = []
            ip_port_list = []
            s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            if ( s1!=None or s2 !=None):
                self.log.info("[+] connect %s please wait",ip1)
                try:
                    s1.sendto(b"ok",(ip1,port1))
                    self.log.info("[+] connect %s success"%(ip1))
                    ip_port_list.append((ip1, port1))
                    socket_list.append(s1)
                    try:
                        socket_list.append(s1)
                        self.log.info("[+] connect %s please wait",ip2)
                        s2.sendto(b"ok", (ip2, port2))
                        self.log.info("[+] connect %s success"%(ip2))
                        socket_list.append(s2)
                        ip_port_list.append((ip2, port2))
                        print("doudou")
                        print(ip_port_list)
                        self.udp_mapping_request_for_salve(socket_list, ip_port_list)
                    except Exception as e:
                        print(e)
                        self.log.error("[-] connect %s faile"%(ip2))
                        s1.close()
                        s2.close()
                except Exception as e:
                    print(e)
                    self.log.error("[-] connect %s faile"%(ip1))
                    s1.close()
                    s2.close()
            else:
                self.log.error("create socket error")
            time.sleep(10)
        return

'''

def main():
    example = '''trans mode Forwarding traffic from a local port to another port
       traffic-forward -mode (U)trans -lhost 0.0.0.0 -lport 8083 -rhost 127.0.0.1 -rport 22 #ssh name@ip -p8083
       slave mode Remote traffic forwarding, forwarding traffic from intranet machines to public machines
        public machines:
            traffic-forward -mode listen -lport 8089 -rport 8088 (The order can be changed)
        intranet machines:
            traffic-forward -mode slave -lhost 127.0.0.1 -lport 22 -rhost x.x.x.x -rport 8089
        You PC
        ssh name@x.x.x.x -p8088
	'''
    parser = argparse.ArgumentParser(
        example
        )
    parser.add_argument('-mode', required=False, type=str, default=None,choices={'trans','slave','listen','Utrans','Uslave','Ulisten'}, help='mode')
    #parser.add_argument('-slave', required=False, type=str, default="n", help='slave fuction')
    parser.add_argument('-lport', required=False, type=int, default=None ,help='Port for forwarding traffic')
    parser.add_argument('-lhost', required=False, type=str, default=None ,help='IP for forwarding traffic')
    parser.add_argument('-rport', required=False, type=int, default=None ,help='Forward to target port')
    parser.add_argument('-rhost', required=False, type=str, default=None ,help='Forward to target ip')
    parser.add_argument('-debug', required=False, type=int, default=40 ,help='debug')
    args = parser.parse_args()
    if(args.mode == "trans"):
        ta = Trans(args.debug)
        ta.tran(args.rhost ,args.rport, args.lhost, args.lport)
        
    if(args.mode == "slave"):
        ta = Trans(args.debug)
        ta.slave(args.lhost, args.lport, args.rhost, args.rport)
        
    if(args.mode == "listen"):
        ta = Trans(args.debug)
        ta.listen(args.lport, args.rport)
        
    if(args.mode == "Ulisten"):
        ta = Trans(args.debug)
        ta.Ulisten(args.lport, args.rport)
        
    if(args.mode == "Utrans"):
        ta = Trans(args.debug)
        ta.Utran(args.lhost ,args.lport, args.rhost, args.rport)
        
    if(args.mode == "Uslave"):
        ta = Trans(args.debug)
        ta.Usalve(args.lhost, args.lport, args.rhost, args.rport)
        
    else:
        print("please use -h view help")
        
if __name__== "__main__":
    main()
#logger = logger()
#logger.info('info')
