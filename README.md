jdwebsite
=======
[![Build Status](https://travis-ci.org/jonge-democraten/website.svg?branch=master)](https://travis-ci.org/jonge-democraten/website) [![Documentation Status](https://readthedocs.org/projects/jdwebsite/badge/?version=latest)](https://readthedocs.org/projects/jdwebsite/?badge=latest) [![Coverage Status](https://coveralls.io/repos/jonge-democraten/website/badge.svg?branch=master)](https://coveralls.io/r/jonge-democraten/website?branch=master) [![Dependency Status](https://gemnasium.com/jonge-democraten/website.svg)](https://gemnasium.com/jonge-democraten/website)  
A website application and content management system developed for the [Jonge Democraten](http://jongedemocraten.nl/).  
Based on Python, Django and [Mezzanine](http://mezzanine.jupo.org/). Open-source and under the MIT-licence. 

#### Documentation
* **[User](http://jdwebsite.readthedocs.org/en/latest/user/)**
* **[Administrator](http://jdwebsite.readthedocs.org/en/latest/administrator/)**
* **[Developer](http://jdwebsite.readthedocs.org/en/latest/developer/)**
* **[Design](http://jdwebsite.readthedocs.org/en/latest/design/)**

#### Quick install
1. `$ ./clean_env.sh`
1. `$ ./build_env.sh`
1. `$ source ./env/bin/activate`  
1. `$ python create_local_settings.py`
1. `$ website/manage.py createdb`
1. `$ website/manage.py loaddata demo_data` *optional, loads demo data (login: admin/admin)*
1. `$ website/manage.py runserver`  
