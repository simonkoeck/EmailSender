import smtplib
from email.mime.text import MIMEText

validserver = [
    {"name": "Gmail", "port": 587, "server": "smtp.gmail.com"},
    {"name" : "Yahoo", "port": 465, "server": "smtp.mail.yahoo.com"},
    {"name": "GMX", "port": 587, "server": "mail.gmx.net"},
    {"name": "Custom SMTP Server"}
]

def main():

    print("""

   ___    __  __      _ _   ___              _         
  | __|__|  \/  |__ _(_) | / __| ___ _ _  __| |___ _ _ 
  | _|___| |\/| / _` | | | \__ \/ -_) ' \/ _` / -_) '_|
  |___|  |_|  |_\__,_|_|_| |___/\___|_||_\__,_\___|_|

        by Simon Koeck - github.com/simonkoeck
    
    """)
    
    i = 1
    for s in validserver:
        print(str(i) + ". " + s["name"])
        i += 1
    try:
        choosen = validserver[int(input(">> ")) - 1]
    except:
        return
    if choosen["name"] == "Custom SMTP Server":
        choosen["server"] = input("Server >> ")
        choosen["port"] = int(input("Port >> "))
    user = input("E-Mail >> ")
    password = input("Password >> ")
    display_name = input("Displayname >> ")
    filename = input("HTML-File-Path >> ")
    subject = input("Subject >> ")
    reciever = input("Reciever (Path to file or E-Mail Address) >> ")
    if reciever.find("@") == -1:
        f = open(reciever, "r+")
        to = f.read().splitlines()
        f.close()
    else:
        to = [reciever]

    f = open(filename, "r+")
    htmlfile = f.read()
    f.close()

    server = smtplib.SMTP(choosen["server"], choosen["port"])
    server.ehlo()
    server.starttls()
    server.login(user, password)

    for email in to:
        try:
            email = email.strip()
            print("Sending email to {}".format(email))
            newmsg = htmlfile
            if htmlfile.find("{name}") > -1:
                name = email.split("@")[0].split(".")[0].capitalize()
                newmsg = htmlfile.replace("{name}", name)
            msg = MIMEText(newmsg, "html")
            msg["Subject"] = subject
            msg["From"] = display_name + " <{}>".format(display_name)
            msg["To"] = email
            server.sendmail(display_name, email, msg.as_string())
            print("Success!")
        except:
            print('Something went wrong...')
            print('If you are using Gmail try allowing \"Less Secure Apps\" - https://myaccount.google.com/lesssecureapps')

    server.close()



if __name__ == "__main__":
    main()
