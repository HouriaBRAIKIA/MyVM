from flask import Flask
import virtualbox

app = Flask(__name__)
myvbox = virtualbox.VirtualBox()
session = virtualbox.Session()

@app.route("/qst1")
def qst1():
    #1) Afficher les machines virtuelles
    return "VM(s):\n + %s" % "\n + ".join([vm.name for vm in myvbox.machines])

@app.route("/qst2")
def qst2():
    #2) Afficher les machines virtuelles en cours d'execution
    namM = "Machines en exe : \n"
    for m in myvbox.machines:
        if m.state != 1:
            namM = namM + m.name
    return namM

@app.route("/qst4")
def qst4():
    #4) Creer une VM (!depuis un appareil virtuel)
    appliance = myvbox.create_appliance()
    appliance.read("C:/Users/pcstar/Desktop/ubuntu_server.ova")
    
    mynewbox = appliance.find_machine('ubuntu_server')  
    mynewbox.config.name = 'projet_cv'
    mynewbox.config.cpu = 2
    
    appliance.import_machines([mynewbox]).wait_for_completion()
    return "Vm created"

@app.route("/qst5")
def qst5():
    #5) Config la mémoire, cpu, nom du VM
    machine = myvbox.find_machine("projet_cv")
    session = machine.create_session()
    #mémoire
    session.machine.memorysize = 1024
    #cpu
    session.machine.cpu_count = 2
    #name   
    session.machine.name = 'projet_cv'
    session.machine.save_settings()
    session.unlock_machine()
    return "New name :), CPU : 2, memory 1024"

@app.route("/qst6")
def qst6():
    #6) Config taille disk
    machine = myvbox.find_machine("projet_cv")
    session = machine.create_session()
    session.Storage = 200
    return "Config taille disk ..."
    
@app.route("/qst7")
def qst7():
    #7) Démarer la VM
    machine = myvbox.find_machine("projet_cv")
    session = machine.create_session()
    progress = machine.launch_vm_process(session, "gui", [])
    progress.wait_for_completion()
    return "Démarage VM ..."
    
@app.route("/qst8")
def qst8():
    #8) Arreter la VM
    machine = myvbox.find_machine("projet_cv")
    session = machine.create_session()
    session.console.power_down()
    return "Bye :)"

@app.route("/qst10")
def qst10():
    #10) Config la carte réseau d'une machine existante
    from virtualbox.library import NetworkAttachmentType
    
    machine = myvbox.find_machine("projet_cv")
    session = machine.create_session()
    adapter = session.machine.get_network_adapter(1)
    adapter.enabled = True
    adapter.attachment_type = NetworkAttachmentType.bridged
    session.machine.save_settings()

@app.route("/qst11")
def qst11():
    #8) Recupérer IP d'une machine
    vm = myvbox.find_machine('projet_cv')
    res = vm.enumerate_guest_properties('/VirtualBox/GuestInfo/Net/0/V4/IP')
    return list(res)

app.run(host="127.0.0.1",port=60000)
