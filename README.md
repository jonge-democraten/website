jdwebsite
=======
[![Build Status](https://travis-ci.org/jonge-democraten/website.svg?branch=master)](https://travis-ci.org/jonge-democraten/website)  
A website application and content management system in development for the [Jonge Democraten](http://jongedemocraten.nl/).  
Based on Python, Django and [Mezzanine](http://mezzanine.jupo.org/). Open-source and under the MIT-licence. 

The project is in the initial development stage. Nothing is stable and everything may change. 

#### Documentation
[![Documentation Status](https://readthedocs.org/projects/jdwebsite/badge/?version=latest)](https://readthedocs.org/projects/jdwebsite/?badge=latest)  
The [user manual](http://jdwebsite.readthedocs.org/en/latest/user/) and [developers documentation](http://jdwebsite.readthedocs.org/en/latest/developer/) can be found [here](http://jdwebsite.readthedocs.org).  

#### Quick install
1. `$ ./build_env.sh`
1. `$ source ./env/bin/activate`  
1. `$ python create_local_settings.py`
1. `$ python website/manage.py createdb`
1. `$ python website/manage.py loaddata demo_data` #Optional, loads demo data (login: admin/admin)
1. `$ python website/manage.py runserver`  
