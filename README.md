# appointment-scheduler (wip)
Intended to be a monitor for doctor availability. I intend to run this in a cronjob so I get notified whenever a doctor has availability
in the timerange I need.

Original source: https://institutodediagnostico.com.ar/

### Project works only for specialities at the moment

create `local_variables.ini` with the following structure

```ini
[variables]
username_dni = 123456789
to_email = xxx@gmail.com
specialty = CARDIOLOGIA
max_days = 7
```

Create your oauth2 token to authorize your account in order to send emails. paste it as `credentials.json`

run `python3 webscrapper.py`

done:
- authenticate webpage
- navigate and scrap availability
- send_emails
- handle specialty
- handle config files

to be done:
- handle non-availability for the next month
- handle doctor
- handle multiple specialities
- handle multiple doctors
- handle multiple users 
