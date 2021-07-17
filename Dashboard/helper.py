from django.core.mail import send_mail
from django.conf import settings
import re
import json
from urllib.request import urlopen
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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

def get_chart(values, save_path):

    print (values)

    labels = ["Missing", "Found"]

    # Create subplots: use 'domain' type for Pie subplot
    fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]])
    fig.add_trace(go.Pie(labels=labels, values=values, name="Missing Stats"),
                  1, 1)

    # Use `hole` to create a donut-like pie chart
    fig.update_traces(hole=.9, hoverinfo="label+percent+name")

    fig.update_layout(
        title_text="Misingly Statistic",
        # Add annotations in the center of the donut pies.
        annotations=[dict(text='Stats', x=0.19, y=0.5, font_size=20, showarrow=False),
                     ])
    ##fig.show()

    fig.write_image(save_path)