#!/usr/bin/python3
import os.path
import drawsanta
import sys

#a function that checks commandline arguments and displays help
def checkarg(arg):
    version = "Secret Santa Resend 1.0"
    helptxt = """Usage: resend [OPTION]... [SANTA]...
    Resends Secret Santa e-mail to one or all santas.

    -a. --all       Resends mail to all stanas in last drawing
    -v, --version   Outputs version information and exits
        --help      Displays this help text

Example:
resend john         Resends email to john based on entry in logfile
resend --all        Resends email to all santas in last drawing"""

    usage="""Usage: resend [Option]... [SANTA]...
Try 'resend --help' for more information."""

    if len(arg)==2:
        if str.startswith(str(arg[1]), "--") == True or str.startswith(str(arg[1]), "-") == True:
            if str(arg[1]) =="--help":
                print(helptxt)
                return False
            elif str(arg[1]) =="-v" or str(arg[1]) =="--version":
                print(version)
                return False
            elif str(arg[1]) =="-a" or str(arg[1]) =="--all":
                return "-a"
            else:
                print(usage)
                return False
        return True
    else:
        print(usage)
        return False


def readlog(logfile):
    if os.path.isfile(logfile):
        with open(logfile, 'r' ) as f:
            content = f.readlines()

    return content



def main():
    argument = checkarg(sys.argv)
    if argument == True or argument == "-a":
        configfile = "secretsanta.conf"
        if drawsanta.checkConfig(configfile):
            #fetching data from config file
            config = drawsanta.configparser.ConfigParser()
            config.read(configfile)
            logfile = config["logging"]["logfile"]
            mailserver = config["mailserver"]["server"]
            promptForAuth = config["mailserver"]["promptForAuth"]
            requireAuth = config["mailserver"]["requireAuth"]

            logfile = readlog(logfile)

            #getting date of last drawing for comparison
            lastdrawing = logfile[-1].split(" ")
            lastdrawing = lastdrawing[0]


            username =""
            password =""

            #Requesting username and password for mailserver
            if promptForAuth == "yes":
                print("Your need to authenticate with " + mailserver)
                username = input("Username: ")
                password = drawsanta.getpass.getpass("Password: ")

            if requireAuth == "yes" and promptForAuth == "no":
                username = config["mailserver"]["username"]
                password = config["mailserver"]["password"]


            print("Sending mail...")

            i=0

            for line in reversed(logfile):
                line = line.split(" ")
                santaName = line[3]
                santaEmail = line[4].strip("<")
                santaEmail = santaEmail.strip(">")
                child = line[6].strip()

                if line[3].lower() == sys.argv[1].lower():
                    print(santaName + " <"+santaEmail + "> --> " + "**********")

                    if drawsanta.sendmail(santaName, santaEmail, child, username, password):
                        print("Done!")
                    #exits the loop as match was found
                    break

                if sys.argv[1] == "--all":
                    logDate = line[0]
                    if logDate == lastdrawing:
                        i+=1
                        print(santaName + " <"+santaEmail + "> --> " + "**********")

                        if drawsanta.sendmail(santaName, santaEmail, child, username, password):
                            failed = False
                        else:
                            failed = True
                            break
                    else:
                        if not failed:
                            print("Done!")
                            print(str(i) + " mails sent")

                        break




               # datetime = line[:19]
               # print (datetime)


               # print(line[santa:30])


#calling main function
if __name__ == "__main__":
        main()
