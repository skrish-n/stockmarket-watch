#!/usr/bin/env python
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt)

import requests
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from run import dbConnection


def getStockQuote(symbol):
    quoteUrl = "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=" + symbol + "&apikey=TPTE05D3FRVY8IR6"
    r = requests.get(quoteUrl)

    if (r.status_code != 200):
        return None
    data = r.json()
    price = float(data['Global Quote']['05. price'])
    print(data['Global Quote']['05. price'])
    return price


def sendEmail(priceMessage):
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


def main():
    # get the stock quote of company:
    symbols = ["ADBE", "HAVELLS.NS", "CUB.NS", "NELCO.NS"]
    alertPrice = [350, 610, 215, 230]
    for i in range(len(symbols)):
        price = getStockQuote(symbols[i])

        if price > alertPrice[i]:
            print("My stock is above my safe price. Exiting now..")
        else:
            print("Stock is below safe price. Alert!")
            # Try to send email
            message = " The " + symbols[i] + " stock price:" + str(price)
            sendEmail(message)

            # Main Logic

    quit()


@jwt_required
def add_stock_details(json_data, user_name):
    fetch_result = dbConnection.find_one({'username': user_name})
    if fetch_result is None:
        return False
    try:
        dbConnection.update({'username': user_name}, {'$push': {'stockDetails':json_data}})
        return True
    except:
        return False
