# vetletemplate
My personal Django/bootstrap for Heroku ready-to-go out-of-the-box repo

# Get the repo up and running
- on github make a new repo with vetletemplate as template. Give it the desired name.
- mkvirtualenv desired_name (or workon existing_venv - not reccomended)
- git clone https://github.com/vetleen/newrepo.git (where newrepo is the name of the new repo you just made)
- pip install -r requirements.txt (should have python installed)
- python manage.py makemigrations (should give no changes messages)
- python manage.py migrate
- python mange.py collectstatic (so we can run tests)
- python manage.py test (should not fail)
- python manage.py runserver
- open http://127.0.0.1:8000/ in browser and it should work






