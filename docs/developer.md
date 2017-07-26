<h1>Developer manual</h1>
This page contains information for jdwebsite developers.

## Installation
Installation is easy on a Linux-like operating system.  
For Windows and Mac, it requires some manual changes or a Linux virtual machine. Instructions are given below.

### Quick Install (Linux)

    $ ./clean_env.sh
    $ ./build_env.sh
    $ source ./env/bin/activate
    $ python create_local_settings.py
    $ python website/manage.py createdb
    $ python website/manage.py loaddata demo_data #Optional, creates admin/admin
    $ python website/manage.py runserver

### Linux 

Installation of the full project, and running a test server, can be done in a few minutes on any Linux machine. Just follow the steps under 'detailed instructions'. There is no need for manual configuration.

**System-Level Dependencies**  
Depending on your Linux distribution, you may need to install some system-level development packages. A list of these dependencies for Ubuntu (15.04) is given below,

*python-virtualenv, python3-dev, libldap2-dev, libsasl2-dev, libxml2-dev, libxslt1-dev, zlib1g-dev, libjpeg-dev, libfreetype6-dev*

Install these using the command,

    $ sudo apt-get install python-virtualenv python3-dev libldap2-dev libsasl2-dev libxml2-dev libxslt1-dev zlib1g-dev libjpeg-dev libfreetype6-dev

**Get the code**  
Create a new clone of the project,

    $ git clone https://github.com/jonge-democraten/website.git

**Virtual environment**  
Delete an existing virtual environment,

    $ ./clean_env.sh

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

### Hostnames
Add the following line to your `/etc/hosts` file to enable the subdomains,

    127.0.0.1 jd.local lh.jd.local ams.jd.local


### Windows

#### Option 1: Native
Install [Python 3](https://www.python.org/downloads/) and [Git](https://git-scm.com/download/win).  
Get the code. Open a Windows command prompt and clone the website repo,
```
git clone https://github.com/jonge-democraten/website.git
```
Enter the `website` directory, create a virtualenv, activate it, and upgrade pip,
```
python -m venv env
env\Scripts\activate.bat
python -m pip install -U pip
```
Download the pyldap Python wheel for your Python version from http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyldap.  
Install this wheel,
```
pip install pyldap-<some specific version info here>.whl
```
Install other requirements,
```
pip install -r requirements.txt
```
Edit `env\Lib\site-packages\rq\worker.py` and replace `def kill_horse(self, sig=signal.SIGKILL):`
with `def kill_horse(self, sig=signal.SIGTERM):`.  
This is required because RQ does not support Windows. We don't need it during development. This change prevents errors.

Create local settings and initialise the database,
```
python create_local_settings.py
python website\manage.py migrate
```
Load demo data and run a development server,
```
python website\manage.py loaddata demo_data
python website\manage.py runserver
```
Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) to view the website.

#### Option 2: Linux Virtual Machine

For Windows and Mac users, it is advised to install a Linux virtual machine and use this to install the project.

* Follow the [instructions](http://www.wikihow.com/Install-Ubuntu-on-VirtualBox) and install Ubuntu on VirtualBox.
* Follow the instructions above for installation on Linux.

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

    (env) $ python website/manage.py test website.core website.jdpages
 
<h3>Automated testing</h3>
[Travis](https://travis-ci.org/jonge-democraten/website) is used to automatically install the environment and run tests on changes in the project.  
The file `.travis.yml` contains the Travis commands to install and test the project.

<h3>Performance</h3>
[Locust](https://github.com/locustio/locust) can be used for load testing. 
It simulates users and provides a web UI to monitor the test.
Easy to install and configure. Read the locust documentation. 
    
-----
## Logging
The Python logging module is used for logging. 

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

<h3>Email error notifications</h3>
All admins, as defined in the ADMINS setting, will receive email notifications of all ERROR level log messages.

<h3>Confidential information</h3>
Confidential information should not be logged. During initial development, logging of confidential information is allowed if marked with a `CONF` tag,
```python 
logger.debug('CONF ' + member.DNA)
```
These will be removed before deployment.  

-----
## Documentation

* Documentation can be found in the `/docs/` directory.
* Docs are writtin in plain text with [Markdown](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet) formatting.
* [MkDocs](http://www.mkdocs.org/) can be used to convert the doc files into nice looking html.
* [readthedocs.org](http://jdwebsite.readthedocs.org/en/latest/) hosts a html version of the documentation, generated from the markdown files.

<h3>MkDocs</h3>
You can use [MkDocs](http://www.mkdocs.org/) to preview the documentation in the readthedocs template.  
Install mkdocs using pip, 

    $ pip install mkdocs
    
run a preview server in the project directory,

    $ mkdocs serve
    
and visit [127.0.0.1:8000](http://127.0.0.1:8000) to preview the generated documentation.

<h3>Code documentation</h3>
* Add comments to code that is not self-explanatory.
* Use [python docstrings](http://en.wikipedia.org/wiki/Docstring#Python) to describe files, classes and functions.
* Add docstrings to files, classes and functions if useful.

**Example**
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
## Database

<h3>Migrations</h3>
A [database migration](https://docs.djangoproject.com/en/1.7/topics/migrations/) needs to be created after database structure changes in `models.py`,

    $ python website/manage.py makemigrations <app_label>  
    
The generated migration file is committed together with changes in `models.py`.  
Migrations have to be carefully managed between different branches, so keep track of other branches and prepare for a merge.

-----
## Demo data

The code base of jdwebsite contains demo data to demonstrate functionality. To create demo data, dump a fixture in `/website/fixtures/`, 

    $ ./create_demo_data.sh

This fixture may be loaded when initialising the development environment (see [Installation](#installation)).

<h3>Caveat</h3>

For some reason, the categories of blog posts in Blogs on non-default Sites are not exported correctly. To include this information, you have to add it by hand.

-----
## Versioning

Version numbers are of the form,

| 1.3.9 | N.N.N | major.minor.micro |
| ------|:-----:| -----:|

* **major** release for everthing worth a new number
* **minor** release for all functional and model (database) changes
* **micro** release for bugfixes and minor view/template modifications 

Pre-releases get a suffix ,

|1.3.9a1| N.N.N(a/b/rc)N |alpha/beta/release-candidate |
|-------------|:----:|----:|

[PEP0440](https://www.python.org/dev/peps/pep-0440/) is used as a basis for the version scheme.
