# SecretSanta
SecretSanta reads a list of Santas(names and corresponding e-mails) and randomly matches each of the names with one of the other Santas on the list (a child). The script then sends an e-mail to each santa informing them who their child is. The script is highly customizable, enabling you to easily configure the email content, server settings and sender information through a configuration file. 

## Usage
The script is executed by running drawsanta.py

# secretsanta.conf
This is the scripts configuration file. 
If no configuration file exists, a default one will be created automatically.
The file contains general, mailserver, email and logging settings. 

```
[general]
santaslist = santas.txt

[mailserver]
server = your.mailserver.com
ssl = yes
starttls = yes
port = 587
requireauth = yes
promptforauth = yes
username = 
password = 

[email]
fromname = Santas little helper
fromemail = secretsanta@yourdomain.com
subject = Secret Santa
emailcontent = email.txt

[logging]
createlogfile = yes
logfile = santas.log
logtimeformat = %%d-%%m-%%Y %%H:%%M:%%S
```
username and password can be empty if **promptforauth = yes**

## stantas.txt
Contains a list names and emails of everyone participating in Secret Santa. 
The name of the file can be changed by editing **secretsanta.conf** and changing the value of **santaslist** under the general section. 

Example 
stantas.txt uses the following format
```
John,john@ourfamilydomain.com
Mary,mary@ourfamilydomain.com
Sarah,sarah@ourfamilydomain.com
Joseph,joseph@ourfamilydomain.com
Mark,mark@ourfamilydomain.com
Jessica,jessica@ourfamilydomain.com
```

## email.txt
This file contains the mail content that will be sent to each of the Santa's.
Filename and location can be changed by modifying **emailcontent** in **secretsantas.conf**

Default email.txt: 

```
HO HO HO!
Marry Christmas %santaName%!

This years family secret santa has been picked and you are santa for %childName%.
Please try not to overspend and keep within the agreed amount of 200 kr. 

Hope you have a fantastic Christmas.

Yours truly,
Santas little helper
```
**%santaNAme%** is a placeholder for the name read from santas.txt
**%childname%** is a placeholder for the name of the child that each Santa has to buy a gift for.


## Logging
There is an option to log to file. By default the script logs to santas.log in the same folder as the script is located. 
Logging can be disabled by setting **createlogfile = no** in **secretsanta.conf**. 
Name and location of the configuration file can be changed by changing the values of **logfile** in **secretsanta.conf** 


## Example of script output
When running the script each Stantas child is cencored in the output. 
```
Sending mail...
John <john@ourfamilydomain.com> --> **********
Mary <mary@ourfamilydomain.com> --> **********
Sarah <sarah@ourfamilydomain.com> --> **********
Joseph <joseph@ourfamilydomain.com> --> **********
Mark <mark@ourfamilydomain.com> --> **********
Jessica <jessica@ourfamilydomain.com> --> **********
Done!
6 mails sent
```
setting **createlogfile = yes** in **secretsanta.conf** will log the uncensored output to file. 


## resend.py
Resends Secret Santa e-mail to one or all santas in last drawing. 
```
Usage: resend [santa]...[OPTION]

    -a. --all       Resends mail to all stanas in last drawing
    -v, --version   Outputs version information and exits
        --help      Displays this help text

Example:
resend john         Resends email to john based on entry in logfile
resend --all        Resends email to all santas in last drawing
```

## Requirements
- Python 3 
- Requests library installed 
- sys library installed 
- random library installed
- getpass library installed
- datetime library installed
- smtplib library installed
- configparser library installed
- os library installed
- re library installed
- EmailMessage library installed
- datetime library installed
