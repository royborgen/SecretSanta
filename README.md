# SecretSanta
SecretSanta reads a list of "Santas" and randomly matches each of the santas with a "child". The script then sends an email to each Santa informing them who their child is. The script is highly customizable, enabling you to easily configure the email content, server settings and sender information through a configuration file. 

## Usage
The script is executed by running drawsanta.py

# secretsanta.conf
This is the scripts configuration file. 
If no configuration file exist, a default one will be created automatically.
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

## stantas.txt
Contains a list names and emails of everyone partisipating in Secret Santa. 
The name of the file can be changed by editing secretsanta.txt and changing the value santaslist under general section. 

Example: 
```
John,john@ourfamilydomain.com
Mary,mary@ourfamilydomain.com
Sarah,sarah@ourfamilydomain.com
Joseph,joseph@ourfamilydomain.com
Mark,mark@ourfamilydomain.com
Jessica,jessica@ourfamilydomain.com
```

## email.txt
This file contains the mail content that will be sent to each of the santas.
Filename and location can be changed by modifying emailcontent in secretsantas.conf

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
%santaNAme% is a placeholder for the name read from santas.txt
%childname% is a placeholder for the name of the child that each santa has to buy a gift for.


## Logging
There is an option to log to file. 
This can be enabled by setting createlogfile = yes in the configuration file secretsanta.conf


## Example output
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
