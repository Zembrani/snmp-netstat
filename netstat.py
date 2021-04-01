from easysnmp import Session
import easysnmp
from tabulate import tabulate

def printTable(table, header):
    print(tabulate(
        table,
        headers = header
    ))

#
# Funcao que pega as listas de valores geradas e imprimme em forma de grid
#
def printGridTCP(localAddress, localPort, remAddress, remPort, status):
    table = []
    for i in range(0, len(localAddress)):
        table.append(['tcp',
                        localAddress[i].value,
                        localPort[i].value,
                        remAddress[i].value,
                        remPort[i].value,
                        "ESTABLISHED" if status[i].value == "5" else status[i].value
                    ])
    printTable(table, ['Protocol', 'Local IP', 'Local Port', 'Remote IP', 'Remote Port', 'Status'])

#
# Funcao que pega as listas de valores geradas e imprimme em forma de grid
#
def printGridUDP(localAddress, localPort):
    table = []
    for i in range(0, len(localAddress)):
        table.append(['udp', localAddress[i].value, localPort[i].value])
    printTable(table, ['Protocol', 'Local IP', 'Local Port'])


if __name__ == "__main__":

    print("Inform the agent IP:")
    # IP do agente mantido fixo por praticidade
    ip = "192.168.1.45"
    # ip = input()
    print("Inform the method (tcp or udp):")
    method = input()

    # Informacao do session referentes ao usuario do gerente criado
    try:
        session = Session(
            hostname=ip,
            community='public',
            version=3,
            security_username= "demo",
            auth_password= "12345678",
            privacy_password= "12345678",
            security_level='authPriv',
            auth_protocol='MD5',
            privacy_protocol="DES"
        )
    except easysnmp.EasySNMPError:
            print("*** IP agent error ***")

    #
    # Chamadas walk para os OID referentes ao tcp
    #
    if 'tcp' in method:
        localAddress = session.walk('tcpConnLocalAddress') # parent 1.3.6.1.2.1.6.13.1
        localPort = session.walk('tcpConnLocalPort')
        remAddress = session.walk('tcpConnRemAddress')
        remPort = session.walk('tcpConnRemPort')
        status = session.walk('tcpConnTable')
        
        printGridTCP(localAddress, localPort, remAddress, remPort, status)
    
    print()
    #
    # Chamadas walk para os OID referentes ao udp
    #
    if 'udp' in method:
        localAddress = session.walk('udpLocalAddress')
        localPort = session.walk('udpLocalPort')

        printGridUDP(localAddress, localPort)