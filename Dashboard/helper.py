from django.core.mail import send_mail
from django.conf import settings
import re
import json
from urllib.request import urlopen


def get_person_location():
    url = 'http://ipinfo.io/json'
    response = urlopen(url)
    data = json.load(response)
    ip = data['ip']
    org = data['org']
    city = data['city']
    country = data['country']
    region = data['region']
    person_location = '\nIP :- {4} \nOrg :- {0} \nCity :- {3} \nRegion :- {1} \nCountry :- {2} '.format(org, region,
                                                                                                      country, city, ip)
    print(person_location)
    return person_location


def send_notification(guardian_email):
    subject = "Person Located!!!"
    person_location = get_person_location()
    message = "The Missing Person Geo Location Information: \n " + person_location

    from_email = settings.EMAIL_HOST_USER
    password = settings.EMAIL_HOST_PASSWORD

    recipient_list = [guardian_email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False, auth_user=None, auth_password=password,
              connection=None, html_message=None)
