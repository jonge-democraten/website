jdwebsite
=======
[![Build Status](https://travis-ci.org/jonge-democraten/website.svg?branch=master)](https://travis-ci.org/jonge-democraten/website) [![Documentation Status](https://readthedocs.org/projects/jdwebsite/badge/?version=latest)](https://readthedocs.org/projects/jdwebsite/?badge=latest) [![Coverage Status](https://coveralls.io/repos/jonge-democraten/website/badge.svg?branch=master)](https://coveralls.io/r/jonge-democraten/website?branch=master)  
A website application and content management system in development for the [Jonge Democraten](http://jongedemocraten.nl/).  
Based on Python, Django and [Mezzanine](http://mezzanine.jupo.org/). Open-source and under the MIT-licence. 

#### Documentation
* **[User manual](http://jdwebsite.readthedocs.org/en/latest/user/)**
* **[Developer manual](http://jdwebsite.readthedocs.org/en/latest/developer/)**

#### Quick install
1. `$ ./clean_env.sh`
1. `$ ./build_env.sh`
1. `$ source ./env/bin/activate`  
1. `$ python create_local_settings.py`
1. `$ website/manage.py createdb`
1. `$ website/manage.py loaddata demo_data` #Optional, loads demo data (login: admin/admin)
1. `$ website/manage.py runserver`  
