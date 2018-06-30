jdwebsite
=======
[![Build Status](https://travis-ci.org/jonge-democraten/website.svg?branch=master)](https://travis-ci.org/jonge-democraten/website) [![Documentation Status](https://readthedocs.org/projects/jdwebsite/badge/?version=latest)](https://readthedocs.org/projects/jdwebsite/?badge=latest) [![Coverage Status](https://coveralls.io/repos/jonge-democraten/website/badge.svg?branch=master)](https://coveralls.io/r/jonge-democraten/website?branch=master) 
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/jonge-democraten/website/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/jonge-democraten/website/?branch=master)  
A website application and content management system developed for the [Jonge Democraten](http://jongedemocraten.nl/).  
Based on Python 3.4+, Django and [Mezzanine](http://mezzanine.jupo.org/). Open-source and under the MIT-licence. 

#### Documentation
* **[User](http://jdwebsite.readthedocs.org/en/latest/user/)**
* **[Administrator](http://jdwebsite.readthedocs.org/en/latest/administrator/)**
* **[Developer](http://jdwebsite.readthedocs.org/en/latest/developer/)**
* **[Design](http://jdwebsite.readthedocs.org/en/latest/design/)**

#### Quick Install (Linux)
Detailed instructions can be found in the [developer documentation](http://jdwebsite.readthedocs.org/en/latest/developer/).

1. `$ ./clean_env.sh`
1. `$ ./build_env.sh`
1. `$ source ./env/bin/activate`  
1. `$ python create_local_settings.py`
1. `$ website/manage.py createdb`
1. `$ website/manage.py loaddata demo_data` *optional, loads demo data (login: admin/admin)*
1. `$ website/manage.py runserver`  

[Windows installation instructions](http://jdwebsite.readthedocs.io/en/latest/developer/#windows) (development only)
