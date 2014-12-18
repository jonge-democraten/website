website
=======
[![Build Status](https://travis-ci.org/jonge-democraten/website.svg?branch=master)](https://travis-ci.org/jonge-democraten/website)

JD website

### Work environment
 * **Build a new work environment:** `$ ./build_env.sh`
 * **Remove the current work env:** `$ ./clean_env.sh`
 * **Generate local settings:** `$ python3 create_local_settings.py`
 * **Activate work env:** `$ source ./env/bin/activate`
 * **Create a database:** `(env) $ python3 website/manage.py createdb`
 * **Run the test server:** `(env) $ python3 website/manage.py runserver`
 
### Testing 
All application logic code has to be unit tested. Unit tests are ideally created before development of functionality. Feature branches are only merged if unit tests are written and all pass. 

Higher level user interface actions are tested manually. 

##### Unit tests
The project uses the [Django unit test](https://docs.djangoproject.com/en/dev/topics/testing/overview/) framework to create unit tests. 
This framework is based on the python unittest module. 

Tests are defined in the `tests.py` file of the application directory. 

##### Run tests
Tests for the project's Django applications can be run with the following command, 

`(env) $ python website/manage.py test <appname>`

##### Automated testing
[Travis](https://travis-ci.org/jonge-democraten/website) is used to automatically install the environment and run tests on changes in the project. 

The file `.travis.yml` contains the Travis commands to install and test the project.

The build indicator on top of this document shows the status of the last automated install and tests.
