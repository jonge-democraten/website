<h1>Developer manual</h1>
This page contains information for jdwebsite developers.  
Please improve me!

## Installation
Installation is easy on a Linux-like operating system.  
For Windows and Mac, we advise to create a Linux virtual machine. Instructions are given below.

<h3>Basics</h3>
    $ ./build_env.sh
    $ source ./env/bin/activate
    $ python create_local_settings.py
    $ python website/manage.py createdb
    $ python website/manage.py loaddata demo_data #Optional, creates admin/admin
    $ python website/manage.py runserver

<h3>Requirements</h3>
**Linux**  
Installation of the full project, and running a test server, can be done in a few minutes on any Linux machine. Just follow the steps under 'detailed instructions'. There is no need for manual configuration.

**Windows and Mac**  
For Windows and Mac users, it is advised to install a Linux virtual machine and use this to install the project.

* Follow the [instructions](http://www.wikihow.com/Install-Ubuntu-on-VirtualBox) and install Ubuntu on VirtualBox.
* Start Ubuntu in a VirtualBox, open the program called "Terminal" and install some required applications by entering the command,

        $ sudo apt-get install git python-virtualenv python3-dev

<h3>Detailed instructions</h3>
**Get the code**  
Create a new clone of the project,

    $ git clone https://github.com/jonge-democraten/website.git

**Virtual environment**  
Create a virtual environment in `./env/` and install all dependencies,

    $ ./build_env.sh  

Activate the virtual environment,

    $ source ./env/bin/activate   

From now on, everything you do within the project should be from a shell with activated virtual environment.

**Configure Django settings**  
Generate a Django `SECRET_KEY` and a `local_settings.py`,

    (env) $ python create_local_settings.py  

**Create a database**  
You have to create an initial database and a root user and password for the database,

    (env) $ python website/manage.py createdb

**Run a test server**  
You can run a local test server with the command,

    (env) $ python website/manage.py runserver

and visit [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser to view the web interface.

<h3>Update and clean</h3>
**Get the latest changes**  
To get the latest version of the project, type the following git command in your project directory,
    
    (env) $ git pull

Migrate possible database changes with,

    (env) $ python website/manage.py migrate

**Clean project**  
You can remove the virtual environment and database with,

    $ ./clean_env.sh

-----
## Workflow
* New features are developed on a separate feature branch.
* The feature branch is merged with master if the feature is finished. 
* This allows to work independently on different features and still share code. 
* Push feature branch commits often to communicate what you are working on.
* Read more about this workflow [here](https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow).


-----
## Testing
All application logic code is to be unit tested. Unit tests are ideally created before development of functionality.
It supports development and documents, in real code instead of text, what classes and functions are supposed to do.
Feature branches are only merged if unit tests are written and all pass.  
Higher level user interface actions are tested manually. 

<h3>Unit tests</h3>
* The project uses the [Django unit test](https://docs.djangoproject.com/en/dev/topics/testing/overview/) framework to create unit tests. 
* This framework is based on the Python unittest module.  
* Tests are defined in `tests.py` of the application directory. 

Run the unit tests,

    (env) $ python website/manage.py test <app_label>
 
<h3>Automated testing</h3>
[Travis](https://travis-ci.org/jonge-democraten/website) is used to automatically install the environment and run tests on changes in the project.  
The file `.travis.yml` contains the Travis commands to install and test the project.

-----
## Logging
The Python logging module is used for logging. Add and commit plenty of useful log statements. This support effective debugging. 

<h3>Example</h3>
To add log statements, simply add the following at the top of your Python file,
```python
import logging
logger = logging.getLogger(__name__)
```
and add a new log statement anywhere in this file by,
```python
logger.debug('debug log statement')
logger.warning('warning message')
logger.error('error message')
```
<h3>Output</h3>
The log statements include log level, application, class, function and line number of the log statement,

    [2014-12-19 22:39:11] ERROR [website.tests::test_logfile() (23)]: Cannot find anything here.

Five log levels are available: `debug(), info(), warning(), error()` and `critical()`.

The log statements for the applications are written to the console, if `DEBUG=True`, and always to `debug.log` and `error.log`. Django errors can be found in `django.log`.

<h3>Configuration</h3>
Logging is configured in the Django `settings.py` `LOGGING` variables. Information about configuration can be found [here](https://docs.djangoproject.com/en/1.7/topics/logging/). New applications have to be added before logging becomes active for those applications. 

<h3>Confidential information</h3>
Confidential information should not be logged. During initial development, logging of confidential information is allowed if marked with a `CONF` tag,
```python 
logger.debug('CONF ' + member.DNA)
```
These will be removed before deployment.  

-----
## Code standards
 * The default Python and Django [code style](https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/) is used.  
 * Write code as simple as possible and focus on readability. 
 * Write code for others to understand and read.

*"Always code as if the person who ends up maintaining your code is a violent psychopath who knows where you live. "* - [source](http://c2.com/cgi/wiki?CodeForTheMaintainer)

<h3>Code check</h3>
* Flake8 is a Python tool to check code style. 
* It runs automatically on Travis after each commit.
* You can find the Flake8 output in the [latest Travis build log](https://travis-ci.org/jonge-democraten/website).

-----
## Code documentation
* Add comments to code that is not self-explanatory.
* Use [python docstrings](http://en.wikipedia.org/wiki/Docstring#Python) to describe files, classes and functions.
* Add docstrings to files, classes and functions if useful.

<h3>Example</h3>
```python
"""
File description.
"""

class ExampleClass(Example):
    """ Class description. """

    def example_function(self):
        """
        Function description 
        on multiple lines.
        """
```

-----
## Database

<h3>Introduction</h3>

<h3>Migrations</h3>
A [database migration](https://docs.djangoproject.com/en/1.7/topics/migrations/) needs to be created after database structure changes in `models.py`,

    $ python website/manage.py makemigrations <app_label>  
    
The generated migration file is committed together with changes in `models.py`.  
Migrations have to be carefully managed between different branches, so keep track of other branches and prepare for a merge.

-----
## Demo data

The code base of jdwebsite contains demo data to demonstrate functionality. To create demo data, dump a fixture. 

```
python3 website/manage.py dumpdata --all --natural --indent 2 forms pages sites blog auth.User > website/fixtures/demo_data.json
```

This fixture may be loaded when initialising the development environment (see [Installation](#Installation)).

<h3>Caveat</h3>

For some reason, the categories of blog posts in Blogs on non-default Sites are not exported correctly. To include this information, you have to add it by hand.
