import socket, urllib3, json, time
global debug
global serv_conf

############################## configuration
debug = "off"
serv_conf = "Optimal"
version = "v0.3.5"
servers = "gmail.com, outlook.com, yandex.com, mail.ru"
protected = " Protection version: v1.4"
############################################

print("\x1B[33m                           ___ __                        .__.__   ")
print("\x1B[33m  ______ ____   ____    __| _//  |_  ____   _____  ____  |__|  |  ")
print("\x1B[33m /  ___// __ \ /    \  / __ |\   __\/  _ \ /     \|__  \ |  |  |  ")
print("\x1B[33m \___ \|  ___/|   |  \/ /_/ | |  | (  <_> )  Y Y  \/ __ \|  |  |__")
print("\x1B[33m/____  >\___  >___|  /\____ | |__|  \____/|__|_|  (____  /__|____/")
print("\x1B[33m     \/     \/     \/      \/                   \/     \/         ")
print(" ")
print("\x1b[37m [>] Library name: sendtomail")
print("\x1b[37m [>] Developer: Misha Korzhik")
time.sleep(0.4)

class server:
    def send(region:str, email:str, *message:str):
        if debug == "on":
            print("[3%] Debug mode ON")
            print("[7%] Server "+region)
            print("[11%] Starting to get URL")
            print("[20%] Getting json from URL")
        url = "https://raw.githubusercontent.com/mishakorzik/mishakorzik.menu.io/master/%D0%A1%D0%B5%D1%80%D0%B2%D0%B5%D1%80/https.json"
        http = urllib3.PoolManager()
        request = http.request('GET', url)
        data = json.loads(request.data.decode('utf8'))
        ip = str(data["mailip"])
        port = int(data["mailport"])
        request = http.request('GET', "https://api.ipify.org/")
        my_ip = request.data.decode('utf8')
        if debug == "on":
            print("[40%] URL json data decode")
        if debug == "on":
            print("[60%] Server IP "+ip+":"+str(port))
            print("[65%] My IP: "+my_ip)
            print("[70%] Checking IP on blacklist")
        message = " ".join([str(m) for m in message])
        check = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        check.connect((ip, port))
        check.sendall(bytes("free|check|ip|"+my_ip,'UTF-8')) #Checking IP for dangerousness
        code = check.recv(1024)
        get = code.decode('utf-8')
        if get == "blacklisted": #Blacklisted IP
            return "Access denied, you ip address blacklisted!"+protected
        elif get == "tor": #IP using Tor
            return "Access denied, please disable tor!"+protected
        elif get == "vpn" or get == "proxy": #IP using vpn
            return "Access denied, please disable vpn!"+protected
        else:
            if debug == "on":
                print("[80%] Server connected!")
            if region == "ru" or region == "ua" or region == "us" or region == "uk" or region == "in" or region == "au" or region == "zn" or region == "tw" or region == "sg" or region == "it" or region == "ca" or region == "fr" or region == "kr" or region == "ar" or region == "es":
                return "Error! You have entered an invalid mail server, available servers: "+servers
            else:
                check.sendall(bytes("smtp|"+region+"|"+email+"|"+message,'UTF-8'))
                if debug == "on":
                   print("[98%] Data send to server")
                code = check.recv(1024)
                code = code.decode('utf-8')
                check.shutdown(socket.SHUT_RDWR)
                check.close()
                return code
    def mail():
        if debug == "on":
            print("[7%] Debug mode ON")
            print("[11%] Starting to get URL")
            print("[20%] Getting json from URL")
        url = "https://raw.githubusercontent.com/mishakorzik/mishakorzik.menu.io/master/%D0%A1%D0%B5%D1%80%D0%B2%D0%B5%D1%80/https.json"
        http = urllib3.PoolManager()
        request = http.request('GET', url)
        data = json.loads(request.data.decode('utf8'))
        if debug == "on":
            print("[40%] URL json data decode")
        ip = str(data["mailip"])
        port = int(data["mailport"])
        if debug == "on":
            print("[60%] Server IP "+ip)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))
        if debug == "on":
            print("[80%] Server connected!")
        client.sendall(bytes("get|free|mail|account",'UTF-8'))
        if debug == "on":
            print("[98%] Data send to server")
        free = client.recv(1024)
        free = free.decode('utf-8')
        free = json.loads(free)
        client.shutdown(socket.SHUT_RDWR)
        client.close()
        print("sendtomail: "+version)
        return free
    def validate(email:str):
        url = "https://raw.githubusercontent.com/mishakorzik/mishakorzik.menu.io/master/%D0%A1%D0%B5%D1%80%D0%B2%D0%B5%D1%80/https.json"
        http = urllib3.PoolManager()
        request = http.request('GET', url)
        data = json.loads(request.data.decode('utf8'))
        ip = str(data["mailip"])
        port = int(data["mailport"])
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))
        client.sendall(bytes("free|email|validation|"+email,'UTF-8'))
        check = client.recv(512)
        check = check.decode('utf-8')
        client.shutdown(socket.SHUT_RDWR)
        client.close()
        return check
    def info(re=True):
        url = "https://raw.githubusercontent.com/mishakorzik/mishakorzik.menu.io/master/%D0%A1%D0%B5%D1%80%D0%B2%D0%B5%D1%80/https.json"
        http = urllib3.PoolManager()
        request = http.request('GET', url)
        data = json.loads(request.data.decode('utf8'))
        ip = str(data["mailip"])
        port = int(data["mailport"])
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))
        client.sendall(bytes("free|get|server|status",'UTF-8'))
        check = client.recv(512)
        check = check.decode('utf-8')
        client.shutdown(socket.SHUT_RDWR)
        client.close()
        if re:
            return check
        else:
            print(check)
    def debug(type:str):
        global debug
        if type == "on":
            debug = "on"
        else:
            debug = "off"
    def regions():
        return "SERVERS: "+servers

class tempmail:
    def create():
        if debug == "on":
            print("[3%] Debug mode ON")
            print("[7%] Searching server...")
            print("[11%] Starting to get URL")
            print("[20%] Getting json from URL")
        url = "https://raw.githubusercontent.com/mishakorzik/mishakorzik.menu.io/master/%D0%A1%D0%B5%D1%80%D0%B2%D0%B5%D1%80/https.json"
        http = urllib3.PoolManager()
        request = http.request('GET', url)
        data = json.loads(request.data.decode('utf8'))
        ip = str(data["mailip"])
        port = int(data["mailport"])
        request = http.request('GET', "https://api.ipify.org/")
        my_ip = request.data.decode('utf8')
        if debug == "on":
            print("[40%] URL json data decode")
        if debug == "on":
            print("[60%] Server IP "+ip+":"+str(port))
            print("[65%] My IP: "+my_ip)
            print("[70%] Checking IP on blacklist")
        check = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        check.connect((ip, port))
        check.sendall(bytes("free|check|ip|"+my_ip,'UTF-8')) #Checking IP for dangerousness
        code = check.recv(1024)
        get = code.decode('utf-8')
        if get == "blacklisted": #Blacklisted IP
            return "Access denied, you ip address blacklisted!"+protected
        elif get == "tor": #IP using Tor
            return "Access denied, please disable tor!"+protected
        elif get == "vpn" or get == "proxy": #IP using vpn
            return "Access denied, please disable vpn!"+protected
        else:
            if debug == "on":
                print("[80%] Server connected!")
            else:
                check.sendall(bytes("free|tempmail|service|create",'UTF-8'))
                if debug == "on":
                   print("[98%] Data send to server")
                code = check.recv(4096)
                code = code.decode('utf-8')
                check.shutdown(socket.SHUT_RDWR)
                check.close()
                return code
    def read(mail:str, domain:str):
        if debug == "on":
            print("[3%] Debug mode ON")
            print("[7%] Searching server...")
            print("[11%] Starting to get URL")
            print("[20%] Getting json from URL")
        url = "https://raw.githubusercontent.com/mishakorzik/mishakorzik.menu.io/master/%D0%A1%D0%B5%D1%80%D0%B2%D0%B5%D1%80/https.json"
        http = urllib3.PoolManager()
        request = http.request('GET', url)
        data = json.loads(request.data.decode('utf8'))
        ip = str(data["mailip"])
        port = int(data["mailport"])
        if debug == "on":
            print("[40%] URL json data decode")
        if debug == "on":
            print("[60%] Server IP "+ip+":"+str(port))
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))
        if debug == "on":
            print("[70%] Sending data to server")
        client.sendall(bytes("free|tempmail|"+mail+"|"+domain,'UTF-8'))
        if debug == "on":
            print("[80%] Feching data")
        data = client.recv(1024)
        if debug == "on":
            print("[97%] Getting data from server")
        data = data.decode('utf-8')
        client.shutdown(socket.SHUT_RDWR)
        client.close()
        return data


class custom:
    def data(data:str):
        if debug == "on":
            print("[3%] Debug mode ON")
            print("[7%] Searching server...")
            print("[11%] Starting to get URL")
            print("[20%] Getting json from URL")
        a01 = data.replace("^38", "free")
        a02 = a01.replace("%72", "get")
        a03 = a02.replace("%65", "server")
        a04 = a03.replace("%10", "status")
        a05 = a04.replace("%11", "status1")
        a06 = a05.replace("%12", "status2")
        a07 = a06.replace("%13", "status3")
        a08 = a07.replace("%14", "status4")
        a09 = a08.replace("%15", "status5")
        a10 = a09.replace("%73", "mail")
        a11 = a10.replace("^92", "|")
        a12 = a11.replace("*04", "email")
        a13 = a12.replace("*09", "mail")
        a14 = a13.replace("*07", "account")
        a15 = a14.replace("*23", "check")
        a16 = a15.replace("#24", "smtp")
        a17 = a16.replace("#17", "api")
        dat = a17.replace("#64", "random")
        if debug == "on":
            print("[35%] Text decoded")
        url = "https://raw.githubusercontent.com/mishakorzik/mishakorzik.menu.io/master/%D0%A1%D0%B5%D1%80%D0%B2%D0%B5%D1%80/https.json"
        http = urllib3.PoolManager()
        request = http.request('GET', url)
        data = json.loads(request.data.decode('utf8'))
        ip = str(data["mailip"])
        port = int(data["mailport"])
        if debug == "on":
            print("[40%] URL json data decode")
        if debug == "on":
            print("[60%] Server IP "+ip+":"+str(port))
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))
        if debug == "on":
            print("[70%] Sending data to server")
        client.sendall(bytes(dat,'UTF-8'))
        if debug == "on":
            print("[80%] Feching data")
        data = client.recv(1024)
        if debug == "on":
            print("[97%] Getting data from server")
        data = data.decode('utf-8')
        client.shutdown(socket.SHUT_RDWR)
        client.close()
        return data
