
# notify-ws

### this project is a minimal jira clone. and focuses of jira's notification system with web sockets.
### The main goal is to have fun, to reinforce the skills on the channels library and to remember the core Django features like templates, generic views etc. (Yes, I have been developing with DRF for a long time as a part of my job.)

<br>

### You can register to the system, log in and create new tasks with assigned users. Afterwards, you can receive instant notifications via the web socket every time the task is updated via the notifier of the task you created, the person who will work on it or the watchers.

<br> <br>
# Setup

## Create an .env file as specified in the .env.example file and then
```
docker-compose up -d 
```
## Simple rigth?
<br>


### Or you can manuel setup. Creating .env file, loading dependencies, starting redis on the relevant port, etc.

```
pip install -r requirements.txt
cd app/
python manage.py migrate
python manage.py runserver 
```
### Visit  [localhost:8000/users/login/](http://localhost:8000/users/login/).


<br>

# Populating random data.
## You can easily generate the necessary data to discover the application with the following command.

```
docker-compose exec web python manage.py random_data -up normal -sp staff -p password123
```

## If you chose manual installation
```
python manage.py random_data -up normal -sp staff -p password123
```

### The -up option provides a username prefix for regular users to be generated. For example, if -up is specified as custom, users will be generated as custom_1, custom_2. 
### -sp allows you to specify a prefix for staff users. -p determines the password that all users will use.

<br> <br>
## Todo list

- [ ] write test (who needs :P)
- [ ] save notifications on the database.
- [ ] better ui.
- [ ] write blog post about channels, and websockets.


### Happy coding!




