import os
import sys
import logging
import platform
import errno

## Logging stuff
logging.basicConfig(filename='hardening.log' ,format='%(asctime)s - %(name)s - %(levelname)s | %(message)s |', stream=sys.stdout, level=logging.INFO)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s | %(message)s |')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

def hardenssh():
    with open("/etc/ssh/sshd_config", "a") as myfile:
        myfile.write("ClientAliveCountMax 2" + "\n" +
                     "Compression no" + "\n" +
                     "MaxAuthTries 2" + "\n" +
                     "MaxSessions 2" + "\n" +
                     "TCPKeepAlive no" + "\n" +
                     "UsePrivilegeSeparation SANDBOX" + "\n" +
                     "AllowAgentForwarding no" + "\n" +
                     "Banner /etc/issue.net")
    os.system('sudo service ssh restart')
    logging.info('SSHD |Added SSH config hardening')

def hardenkernel():
    with open("/etc/sysctl", "a") as myfile:
        myfile.write("fs.suid_dumpable  0" + "\n" +
                     "kernel.core_uses_pid 1" + "\n" +
                     "kernel.kptr_restrict 2" + "\n" +
                     "kernel.sysrq 0" + "\n" +
                     "net.ipv4.conf.all.forwarding 0" + "\n" +
                     "net.ipv4.conf.all.log_martians 1" + "\n" +
                     "net.ipv4.conf.all.send_redirects 0" + "\n" +
                     "net.ipv4.conf.default.log_martians 1" + "\n" +
                     "net.ipv4.tcp_syncookies 1" + "\n" +
                     "net.ipv4.tcp_timestamps")
    logging.info('Kernel |Kernel hardening added')

def banner():
    with open("/etc/issue.net", "a") as issue:
        issue.write("""###############################################################
    #                                                      Welcome to Meastro's server                                                           # 
    #                                   All connections are monitored and recorded                                         #
    #                          Disconnect IMMEDIATELY if you are not an authorized user!                    #
    ###############################################################""")
    logging.info('issue.net | Add legal banner to /etc/issue.net, to warn unauthorized users [BANN-7130]')
    with open("/etc/issue", "a") as issue:
        issue.write("""###############################################################
    #                                                      Welcome to Meastro's server                                                           # 
    #                                   All connections are monitored and recorded                                         #
    #                          Disconnect IMMEDIATELY if you are not an authorized user!                    #
    ###############################################################""")
    logging.info('issue | Add legal banner to /etc/issue, to warn unauthorized users [BANN-7130]')
    with open("/etc/motd", "a") as motd:
            motd.write("""###############################################################
    #                                                      Welcome to Meastro's server                                                           # 
    #                                   All connections are monitored and recorded                                         #
    #                          Disconnect IMMEDIATELY if you are not an authorized user!                    #
    ###############################################################""")
    logging.info('MOTD | Add a legal banner to /etc/issue, to warn unauthorized users [BANN-7126]')

def tools():
    try:
        os.system('sudo apt-get update -y > /dev/null 2>&1 && sudo apt-get upgrade -y > /dev/null 2>&1 && sudo apt-get dist-upgrade -y >/dev/null 2>&1')
        logging.info('System updated')
    except:
        logging.critical('Could not update!')
    try:
        os.system('sudo apt-get install git')
        logging.info('Git installed')
    except:
        logging.critical('Could not install git!')
    try:
        os.system('sudo apt-get install AIDE -y')
        logging.info('AIDE |Aide is installed! integrety')
    except:
        logging.critical('AIDE | could not install AIDE already installed?')
    try:
        os.system('sudo apt-get install acct -y')
        logging.info('[FINT-4350] |ACCT is installed! integrety')
    except:
        logging.critical('[FINT-4350] | could not install ACCT already installed?')
    try:
        os.system('sudo apt-get install auditd -y')
        logging.info('[ACCT-9628] | Enable auditd to collect audit information ')
    except:
        logging.critical('[ACCT-9628] | Could not install auditd!')
    try:
        os.system('sudo apt-get install rkhunter chkrootkit -y')
        logging.info('[ACCT-9628] | Anti maleware ')
    except:
        logging.critical('[ACCT-9628] | Could not install  Anti maleware!')
    try:
        os.system('sudo apt-get install libpam-cracklib -y')
        logging.info('[AUTH-9262] | Cracklib ')
    except:
        logging.critical('[AUTH-9262] | Could not install Crackliv!')
    try:
        os.system('sudo apt-get install sysstat -y')
        logging.info('[ACCT-9626] | Sysstat accounting data')
    except:
        logging.critical('[ACCT-9626] | Sysstat accounting data not installed!')
    try:
        os.system('sudo apt-get install arpwatch -y')
        logging.info('NETW-3032 |ARP is installed! integrety')
    except:
        logging.critical('NETW-3032 | could not install ARP already installed?')
    try:
        os.system('sudo apt-get install debsums -y')
        logging.info('NETW-3032 |ARP is installed! integrety')
    except:
        logging.critical('NETW-3032 | could not install ARP already installed')


def cleanlog():
    logging.info('Remove temp files')
    try:
        logging.info('Remove temp files')
        os.system(command='sudo rm -r /tmp')
        os.system(command='sudo rm -r /var/tmp')
    except:
        logging.critical('Could not remove temp files')

def lynisupdate():
    os.system("cd /usr/local")
    os.system("sudo git clone https://github.com/CISOfy/lynis.git")

def firewall():
    try:
        os.system("sudo apt-get install ufw")
        logging.info("installed UFW!")
    except:
        logging.info("Ufw already installed!")
    try:
        os.system("sudo ufw allow ssh")
        logging.info("Allowed SSH!")
    except:
        logging.info("SSH already allowed")
    try:
        os.system("sudo ufw enable")
        logging.info("UFW Enabled")
    except:
        logging.info("UFW Already enabled!")

def main():
    logging.info("Welcome to Hardening")
    logging.info("Running on %s version %s" %(platform.system(),platform.release()))
    logging.info("Testing..")
    lynisupdate()
    tools()
    banner()
    hardenssh()
    cleanlog()

if __name__ == "__main__":
    # execute only if run as a script
    user = os.getenv("SUDO_USER")
    if user is None:
        print("This program need 'sudo'")
        exit()
    main()