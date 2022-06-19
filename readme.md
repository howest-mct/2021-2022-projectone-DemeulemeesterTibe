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

Download the sql file in the folder [database-export](https://github.com/howest-mct/2021-2022-projectone-DemeulemeesterTibe/tree/master/database-export) and run the file in MySQL workbench

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
