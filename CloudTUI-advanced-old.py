import os
import boto
import sys
from boto.s3.connection import OrdinaryCallingFormat
from boto.s3.connection import S3Connection
from boto.ec2.regioninfo import RegionInfo
#from ssl import SSLSocket
import threading
import string
import socket
import subprocess
from clonevm import VM
import time



###DATI DI LOGIN
access_id=""
access_secret=""
host=""
port=0
cumulusport = 0
canonical_id=""
key = ""
hostmonitor = ""
portmonitor = 0
path = ""
monitorenable = 0
abletomonitor = 1
validate_certs_opt = False
p2 = 0
terminal = ""
###



#Flag globali
flag_rules = False
flag_instances = False
thread_instances = []
thread_rules = []
globvariables = []
vlock = threading.Lock()
vlock2 = threading.Lock()
kill = False





def loadvariables():
  global globvariables
  
  try:
      variables = open("nimbus/variables.txt", "r")
  except:
      print("Bad variables configuration file. Program Terminated.")
      exit()
  
  #Chop della prima riga
  line = variables.readline()
  line = variables.readline()[:-1]
  
  globvariables.append(line)
  
  i = 1
  
  while line != "###":
      i += 1
      line = variables.readline()[:-1]
      globvariables.append(line)
  
  variables.close()
  
  print("Loading Variables: SUCCESS\n")
  
  return 0
  



def loadrules():
  
  global flag_rules
  global vlock
  
 
  
  
  #Apro in lettura il file delle regole 
  try:
      rules = open("nimbus/rules.txt", "r")
  except:
      print("Bad rule file. Program Terminated.")
      exit()
  
  line = rules.readline()
  
  
  if line == "":
    vlock.acquire()
    flag_rules = False
    vlock.release()
    rules.close()
    return 1
    
  
  while line != "":  
      thread_rules.append(line)
      line = rules.readline()
      
  
  rules.close()
  
  vlock.acquire()
  flag_rules = False
  vlock.release()
  
  
  
  return 1
  


def verify(vm, var1, var2, op):
  
  global globvariables
  global hostmonitor
  global portmonitor

  
  try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  except socket.error, msg:
    sys.stderr.write("[ERROR] %s\n" % msg[1])
    sys.exit(1)
  
  
 
  
  try:
    sock.connect((hostmonitor, portmonitor))
  except socket.error, msg:
    sys.stderr.write("[ERROR] %s\n" % msg[1])
    sys.exit(2)
  
  
 
  
  #Invio vm_id * resource
  
  sock.send(str(vm) + "\b" + str(var1))
  
  #il valore di var1 lo devo ricavare obbligatoriamente
  
 
  
  data = sock.recv(6)
  string = ""
 # print("Ricevuto: " + str(data))
  #while len(data):
    #string = string + data
    #data = sock.recv(6)
  
  
  
  sock.close()
  

  #in data trovero' il valore del parametro che mi serve. In pratica il valore di var1 o i valori sia di var1 che di var2 (doppia request).
  
  v1 = int(data)
  
  
  
  if ((var2 in globvariables) == True):
    try:
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, msg:
      sys.stderr.write("[ERROR] %s\n" % msg[1])
      sys.exit(1)
    
    try:
      sock.connect((HOST, PORT))
    except socket.error, msg:
      sys.stderr.write("[ERROR] %s\n" % msg[1])
      sys.exit(2)
      
    sock.send(str(vm) + "\b" + str(var2))  
    data = sock.recv(6)
    string = ""
   
    sock.close()
    v2 = int(data) #v2 avra' il valore comunicato dal server
  else:
    v2 = int(var2)

  print("VALORE SOGLIA: " + str(v2) + "\n")
    ##effettuo la seconda richiesta per ottenere il valore di var2
    
  ##Altrimenti var2 e' un numero e posso effettuare la comparazione direttamente
  
  if (str(op) == ">"):
    #comparazione diretta
    if (int(var1) > int(v2)):
      return True
    else:
      return False
    
  if (str(op) == "<"):
    if (int(var1) < int(v2)):
      return True
    else:
      return False
      
  if (str(op) == "="):
    if (int(var1) == int(v2)):
      return True
    else:
      return False
      
  
 
  
  
  
  
  
  return 0
  
def terminateIt(vm): 

  #stampo l'elenco delle Vms, prendo in input l'indentificatore della vm che l'utente vuole terminare e la termino.
  
  global vlock2
  global access_id
  global access_secret
  global host
  global port
  global cumulusport
  global canonical_id
  global thread_instances
  global validate_certs_opt
  

  
  
  region = RegionInfo(name="nimbus", endpoint=host)
  ec2conn = boto.connect_ec2(access_id, access_secret, region=region, port=port)
  cf = OrdinaryCallingFormat()
  s3conn = S3Connection(access_id, access_secret, host=host, port=cumulusport, is_secure=False, calling_format=cf)
  
    
    
  try:
    ec2conn.terminate_instances(vm)#check come argomento
    print("Instance " + str(vm) + " terminated.")
  except Exception:
    print("Unable to terminate " + str(vm) + " instance.")
      
  vlock2.acquire()
  thread_instances.remove(vm)
  vlock2.release()

  return 0
  
def cloneIt(vm):
  #Mi collego al server e mi faccio restituire l'elenco delle istanze che ho in esecuzione
  global access_id
  global access_secret
  global host
  global port
  global cumulusport
  global canonical_id
  global path
  global validate_certs_opt

  
  region = RegionInfo(name="nimbus", endpoint=host)
  ec2conn = boto.connect_ec2(access_id, access_secret, region=region, port=port)
  cf = OrdinaryCallingFormat()
  s3conn = S3Connection(access_id, access_secret, host=host, port=cumulusport, is_secure=False, calling_format=cf)
  
  
  
  instances = ec2conn.get_all_instances()
  
  if len(instances) == 0:
    try:
      ec2conn.close()
      s3conn.close()
      return
    except:
      return 
  
  
  
  print("Your VMs List:\n")
  
  cnt = 1
  publicip = 0
  found = False
  
  for j in instances:
      if found == False:
	for i in j.instances:
	  if (i.id == vm):
	    publicip = i.ip_address
	    found == True
	    break
	  cnt = cnt + 1
      else:
	break

  #stringa = "/home/" + str(os.getlogin()) + "/nimbus-cloud-client-021/bin/cloud-client.sh --status > tmp.txt"    
  stringa = path + "\\bin\\cloud-client.sh --status > tmp.txt"    
  
  process = subprocess.Popen(stringa, shell=True) 
  
  process.wait()
  
  
  try:
      ftmp = open("tmp.txt", "r")
  except IOError:
      print("Program is unable to open a necessary file. Program Terminated.")
      kill = True
      exit()
  
  output = []
  line = ftmp.readline()
  i = 1
  
  while line != "":
      output.append(line)
      i += 1
      line = ftmp.readline()
  
  ftmp.close()    


  ip1 = 3
  

  vlock2.acquire()
  length = thread_instances
  vlock2.release()
  
  for n in range(0, len(length)):
      split = output[ip1].split()
      if (split[5] == publicip):
	vmclonetmp = output[ip1 + 6].split()
	vmclone = vmclonetmp[1]
	break
      ip1 = ip1 + 9
  
  #Salvo l'immagine sull'hd
  os.system(path + "/bin/cloud-client.sh --save --handle " + str(vmclone) + " --hours 1 --newname TMP")


  os.system(path + "/bin/cloud-client.sh --download --name TMP --localfile ./TMP")

  os.system(path + "/bin/cloud-client.sh --transfer --sourcefile TMP  --common")
      

  os.system(path + "/bin/cloud-client.sh --run --name TMP --hours 8")

  os.system(path + "/bin/cloud-client.sh --run --name TMP --hours 8")

  os.system(path + "/bin/cloud-client.sh --delete --common --name TMP")

  vlock2.acquire()
  thread_instances = ListRunningVms()
  vlock2.release()
 	
	
  return 0
  
  
def doAction(vm, action):
  
  if str(action) == "TERMINATE":
    terminateIt(vm)
    
  if str(action) == "CLONE":
    cloneIt(vm)
  
  return 0
  
def monitor():
  global thread_instances
  global vlock2
  global monitorenable
  global hostmonitor
  global portmonitor
  global abletomonitor
  
  
  if monitorenable == 0 or abletomonitor == 0:
    return 1
  
  
  #controllo che il server di monitoring sia online
  
  try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  except socket.error, msg:
    sys.stderr.write("[ERROR] %s\n" % msg[1])
    sys.exit(1)
  
  
  try:
    sock.connect((hostmonitor, int(portmonitor)))
  except socket.error, msg:
    sys.stderr.write("Monitoring server is unreachable. This can be due to a CloudTUI-advance configuration error.\n Please check your login.txt monitoring configuration data and restart CloudTUI-advance.\n")
    abletomonitor = 0
    return 1
  
  
  
  #per ogni regola, e per ogni macchina, verifico
  for rule in thread_rules:
    actual = string.split(rule, " ")
    var1 = actual[0]
    op = actual[1]
    var2 = actual[2]
    action = actual[3]
    vlock2.acquire()
    for vm in thread_instances:
      time.sleep(2)
      verified = verify(vm, var1, var2, op)
      if verified == True:
	doAction(vm, action)
    vlock2.release()
    
  return 1

def procRules():
  #carico in memoria le rules
  #... e continuo a processarle, per ogni istanza running
  #la lista delle istanze running e' caricata anch'essa in memoria.
  #se viene modificato il flag globale delle rules, ricarico le rules.
  #se viene modificato il flag globale delle istanze, ricarico le istanze.
  
  #fase preliminare:
  #loadrules()
  #loadinstances()
  #goto Loop
  global flag_rules
  global kill
  
  loadrules()
  
  
  
  
  #il Loop si compone di diverse fasi:
  #while True:
  #  if check_flags():  
  #     reload_rules or/and reload_instances
  #  else:
  #    check_rules()
  
  
  while True:
    if kill == True:
      exit(0)
    if flag_rules == True:
      loadrules()
    monitor()
      

  return 1  




def multiProc():
  global p2
  #p = threading.Thread(target = MainLoop)
  p2 = threading.Thread(target = procRules)
 
  #p.start()
  p2.start()  

  MainLoop()




def MainLoop():
  
    

    while True:
      showMMenu()
    
    
    return 1

def ShowHelp():
    print("")
    return 1

def Exit():
    global p2
    global kill
  
    print("Program Terminated")
    kill = True
    #p2.stop()
    sys.exit()
    

def ShowRules():
    
    global kill
    
    print("Actual Rules:\n")
    #Apro in lettura il file delle regole e stampo il contenuto regola per regola
    try:
        rules = open("nimbus/rules.txt", "r")
    except:
        print("Bad rule file. Program Terminated.")
        kill = True
        exit()
    
    line = rules.readline()
    i = 1

    if line == "":
      print("There isn't any rule in rules file.")
      
   
    
    
    
    while line != "":
        print(str(i) + ") " + str(line) + "\n")
        i += 1
        line = rules.readline()
    
    rules.close()
    
    
    
    return 1

def MakeRule():
  
    global vlock
    global flag_rules
    global kill
    
    print("You are going to make a new rule.\n1) Continue;\n2) Go back;\n")
    
    test = 0
    
    while test != 1:
	try:
	  choice = input()
	  if (choice == 1):
	      test = 1
	  if (choice == 2):
	      test = 1
	      return
	except Exception:
	  print("Unavailable choice!")
    
    print("In order to make a new rule, you need to specify two variables, one operator and one action.\n")
        
    #Stampo l'elenco delle variabili possibili tra cui scegliere la prima
    
    print("Please choose the first variable:")
    
    try:
        variables = open("nimbus/variables.txt", "r")
    except:
        print("Bad variables configuration file. Program Terminated.")
        kill = True
        exit()
    
    #Chop della prima riga
    line = variables.readline()
    line = variables.readline()[:-1]
    
    check = []
    
    check.append(line)
    
    i = 1
    
    while line != "###":
        print(str(i) + ") " + str(line))
        i += 1
        line = variables.readline()[:-1]
        check.append(line)
    
    variables.close()
    
    
    
    print("\n")
    
    
    test = 0
    
    while test == 0:
	try:
	  var1 = input("Variable: ")
	  try:
	    var1 = check[var1 - 1]
	    test = 1
	  except IndexError:
	    continue
        except Exception:
	  print("Unavailable choice!")
	  continue
            
        
    
    
    
    #Scelgo la seconda variabile
     
    
    print("\nIf you want input a number as second variable, insert 0 else insert 1: ")
    
    while True:
      try:
	what = input()
	if int(what) == 0 or int(what) == 1:
	  break
      except Exception:
	print("Unavailable choice!")
	continue
      
    
    
    if what == 1:
      
      try:
	  variables = open("nimbus/variables.txt", "r")
      except:
	  print("Bad variables configuration file. Program Terminated.")
	  kill = True
	  exit()
      
      line = variables.readline()
      line = variables.readline()
      
      i = 1
      
      while line != "###":
	  print(str(i) + ") " + str(line))
	  i += 1
	  line = variables.readline()[:-1]
      
      variables.close()
      
      test = 0
      
      while test == 0:    
	  try:
	    var2 = input("Variable: ")
	    
	    try:
		var2 = check[var2 - 1]
		test = 1
	    except IndexError:
		continue
	  except Exception:
	    print("Unavailable choice!")
	    continue
    
    
    if what == 0:
      while True:
	try:
	  print("Please insert a value: ")
	  var2 = input()
	  break
	except Exception:
	  print("Unavailable choice!")
	  continue
       
    
    
   
    #Scelgo l'operatore
    
    test = 0
    
    while test != 1:
        try:
	    op = input("Please choose an operator: \n1) >\n2) <\n3) =\n") 
	    if (int(op) == 1): 
		test = 1
		op = ">"
	    if (int(op) == 2):
		test = 1
		op = "<"
	    if (int(op) == 3):
		test = 1
		op = "="
	    if (int(op) > 3 or int(op) < 1):
		print("Invalid Operator\n")
        except Exception:
	    print("Invalid Operator\n")
	    continue
    
    #Stampo l'elenco delle azioni disponibili
    
    print("Operator " + op)
    
    checkactions = []
    
    try:
        actions = open("nimbus/variables.txt", "r")
    except:
        print("Bad variables configuration file. Program Terminated.")
        kill = True
        exit()
    
    line = actions.readline()[:-1]
    
    while line != "//ACTIONS\n":
        line = actions.readline()
    
    
    line = actions.readline()[:-1]
    
    checkactions.append(line)
    
    i = 1
    
    while line != "***":
        print(str(i) + ") " + str(line))
        i += 1
        line = actions.readline()[:-1]
        checkactions.append(line)
    
    actions.close()
    
    test = 0
    
    while test == 0:    
	try:
	  action = input("Action: ")
	  action = checkactions[action - 1]
	  test = 1
        except Exception:
	  print("Invalid Operator\n")
	  continue
    
    print(action)
    
    #aggiorno il file delle regole
    try:
	update = open("nimbus/rules.txt", "a")
	if int(what) == 1:
	  update.write(var1+" "+op+" "+var2+" "+action+"\n")
	if int(what) == 0:
	  update.write(var1+" "+op+" "+str(var2)+" "+action+"\n")
      
    except IOError:
        print("Bad rules file. Program Terminated.")
        kill = True
        exit()

    update.close()
    
    print("Rule saved.\n")
    
    vlock.acquire()
    flag_rules = True
    vlock.release()
        
    
    return 1

def DeleteRule():
    
    global vlock
    global flag_rules
    global kill
    #stampo il contenuto del file delle regole
    
    
    
    print("Please select the rule that you want to remove:")
    
    try:
        frules = open("nimbus/rules.txt", "r")
    except IOError:
        print("Bad rules file. Program Terminated.")
        kill = True
        exit()
    
    rules = []
    line = frules.readline()
    i = 1
    
    if line == "":
      print("There isn't any rule in rules file.")
      return 1
    
    while line != "":
        rules.append(line)
        print(str(i) + ") " + str(line))
        i += 1
        line = frules.readline()
    
    frules.close()
    
    print("Rule: ")
    
    while True:
        try:      
            choice = input()
            check = rules[choice-1]
            break
        except Exception:
            print("Unavailable choice!n")
    
    try:
        source = open("nimbus/rules.txt","r")
    except IOError:
        print("Bad rules file. Program Terminated.")
        kill = True
        exit()
        
    try:
        tmp = open("nimbus/tmp.txt", "w")
    except IOError:
        print("You don't have enough space to do this operation.")
        source.close()
        return
    
    for line in source:
        if (line != check):
            tmp.write(line)
    
    source.close()
    tmp.close()
            
    os.remove("nimbus/rules.txt")
    os.rename("nimbus/tmp.txt", "nimbus/rules.txt")
    
    vlock.acquire()
    flag_rules = True
    vlock.release()
    
    return 1

def RunVm():  

    global vlock2
    global access_id
    global access_secret
    global host
    global port
    global cumulusport
    global canonical_id
    global key
    global path
    global validate_certs_opt
    
    print("List of all available images:\n")
    
    
    
    region = RegionInfo(name="nimbus", endpoint=host)
    ec2conn = boto.connect_ec2(access_id, access_secret, region=region, port=port)
    cf = OrdinaryCallingFormat()
    s3conn = S3Connection(access_id, access_secret, host=host, port=cumulusport, is_secure=False, calling_format=cf)
    
    imgs = []
    
    cnt  = 1
    
    images = ec2conn.get_all_images()
    
    
    for i in images:
	print(str(cnt) + ") " + i.id)
	imgs.append(i.id)
	cnt = cnt + 1
    
    try:
      ec2conn.close()
      s3conn.close()
    except:
      print("Continue ...")
    
    

    
    
    while True:
      print("Please select the number of the image to load in your VM or insert 0 to turn back: ")
      try:
	vm = input()
	if int(vm) == 0:
	    return
	check = imgs[vm-1]
	break
      except Exception:
	print("Unavailable choice!")
      
	  
	
	
    num = 0
    
    while num <= 0:
      try:
	print("Number of VMs: ")
	num = int(input())
      except Exception:
	print("Unavailable choice!")
	
      
    
    hours = 0
    while hours <= 0:
      try:
	print("How many hours should your VMs work: ")
	hours = int(input())
      except Exception:
	print("Unavailable choice!")	

  
    #Lo script deve avvalersi del cloud-client per eseguire le VM, altrimenti non si puo' garantire la possibilita' di effettuare
    #il cloning con l'attuale versione di Boto.

          
   
     
    for i in range(0, int(num)):
      os.system(path + "/bin/cloud-client.sh --run --name " + str(check) + " --hours " + str(hours))


    

    

    vlock2.acquire()
    thread_instances = ListRunningVms()
    vlock2.release()

      
        
    
      
      
    return 1

def TerminateVm():
    #stampo l'elenco delle Vms, prendo in input l'indentificatore della vm che l'utente vuole terminare e la termino.
    
    global vlock2
    global access_id
    global access_secret
    global host
    global port
    global cumulusport
    global canonical_id
    global validate_certs_opt

    
    ids = []
    
    
    ids = ListRunningVms()
    

    
    if len(ids) == 0:
      return 1
    
    
    region = RegionInfo(name="nimbus", endpoint=host)
    ec2conn = boto.connect_ec2(access_id, access_secret, region=region, port=port)
    cf = OrdinaryCallingFormat()
    s3conn = S3Connection(access_id, access_secret, host=host, port=cumulusport, is_secure=False, calling_format=cf)
    
    
    cnt  = 1
    
    while len(ids) != 0:
      print("Please select the number of the VM you want to shut down or '0' to stop 'Terminate' operation: ")
      
      while True:
	try:
	  vm = input()
	  
	  if (vm == 0):
	    try:
	      ec2conn.close()
	      s3conn.close()
	      print("Continue...")
	    except:
	      print("Continue...")
	    
	    return 1
	    
	  check = ids[vm-1]
	  
	  
	  break
	except Exception:
	  print("Unavailable choice!")
	
	
      try:
	ec2conn.terminate_instances(str(check))#check come argomento
	print("Instance terminated.")
	ids = ListRunningVms()
      except Exception:
	print("Unable to terminate instance.")
      
    return 1

def ListRunningVms():
    #Mi collego al server e mi faccio restituire l'elenco delle istanze che ho in esecuzione
    global access_id
    global access_secret
    global host
    global port
    global cumulusport
    global canonical_id
    global validate_certs_opt

    
    region = RegionInfo(name="nimbus", endpoint=host)
    ec2conn = boto.connect_ec2(access_id, access_secret, region=region, port=port)
    cf = OrdinaryCallingFormat()
    s3conn = S3Connection(access_id, access_secret, host=host, port=cumulusport, is_secure=False, calling_format=cf)
    
    ids = []
    
    instances = ec2conn.get_all_instances()
    
    if len(instances) == 0:
      print("You don't have any instance running or pending.")
      try:
	ec2conn.close()
        s3conn.close()
        print("Continue ...")
      except:
	print("Continue ...")
      return ids
    
    
    print("Your VMs List:\n")
    
    cnt = 1
    
    for j in instances:
	for i in j.instances:
	  print("\n" + str(cnt) + ") \nINSTANCE: " + i.id + "/" + i.image_id + " " + "\nPUBLIC DNS NAME: " + i.public_dns_name + "\nSTATUS: " + i.state + "\n")
	  ids.append(i.id)
	  cnt = cnt + 1
	  
    
    try:
      ec2conn.close()
      s3conn.close()
    except:
      print("Continue ...")
    
    return ids

def CloneVm():
    #Clone di una Vm. Stampo la lista delle Vms in esecuzione attendo l'input di un ID e clono secondo le specifiche dell'utente.
    
    global access_id
    global access_secret
    global host
    global port
    global cumulusport
    global canonical_id
    global thread_instances
    global vlock2
    global path
    
    #Lancio il cloud-client con parametro --status e ne salvo l'output nel file tmp.txt.
    #Apro tmp.txt e lo parsifico alla ricerca dei vm-handle per ogni vm-id.
    #Chiedo all'utente quale vm intende clonare.
    #Eseguo i comandi del cloning.
 
   
    
    
    stringa = path + "/bin/cloud-client.sh --status > tmp.txt"    
    
    process = subprocess.Popen(stringa, shell=True) 
    
    process.wait()
    
    
    try:
        ftmp = open("tmp.txt", "r")
    except IOError:
        print("Program is unable to open a necessary file. Program Terminated.")
        kill = True
        exit()
    
    output = []
    line = ftmp.readline()
    i = 1
    
    while line != "":
        output.append(line)
        i += 1
        line = ftmp.readline()
    
    ftmp.close()    

    #Cerco le righe che iniziano per '[*]' e '*' in sequenza
    #Parser:
    #
    #Passo 1: id1 = 3 vmcloneid1 = 9
    #Passo k: idk = vmcloneid[k-1] + 3   vmcloneidk = vmcloneid[k-1] + 9
    
    
    
    arrayvm = []

    id1 = 2
    vmcloneid1 = 9
    image = 10

    vlock2.acquire()
    length = thread_instances
    vlock2.release()
   
    for n in range(0, len(length)):
	split = output[id1].split()
	split2 = output[vmcloneid1].split()
	split3 = output[image].split()
	tmp = VM(str(split[6]), str(split2[1]), str(split3[1]))
	arrayvm.append(tmp)
	id1 = id1 + 10
	vmcloneid1 = vmcloneid1 + 10
	image = image + 10
    
    cnt  = 1
    vms = []    
    
    for i in arrayvm:
	print(str(cnt) + ") " + i.vmid + " (" + i.vmcloneid + " image: " + i.image + ")")
	vms.append(i.vmcloneid)
	cnt = cnt + 1
    
    
    
    
    while True:
      print("Please select the VM that you want to clone or insert 0 to turn back: ")
      try:
	vm = input()
	if int(vm) == 0:
	  return
	check = vms[vm-1]
	break
      except Exception:
	print("Unavailable choice!")
    
  
    #Salvo l'immagine sull'hd
    os.system(path + "/bin/cloud-client.sh --save --handle " + str(check) + " --hours 1 --newname TMP")
    
    
    os.system(path + "/bin/cloud-client.sh --download --name TMP --localfile ./TMP")
    
    os.system(path + "/bin/cloud-client.sh --transfer --sourcefile TMP  --common")
       
    
    
    hours = 0
    while hours <= 0:
      try:
	print("How many hours should your cloned VM works: ")
	hours = int(input())
      except Exception:
	print("Unavailable choice!")

    os.system(path + "/bin/cloud-client.sh --run --name TMP --hours " + str(hours))

    os.system(path + "/bin/cloud-client.sh --delete --common --name TMP")
    
    vlock2.acquire()
    thread_instances = ListRunningVms()
    vlock2.release()

    
    
    
    return 1

def LoginVm():
    #Stampo l'elenco delle Vms e chiedo in input l'ID della macchina cui ci si vuole loggare.
    #Lancio un terminale passando come parametro una stringa "ssh #VM#@futuregrid.org"
    #FINE
    global access_id
    global access_secret
    global host
    global port
    global cumulusport
    global canonical_id
    global validate_certs_opt
    global terminal

    
    ids = []
    
    ids = ListRunningVms()
    
    if len(ids) == 0:
      return 1
    
    
    region = RegionInfo(name="nimbus", endpoint=host)
    ec2conn = boto.connect_ec2(access_id, access_secret, region=region, port=port)
    cf = OrdinaryCallingFormat()
    s3conn = S3Connection(access_id, access_secret, host=host, port=cumulusport, is_secure=False, calling_format=cf)
    
    test = 0
    
    while test == 0:
      print("Please insert a valid ID or '0' to stop 'Login' operation: ")
      try:
	vm = input()
	if vm == 0:
	    try:
	      ec2conn.close()
	      s3conn.close()
	      print("Continue...")
	    except:
	      print("Continue...")
	    return 1
	try:
	  vm = ids[vm-1]
	  test = 1
	except IndexError:
	  print("Bad ID")
	  continue
	
	    
      except Exception:
	print("Unavailable choice!")
	continue
	  
    print("Continue ...")
    
    
    instances = ec2conn.get_all_instances()
    
    for i in instances:
      for j in i.instances:
	if j.id == str(vm):
	  launch = j.public_dns_name
    
    
    
    if terminal == "default":
      stringa = "xterm -e ssh root@" + launch
    else:
      stringa = terminal + " -e ssh root@" + launch

    process = subprocess.Popen(stringa, shell=True, stdout=subprocess.PIPE)
    


    
  
    return 1


def VmsCommands():
    print("1) Run VM;\n2) Terminate VM;\n3) Print VMs status;\n4) Clone VM;\n5) Login to a VM;\n6) Go back;\n")
    
    test = 0
    
    while test != 1:
        try:
	  choice = input("Please make a choice: ")

	  if (choice == 1):
	    test = 1
	    RunVm()
	  if (choice == 2):
	    test = 1
	    TerminateVm()
	  if (choice == 3):
	    test = 1
	    ListRunningVms()
	  if (choice == 4):
	    test = 1
	    CloneVm()
	  if (choice == 5):
	    test = 1 
	    LoginVm()
	  if (choice == 6):
	    test = 1
	    return
	  if (choice < 1 or choice > 6):
	    print("Unavailable choice!")
	  
	except Exception:
	  print("Unavailable choice!")
            
    return 1

def RulesCommands():
    print("1) Show Actual Rules;\n2) Make new Rule;\n3) Delete a Rule;\n4) Go back;\n")
    
    test = 0
    
    while test != 1:
        
        try:
	  choice = input("Please make a choice: ")
      
	  if (choice == 1):
	      test = 1
	      ShowRules()
	  if (choice == 2):
	      test = 1
	      MakeRule()
	  if (choice == 3):
	      test = 1
	      DeleteRule()
	  if (choice == 4):
	      test = 1
	      return
        except Exception:
	  print("Unavailable choice!")
	  continue

    return 1

    
def monitorOnOff():
  global monitorenable
  
  choice = 0
  
  if monitorenable == 0:
    while (choice != 0 or choice != 1):
      print("Monitoring is off. Do you want to turn it on?\n")
      try:
	choice = input("(0 - no, 1 - yes): ")
	if choice == 0:
	  return
	if choice == 1:
	  monitorenable = 1
      except Exception:
	print("Unavailable choice!")
  else:
    while (choice != 0 or choice != 1):
      print("Monitoring is on. Do you want to turn it off?\n")
      try:
	choice = input("(0 - no, 1 - yes): ")
	if choice == 0:
	  return
	if choice == 1:
	  monitorenable = 0
      except Exception:
	print("Unavailable choice!")
      
  return 0
    
def OtherCommands():
    
    global kill
    global p2
    
    print("1) Show Help;\n2) Exit Program;\n3) Monitoring \n4) Go back;\n")
    
    test = 0
    
    while test != 1:
        
        try:
	  choice = input("Please make a choice: ")
      
	  if (choice == 1):
	      test = 1
	      ShowHelp()
	  if (choice == 2):
	      test = 1
	      #p2.stop()
	      Exit()
	  if (choice == 3):
	      test = 1
	      monitorOnOff()
	  if (choice == 4):
	      test = 1
	      return
	  if (choice > 4 or choice < 1):
	      print("Unavailable choice!")
	except Exception:
	  print("Unavailable choice!")
	  continue
    
    return 1

def showMMenu():
    
    print("Main Menu:\n")
    print("1) VMs Commands;\n2) Rules Commands;\n3) Other Commands\n")
    
    
    
    test = 0
    
    while test != 1:
        
	try:
	    choice = input("Please make a choice: ")
	
	    if (choice == 1):
		test = 1
		VmsCommands()
	    if (choice == 2):
		test = 1
		RulesCommands()
	    if (choice == 3):
		test = 1
		OtherCommands()
	except Exception:
	   print("Unavailable choice!")
	   continue
	
    return
    
    
    

def showMenu():
    global kill
  
    print("CloudTUI-advance")
    print("Please select the Cloud platform that you want to use:")
    
    try:
        platforms = open("platforms.txt", "r")
    except IOError:
        print("Bad platforms configuration file. Program Terminated.")
        kill = True
        exit()
    
    
    
    plat = []
    line = platforms.readline()
    i = 1
    
    while line != "":
        plat.append(line)
        print(str(i) + ") " + line.replace('\n', ''))
        i += 1
        line = platforms.readline()
    
    platforms.close()
    
    
    
    while True:
        try:      
	    print("Please make a choice: ")
            choice = input()
            check = plat[choice-1]
            print(check)
            break
        except Exception:
            print("Unavailable choice!n")
        
    
    return check
    
    
def checkNimbus():
    
    global access_id
    global access_secret
    global host
    global port
    global cumulusport
    global canonical_id
    global key
    global thread_instances
    global hostmonitor
    global portmonitor
    global path
    global monitorenable
    global validate_certs_opt
    global terminal


    #Caricamento dei dati di login
    
    
    #Apro in lettura il file dei dati di login
    try:
	login = open("nimbus/login.txt", "r")
    except:
	print("Bad login data file. Program Terminated.")
	exit()
    
    #Leggo i dati dal file
    
    
    cnt = 0
    
    line = login.readline()[:-1]
    
    while (line != None):
	tmp = line.split()
	
	if (len(tmp) != 0):
	
	  if tmp[0] == "PORT":
	      port = int(tmp[2])
	      print("PORT: " + str(port))
	      cnt = cnt + 1
	      
	  if tmp[0] == "CANONICALID":
	      canonical_id = str(tmp[2])
	      print("CANONICAL_ID: " + str(canonical_id))
	      cnt = cnt + 1
	      
	  if tmp[0] == "HOSTMON":
	      hostmonitor = str(tmp[2])
	      print("MONITOR HOST: " + str(hostmonitor))
	      cnt = cnt + 1
	      
	  if tmp[0] == "MONPORT":
	      portmonitor = str(tmp[2])
	      print("MONITOR HOST PORT: " + str(portmonitor))
	      cnt = cnt + 1

	  if tmp[0] == "PATH":
	      path = str(tmp[2])
	      print("CLOUD CLIENT PATH: " + str(path))
	      cnt = cnt + 1	    
	      
	  if tmp[0] == "MONITOR_ENABLED":
	      monitorenable = int(tmp[2])
	      print("MONITORING ENABLED: " + str(monitorenable))
	      cnt = cnt + 1	    
	      
	  if tmp[0] == "VALIDATE_CERTS":
	      if tmp[2] == 0:
		validate_certs_opt = False
	      else:
		validate_certs_opt = True
	      print("VALIDATE CERTS: " + str(validate_certs_opt))
	      cnt = cnt + 1	      
	      
	  if tmp[0] == "SSHKEYID":
	      for i in tmp[2:len(tmp)]:
		if len(key) != 0:
		  key = str(key) + " " + str(i)
		else:
		  key = str(key) + str(i)
	      
	      print("SSH KEY NAME: " + str(key))
	      cnt = cnt + 1
	      
	  if tmp[0] == "TERMINAL":
	      terminal = str(tmp[2])
	      print("TERMINAL: " + str(terminal))
	      cnt = cnt + 1	
	    
	
	
	if cnt == 9:
	    break;
	
	line = login.readline()[:-1]
    
    
    if (cnt < 9):
	print("Bad login data file. Program terminated.\n")
	exit()
	
   
	
    login.close()
    

    
    #Leggo gli altri dati necessari da cloud.properties
    
    
    
    try:
	login = open(path + "/conf/cloud.properties", "r")
    except:
	print("Bad \"cloud.properties\" file. Program Terminated.")
	exit()
    
    #Leggo i dati dal file
    
    
    
    cnt = 0
    
    line = login.readline()[:-1]
    
    while (line != None):
	
	if (line != ""):
	    #controllo per ogni riga se c'e' uno dei parametri che mi servono
	   
	    if (str(line)[:15] == "vws.repository="):
	      #devo spezzare la linea in hostname e porta
	      tocut = list(line[15:])
	      
	      host = ""
	      strport = ""
	      test = 0
	      
	      for i in tocut:
		if test == 1:
		  strport = strport + i
	        if i != ':' and test == 0:
		  host = host + i
		else:
		  test = 1
	      
	      
	      
	      cumulusport = int(strport)
	      print "HOST: " + host
	      print "PORT: " + str(cumulusport)
	      cnt = cnt + 1
	      
	    if (str(line)[:20] == "vws.repository.s3id="):
	      access_id = str(line)[20:]
	      print "ACCESS_ID: " + access_id
	      cnt = cnt + 1
	    
	    if (str(line)[:21] == "vws.repository.s3key="):
	      access_secret = str(line)[21:]
	      print "ACCESS_SECRET: " + access_secret
	      cnt = cnt + 1
	    
	
	
	if cnt == 3:
	    print("Good login data file.\n")
	    break;
	
	line = login.readline()[:-1]
    
    
    
    if (cnt < 3):
	print("Bad \"cloud.properties\" file. Program terminated.\n")
	exit()   
	
    login.close()
    
    
    
    
    print("Trying connection to nimbus Platform ... please wait.\n")
    
    
    
    region = RegionInfo(name="nimbus", endpoint=host)
    
    
    
    try:
    
        ec2conn = boto.connect_ec2(access_id, access_secret, region=region, port=port)
        cf = OrdinaryCallingFormat()
        s3conn = S3Connection(access_id, access_secret, host=host, port=cumulusport, is_secure=False, calling_format=cf)
        ec2conn.close()
        s3conn.close()
        
    except Exception:
        print("Login Data Check: SUCCESS.")   
	
    
    print("Connection OK\n")
		
    print("Retrieving running VMs... please wait.\n")
    
    thread_instances = ListRunningVms()
    
    print("Running VMs: " + str(thread_instances))

 
    

def start():
    
    #Viene mostrato il menu' con le scelte possibili per la piattaforma
    choice = showMenu()
    
    #in base alla piattaforma selezionata, viene caricato il file di configurazione corrispondente
    #fase futura DA IMPLEMENTARE
       
    
    #vengono caricate le informazioni di login dal file di configurazione corrispondente alla piattaforma selezionata
    
    #check dei dati di login (mediante una connect)
    
    checkNimbus()
    
    
    #caricamento delle variabili di monitoring
    loadvariables()
    
    #ho superato tutti i check iniziali, posso spostarmi nel Main Loop avviando il secondo thread di supporto
    
    multiProc()
    
    
   
    
    
    


start()

    
