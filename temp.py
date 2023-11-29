import requests
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# List of URLs to monitor
urls = [
    "https://www.jcrew.com/sale/men?crawl=no&trending=newToSale",
    "https://www.jcrew.com/plp/mens/features/wallace-and-barnes"
]

# Set the interval (in seconds) to wait before checking the websites again
interval = 900  # 15 minutes

# Set up email parameters
sender_email = ""
sender_password = ""
receiver_email = ""

def send_email(subject, body):
    # Set up the message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # Log in to the email server and send the message
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, sender_password)
    text = message.as_string()
    server.sendmail(sender_email, receiver_email, text)
    server.quit()

# Get the initial content of each website and store in a dictionary
initial_page_contents = {url: requests.get(url).content for url in urls}

while True:
    # Wait for the specified interval
    time.sleep(interval)

    # Check each website in the list
    for url in urls:
        # Make a new request to the website
        response = requests.get(url)
        current_page_content = response.content

        # Check if the current page content is different from the initial page content
        if current_page_content != initial_page_contents[url]:
            # If there is a difference, send an email notification
            send_email("Change Detected on Website", f"A change was detected on the website: {url}")

            # Update the initial page content to the current page content
            initial_page_contents[url] = current_page_content
