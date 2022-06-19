# Project One - Smart Wekker

## About this project

I created a smart alarm clock that you can't turn off normally. You have to stand on top of the weightsensor for 3 seconds and then the alarm will go off.
In this project there are some sensors and actuators.

- Weight Sensor
- Licht Sensor
- Joystick
- RGB Ring
- LCD Display

## Database

To import the database onto your raspberry pi you firstly have to make a `ssh connection` using `TCP/IP` over `SSH` using `MYSQL Workbench`
Then you have to fill in the correct values

- SSH Hostname: (IP address)
- SSH Username: (User of the Pi)
- SSH Password: (Password of Pi)
- MYSQL Hostname: 127.0.0.1
- MySQL Server Port: 3306
- Username: (User of the Pi)
- Password: (Password of Pi)

Download the sql file in the folder [database-export](https://github.com/howest-mct/2021-2022-projectone-DemeulemeesterTibe/tree/master/database-export) and run the file in the remote MySQL workbench session

## Backend

Before you can run app.py you first have to download some libraries and some packages
This can be done using these commands

```
pip install rpi_ws281x adafruit-circuitpython-neopixel
pip install 'git+https://github.com/bytedisciple/HX711.git#egg=HX711&subdirectory=HX711_Python3'
pip install flask-cors
pip install flask-socketio
pip install mysql-connector-python
pip install gevent
pip install gevent-websocket
```

Now that you have all the libraries and all the packages we will make sure that the code will automatically run on startup
You can do that by following these steps:

1. First we will create a file by running this command:

   ```
   nano mijnproject.service
   ```

2. Now that we have created a file and are in the editor you can copy this into the file:
   ```
    [Unit]
    Description=ProjectOne Project
    After=network.target
    [Service]
    ExecStart=/usr/bin/python3 -u /home/student/2021-2022-projectone-DemeulemeesterTibe/backend/app.py
    WorkingDirectory=/home/student/2021-2022-projectone-DemeulemeesterTibe/backend
    StandardOutput=inherit
    StandardError=inherit
    Restart=always
    User=root
    [Install]
    WantedBy=multi-user.target
   ```
3. Now that you have copied the text into the file you can save the changes by pressing these shortcuts:
   `Ctrl + X` then `Y` and `Enter`
4. After that you have to copy the file to another path with this command:
   ```
    sudo cp mijnproject.service /etc/systemd/system/mijnproject.service
   ```
5. finally we will make sure that the service runs on bootup byy running this command:
   ```
   sudo systemctl enable mijnproject.service
   ```
6. (Optional) If you want to disable this service you can do that with this command:
   ```
   sudo systemctl disable mijnproject.service
   ```

## Frontend

When you have copied the content of the Github Content you have to change the the html file of the apache server.
You can change that by following these commands:

```
sudo nano /etc/apache2/sites-available/000-default.conf
```

Then change `DocumentRoot /var/www/html`
To.
`DocumentRoot /home/student/2021-2022-projectone-DemeulemeesterTibe/front-end`

After that save it by clicking `Ctrl + X` and then clicken `Y` and `Enter`

Now we have to change the right of the root folder
We will change that by doing these steps:

```
sudo nano /etc/apache2/apache2.conf
```

Then change

```
<Directory />
    Options FollowSymLinks
    AllowOverride All
    Require all denied
</Directory>

```

To

```
<Directory />
    Options Indexes FollowSymLinks Includes ExecCGI
    AllowOverride All
    Require all granted
</Directory>

```

After that save it by clicking `Ctrl + X` and then clicken `Y` and `Enter`
Now we have to restart the Apache service by running this command:

```
sudo service apache2 restart
```

Hoe kan een externe persoon (die niets weet over de "ProjectOne" opdracht) het project snel runnen op de eigen pc?
Op github vind je verschillende voorbeelden hoe je een readme.md bestand kan structureren.

- [Voorbeeld 1](https://github.com/othneildrew/Best-README-Template)
- [Voorbeeld 2](https://github.com/tsungtwu/flask-example/blob/master/README.md)
- [Voorbeeld 3](https://github.com/twbs/bootstrap/blob/main/README.md)
- [Voorbeeld 4](https://www.makeareadme.com/)

## Inhoud

Zoals je kan zien is er geen "vaste" structuur voor zo'n document. Je bepaalt zelf hoe je het bestand via markdown structureert. Zorg ervoor dat het document minimaal op volgende vragen een antwoord biedt.

- Wat is de structuur van het project?
- Wat moet er gebeuren met de database? Hoe krijgt de persoon dit up and running?
- Moeten er settings worden veranderd in de backend code voor de database?
- Runt de back- en front-end code direct? Of moeten er nog commando's worden ingegeven?
- Zijn er poorten die extra aandacht vereisen in de back- en/of front-end code?

## Instructables

Plaats zeker een link naar de Instructables zodat het project kan nagebouwd worden!
