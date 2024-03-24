"""
 # MIT License
 # 
 # Copyright (c) 2024 Rahul Singh
 # 
 # Permission is hereby granted, free of charge, to any person obtaining a copy
 # of this software and associated documentation files (the "Software"), to deal
 # in the Software without restriction, including without limitation the rights
 # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 # copies of the Software, and to permit persons to whom the Software is
 # furnished to do so, subject to the following conditions:
 # 
 # The above copyright notice and this permission notice shall be included in all
 # copies or substantial portions of the Software.
 # 
 # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 # FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 # LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 # SOFTWARE.
 """

#!/usr/bin/env python3
import os
import time
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

fromaddr="lumiraspberry18@gmail.com"
toaddr="rahulks25897@gmail.com"
msg = MIMEMultipart()

msg['From'] = fromaddr
msg['To'] = toaddr
msg['subject'] = "Message from Raspberry pi"

body =""

msg.attach(MIMEText(body, 'plain'))
os.system ("fswebcam -r 680x480 --no-banner /home/pi/image.jpg")


filename = "image.jpg"
attachment = open("/home/pi/image.jpg", "rb")
part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename=%s" % filename)
msg.attach(part)
server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login(fromaddr, "raspberry18")
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
print "Your Message has been sent successfully"

