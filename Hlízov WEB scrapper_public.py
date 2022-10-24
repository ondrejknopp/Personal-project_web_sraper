import requests
from bs4 import BeautifulSoup as bs
import requests
import time
import smtplib
import email
import sys
from datetime import date

from email.mime.text import MIMEText
#from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

def main():
    today = date.today()
    today = today.strftime("%d.%m.%y")
    Hlizov_WebPage = "http://www.obec-hlizov.cz/"
    hlizov_soup = get_soup(Hlizov_WebPage)
    txt_soup = str(hlizov_soup.findAll(text=True))
    #print(hlizov_soup.prettify())
    today_date =  str(today)
    #print(today_date)
    soup_substring_prep= substring_after(txt_soup, "Oznámení ČEZ Distribuce - přerušení dodávky elektřiny")
    input_date = soup_substring_prep[37:45]
    #print(input_date)


    if "přerušení dodávky elektřiny" in txt_soup and today_date == input_date:
        print("Na stránkách obce oznámení o přerušení dodávky elektřiny!")
        # Call the message function
        mail()

    elif "přerušení dodávky elektřiny" in txt_soup and today_date != input_date:
        print("Oznámení o přerušení dodávky elektřiny - neaktuální...")

    else:
        print('Nenašel jsem nic..')

def substring_after(s, delim):
    return s.partition(delim)[2]

def mail():
    # initialize connection to our email server,
    smtp = smtplib.SMTP("smtp.gmail.com", 587)
    smtp.ehlo()
    smtp.starttls()

    # Login with your email and password
    smtp.login("your_email", "password")

    # Call the message function
    msg = message("ČEZ Alert!", "Na stránkách obce oznámení o přerušení dodávky elektřiny!",None, None)

    to = ["receiving_address"]

    # Provide some data to the sendmail function!
    smtp.sendmail(from_addr="sending_address", to_addrs=to, msg=msg.as_string())

    # Finally, don't forget to close the connection
    smtp.quit()

def get_soup(adresa):
    try:
        r = requests.get(adresa)
    except:
        print("Chyba s vlozenim odkazu, zkontrolujte vlozeny odkaz!")
        sys.exit()
    return bs(r.content, "html.parser")


def message(subject="Notification",
            text="", img=None,
            attachment=None):
    # build message contents
    msg = MIMEMultipart()
    msg['Subject'] = subject

    # Add text contents
    msg.attach(MIMEText(text))

    # Check if we have anything given in the img parameter
    if img is not None:

        # Check whether we have the lists of images or not!
        if type(img) is not list:
            # if it isn't a list, make it one
            img = [img]

            # Now iterate through our list
        for one_img in img:
            # read the image binary data
            img_data = open(one_img, 'rb').read()
            # Attach the image data to MIMEMultipart
            # using MIMEImage, we add the given filename use os.basename
            msg.attach(MIMEImage(img_data,
                                 name=os.path.basename(one_img)))

    # We do the same for
    # attachments as we did for images
    if attachment is not None:

        # Check whether we have the
        # lists of attachments or not!
        if type(attachment) is not list:
            # if it isn't a list, make it one
            attachment = [attachment]

        for one_attachment in attachment:
            with open(one_attachment, 'rb') as f:
                # Read in the attachment
                # using MIMEApplication
                file = MIMEApplication(
                    f.read(),
                    name=os.path.basename(one_attachment)
                )
            file['Content-Disposition'] = f'attachment;\
            filename="{os.path.basename(one_attachment)}"'

            # At last, Add the attachment to our message object
            msg.attach(file)
    return msg


if __name__ == "__main__":
    main()