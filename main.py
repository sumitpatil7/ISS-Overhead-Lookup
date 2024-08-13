from time import sleep

import requests
from datetime import datetime
import smtplib

MY_LAT = 16.771630  # Your latitude
MY_LONG = 74.025420  # Your longitude


def issoverhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True
    return False


def isdark():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = str(datetime.now())
    current_hour = int(time_now.split(" ")[1].split(":")[0])

    # Handling overnight boundary
    if sunrise < sunset:  # Sunrise and sunset within the same day
        return sunset <= current_hour <= sunrise
    else:  # Sunrise and sunset cross midnight
        return current_hour >= sunset or current_hour < sunrise


def emailsend():
    usern = "Your username"
    passw = "your pass"
    toaddress = "To address"

    try:
        connection = smtplib.SMTP("smtp.gmail.com", 587)  # Use port 587 for Gmail
        connection.starttls()
        connection.login(user=usern, password=passw)
        connection.sendmail(from_addr=usern,
                            to_addrs=toaddress,
                            msg="Subject: ISS Overhead Lookup\n\nPlease look up in the sky! ISS is right above you!")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        connection.quit()


while True:
    sleep(60)
    if issoverhead() and isdark():
        emailsend()
