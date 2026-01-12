 Running this project

To get this project up and running you should start by having Python installed on your computer. It's advised you create a virtual environment to store your projects dependencies separately. You can install virtualenv with

```
pip install virtual env  
```

Clone or download this repository and open it in your editor of choice. In a terminal (mac/linux) or windows terminal, run the following command in the base directory of this project

```
virtual env env
```

That will create a new folder `env` in your project directory. Next activate it with this command on mac/linux:

```
source env/bin/active
```

Then install the project dependencies with

```
pip install -r requirements.txt

Then make migrations

python manage.py makemigrations

python manage.py migrate
```

Now you can run the project with this command

```
python manage.py runserver
```

**Note** if you want payments to work you will need to enter your own Stripe API keys into the `.env` file in the settings files.

---

## Follow the tutorial

This project is part of a [series on YouTube](https://youtu.be/z4USlooVXG0) that teaches how to build an e-commerce website with Django.

---

## Support

If you'd like to support this project and all the other open source work on this organization, you can use the following options

