# appointment-scheduler (wip)
pet project for hospital appointment scheduler

Project works for specialities only: 

create `local_variables.ini` with the following structure

```ini
[variables]
username_dni = 
to_email = xxx@gmail.com
specialty = CARDIOLOGIA
max_days = 7
```

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