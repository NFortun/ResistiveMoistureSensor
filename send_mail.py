import smtplib, ssl, time



def send_email(message):
        port = 587  # For SSL
        smtp_server = "smtp-mail.outlook.com"
        sender_email = "<sender_mail>"  # Enter your address
        receiver_email = "<receiver_mail>"  # Enter receiver address
        password = "<password>"
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            try:
                server.ehlo()
                server.starttls(context=context)
                server.ehlo()
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, "Subject: Alerte bonsai \n\n"+message)
            except Exception as e:
                print("Failed to send mail at "+ time.strftime("%H:%M:%S", time.localtime()))
            finally:
                server.quit()
