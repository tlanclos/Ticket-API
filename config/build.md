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
apt-get install unixodbc
apt-get install unixodbc-dev
apt-get install tdsodbc
```

## Install python libraries

```
pip3 install flask
pip3 install flask-restful
pip3 install flask-sqlalchemy
pip3 install pymssql
pip3 install sqlalchemy
pip3 install addict
pip3 install Pillow
pip3 install mod_wsgi
pip3 install validate_email
pip3 install phonenumbers
pip3 install pyodbc
pip3 install scrypt
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

## Setup apache SSL
Run this command
```
a2enmod ssl
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

## Install SSL certificates
Please ensure you install SSL certificates in the following locations with the following permissions and names.
- Certificate:
  - Location: /etc/ssl/certs/techneauxcmps.crt
  - Mode: 0644
  - Owner: root
  - Group: root
- Private Key:
  - Location: /etc/ssl/private/techneauxcmps.key
  - Mode: 640
  - Owner: root
  - Group: ssl-cert

## Setup libtdsodbc.so as a driver for unixodbc
```
# Update our search index for mlocate
updatedb

# This will return the path to libtdsodbc.so, it is
# important to know this path for the following step
# When I ran the search, the path I received was:
# /usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so
locate libtdsodbc.so

# This one is also important
# /usr/lib/x86_64-linux-gnu/odbc/libtdsS.so
locate libtdsS.so
```

- Next, using the path located above, place the following in `/etc/odbcinst.ini`
```
[FreeTDS]
Driver = /usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so
Setup = /usr/lib/x86_64-linux-gnu/odbc/libtdsS.so
Threading = 1
```

- Next, Copy place the following in `/etc/odbc.ini`
```
[SQLServer]
Driver        = FreeTDS
Server        = place.server.name.here
Database      = DatabaseName
Port          = 1433
TDS_Version   = 7.1
```

- Last, make the lib noted above executable (for some reason it is not by default)
```
chmod a+x /usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so
```

- You can test the connection via where `user` is the username and `place` is the first part of server
```
osql -S SQLServer -U user@place -P password
```

## Run the make install at the root of the github repo Ticket-API
```
make
make install
```
