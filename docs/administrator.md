# Administrator guide

## Introduction

The code of the new JD website is written to be readible and accessible. The same holds for the code of Mezzanine, the framework upon which the site is built. However, this should be of no concernt to the people who perform day-to-day administration of the site. This guide is for them.

### Intended audience

This guide is written for administrators of the JD website.

### Purpose

This document has three purposes:
* provide instructions for *deploying* a stable and secure instance of the website;
* provide a step-by-step walkthrough of *importing* the data in an old Joomla installation to your new website;
* provide guidance for *day-to-day administration* of an active instance of the website.

## Deployment

### The broad lines: deploying Mezzanine

Our instance of the website runs on WSGI, which is a deployment platform for Python applications. To a great extent, our website is just a Django website. Instructions for deployment, such as at [https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/](https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/), will take care of the broad lines. The rest of this section is dedicated to the details.

### Database backend: MySQL

The instructions at [https://docs.djangoproject.com/en/1.8/ref/databases/](https://docs.djangoproject.com/en/1.8/ref/databases/), about how to set up a database backend for a Django application, will guide you to installing your preferred database backend. We have done development on an SQLite backend. Testing and production run on a MySQL backend. We have not tried any others.

### Timezone tables

Make sure the database contains the timezone tables, needed by the calendar app.

For MySQL, see [http://dev.mysql.com/doc/refman/5.6/en/mysql-tzinfo-to-sql.html](http://dev.mysql.com/doc/refman/5.6/en/mysql-tzinfo-to-sql.html).

## Importing data from Joomla

When deploying the website for production, you will not want to use the demo data. Instead, you want to import data from an existing website. For our existing Joomla installation, we have provided migration scripts.

### How to migrate

**Preparations**

1. Make a list of all blog posts and events that have been created in the past month on all department websites. Note their current URLs.
1. For every item on the list, find its new URL on the test environtment.
1. Enter these URLs into the `import_redirect()` function of `/website/management/commands/jd_finalize.py`. Examples are provided there.

**Actual migration**

1. Log in to the server as root
1. Switch to the website user: `su -s/bin/bash website`.
1. Go to your home directory: `cd`.
1. Run `./migrate.sh`.
1. Create a local admin user with a *strong* password.
1. If an error occurs, fix it and rerun `./migrate.sh`. Note any warnings.

**Post-migration testing**

1. Test the website after migration. Does everything work?
1. Check especially whether the content concerning the warnings in the previous step works.
1. If you run into any problems, fix them and go back to running `./migrate.sh`.

**Switching the sites**

1. Rename the main Mezzanine site to jongedemocraten.nl.
1. Change the Apache config to rename the site to jongedemocraten.nl in the config for this website. The config for the Joomla website should be renamed to someting else, e.g. oldsite.jongedemocraten.nl.
1. Protect access to the old site with a client certificate requirement. Peek at the phpmyadmin config to see how to do this.

### Functionality of the migration scripts

**migrate.sh**

`migrate.sh` is the migration script that calls all others. It is kept outside of the repository because it contains database credentials. It makes use of the Django manage.py interface to run further migration steps.

**jd_pre.py**

By default, the syncdb command creates a site named 'example.com' with site ID 1. Since we depend on the main site to have site ID 1, we want to rename the example.com site to our own name. `jd_pre.py` takes care of that.

**jd_joomla_import_site.py**

The import process happens on a site-by-site basis. `migrate.sh` calls `jd_joomla_import_site.py` once for every site. This script then handles retrieving the content (pages, blog posts, blog categories, events) from the old site and importing it into the new one.

**jd_finalize.py**

Even though `jd_joomla_import_site.py` handles most content, there are some things that it cannot do. Therefore, it is necessary to have an additional step, after importing all sites and their content. `jd_finalize.py` provides this step. It is run only once. It sets all configuration options for all sites, such as Twitter search queries, sidebar blogs, menu layout, group permissions, column elements and many other things. It also migrates the newsletters and their subscribers.

## Day-to-day administration

Some tasks come up during day-to-day administration of the website. Here is how to perform them.

### Set up a development version of the website

In order to run acceptance tests, it may be nice to run a second version of the website in parallel from the first.

1. Make a full copy of the MySQL database into another database. Create a user with full access to this secondary database.
1. 

### Deploy new code

New code is introduced by pulling it from GitHub.

1. Change to user website: `su -s/bin/bash website`.
1. Pull the new code from GitHub: `git pull`.
1. Source the virtualenv: `source env/bin/activate`.
1. Upgrade any packages based on the requirements file: `pip3 install -r requirements.txt`.
1. Apply migrations if necessary: `website/manage.py migrate`.
1. Redeploy static files, if necessary: `umask 022 && website/manage.py collectstatic`.
1. Reload the WSGI server: `# pkill -HUP -u website uwsgi`.

### Create a full backup

Backing up is done by making a copy of the following data:

* The full database
* The `local_settings.py` file.
* The `website/static/website/media` directory.

### Restore a full backup

Restoring a backup is done by overwriting the current data with the data from the backup.

Be sure to run the restored data on the same version of the website codebase as the one used when backing it up.
