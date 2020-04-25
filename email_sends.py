import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def registrationEmail(emailAddress):
    return True


def sendStockReminder(priceMessage):
    port = 465
    smtp_server = "smtp.gmail.com"
    sender_email = "saitest101@gmail.com"
    receiver_email = "080sai@gmail.com"
    password = "saitest101adobe"
    '''rec = []
    for var in receiver_email:
        rec.append(var.encode('utf-8'))

    print(rec)
    '''
    print(receiver_email)
    # print(type(receiver_email))
    message = MIMEMultipart("alternative")
    message["Subject"] = "Stock Price Alert"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = """\
	Hi User,
	This is your stock price alert!
	""" + priceMessage + """
	"""
    html = """\
	<html>
	  <body>
	    <p>Hi User,<br/><br/>
	      This is your stock price alert!<br>
	     """ + priceMessage + """ <br/> <br/>
	       Regards, <br>
	       Your humble script.
	    </p>
	  </body>
	</html>
	"""

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )
        # Create a secure SSL context
