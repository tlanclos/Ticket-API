## Install base system packages

```
apt-get install finger
apt-get install apache2
apt-get install apache2-dev
apt-get install python3
apt-get install python3-pip
apt-get install python3-dev
apt-get install freetds-bin
apt-get install freetds-common
apt-get install freetds-dev
apt-get install libjpeg-dev
apt-get install libpng3
apt-get install libpng-dev
apt-get install libz-dev
apt-get install htop
```

## Install python libraries

```
pip3 install flask
pip3 install flask-restful
pip3 install pymssql
pip3 install sqlalchemy
pip3 install addict
pip3 install Pillow
pip3 install mod_wsgi
```

## Setup mod_wsgi
Run this command
```
mod_wsgi-express install-module
```
The previous command will return two lines, one with a "LoadModule" and the other with a "WSGIPythonHome". Modify the following statements accordingly to the two lines. They will be in the format of `echo "..." > file`. For the first, replace "..." with the "LoadModule" line, for the second, replace "..." with the "WSGIPythonHome" line.
```
echo "..." > /etc/apache2/mods-available/wsgi_express.load
echo "..." > /etc/apache2/mods-available/wsgi_express.conf
```
For example:
```
echo "LoadModule wsgi_module /usr/lib/apache2/modules/mod_wsgi-py34.cpython-34m.so" > /etc/apache2/mods-available/wsgi_express.load
echo "WSGIPythonHome /usr" > /etc/apache2/mods-available/wsgi_express.conf
```
The run this command
```
a2enmod wsgi_express
```


## Remove the default apache html file
```
rm /var/www/html/index.html
```

## Add the service user
```
useradd -g www-data -M -s /usr/sbin/nologin ticket-api
passwd ticket-api
```

## Run the make install at the root of the github repo Ticket-API
```
make
make install
```
