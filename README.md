To run project:
`docker compose up`




HOW TO DEVELOP:

AT FIRST ACTIVATE CREATE AND ACTIVATE ENV:
    CREATION:
        python3 -m venv env
    ACTIVATION:
        source env/bin/activate

AFTER EVERY CHANGE (EXCEPT TEMPLATES):
    sudo service apache2 restart

AFTER EVERY CHANGE TO STATIC FILES:
    python manage.py collectstatic
