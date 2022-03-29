from igramscraper.instagram import Instagram
from email.message import EmailMessage
import smtplib
import os

load_dotenv()
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
PASSWORD = os.environ.get("PASSWORD")
PORT_NUMBER = os.environ.get("PORT_NUMBER")
INSTA_USERNAME = os.environ.get("INSTA_USERNAME")
INSTA_PASSWORD = os.environ.get("INSTA_PASSWORD")
USERNAME=os.environ.get("USERNAME")
FOLLOWER_LIMIT = os.environ.get("FOLLOWER_LIMIT")

instagram = Instagram()
instagram.with_credentials(INSTA_USERNAME, INSTA_PASSWORD)
instagram.login(force=False,two_step_verificator=True)

followers = []
account = instagram.get_account(USERNAME)
followers = instagram.get_followers(account.identifier, FOLLOWER_LIMIT)
current_followers = []

for follower in followers['accounts']:
  current_followers.append(follower.USERNAME)

del followers

if os.path.exists('insta_followers_current.txt'):
  print("Exists")
  f = open('insta_followers_current.txt',"r+")
  old_followers = f.read()
  unfollowers = (list(set(old_followers) - set(current_followers)))
  followers = (list(set(current_followers) - set(old_followers)))
  f.close()
  unfollowers_str = ('\n'.join(map(str, unfollowers)))
  if(len(unfollowers_str)>=1):

    # Sending email
    server=smtplib.SMTP('smtp.gmail.com',PORT_NUMBER)
    msg = EmailMessage()
    msg.set_content('You have been unfollowed by : {} Username : {}'.format(len(unfollowers),unfollowers_str))
    msg['Subject'] = 'You have been unfollowed...'
    msg['From'] = SENDER_EMAIL
    msg['To'] =RECEIVER_EMAIL

    server.starttls()
    try:
      server.login(SENDER_EMAIL,PASSWORD)
      print("Login success")
      try:
        server.send_message(msg)
        print("Mail sent")
        time.sleep(1)
        print("Mail sent to : \n",RECEIVER_EMAIL)
        server.quit()
      except:
        print("Failed to sent")
    except:
      print("Login Fail")
  print("Total followers : ",len(followers))
  f = open('insta_followers_current.txt',"r+")
  f.write(str(current_followers))
  f.close()
else:
  f = open('insta_followers_current.txt', 'w')
  f.write(str(current_followers))
  print("Total followers : ",len(current_followers))
  f.close()
