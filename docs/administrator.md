# Administrator guide

## Introduction

The code of the new JD website is written to be readible and accessible. The same holds for the code of Mezzanine, the framework upon which the site is built. However, this should be of no concernt to the people who perform day-to-day administration of the site. This guide is for them.

### Intended audience

This guide is written for administrators of the JD website.

### Purpose

This document has three purposes:
* provide instructions for *deploying* a stable and secure instance of the website;
* provide guidance for *day-to-day administration* of an active instance of the website.

## Deployment

### The broad lines: deploying Mezzanine

Our instance of the website runs on WSGI, which is a deployment platform for Python applications. To a great extent, our website is just a Django website. Instructions for deployment, such as at [https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/](https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/), will take care of the broad lines. The rest of this section is dedicated to the details.

### Database backend: MySQL

The instructions at [https://docs.djangoproject.com/en/1.8/ref/databases/](https://docs.djangoproject.com/en/1.8/ref/databases/), about how to set up a database backend for a Django application, will guide you to installing your preferred database backend. We have done development on an SQLite backend. Testing and production run on a MySQL backend. We have not tried any others.

### Timezone tables

Make sure the database contains the timezone tables, needed by the calendar app.

For MySQL, see [http://dev.mysql.com/doc/refman/5.6/en/mysql-tzinfo-to-sql.html](http://dev.mysql.com/doc/refman/5.6/en/mysql-tzinfo-to-sql.html).

### Twitter Feed Update

The [Mezzanine Twitter app](http://mezzanine.jupo.org/docs/twitter-integration.html?highlight=twitter) is used to consume, store and display tweets.

The twitter feed needs to be updated with tweets via a script that calls the `poll_twitter` management command,
`/usr/local/bin/poll_twitter.sh`:

```bash
#!/bin/sh
#

PROJECTDIR="/usr/share/website/site/website"
VENVDIR="/usr/share/website/site/env"
RUNAS="website"

sudo -u ${RUNAS} -H bash -c "source $VENVDIR/bin/activate; ${PROJECTDIR}/manage.py poll_twitter"
```

Create a cronjob to run the script every 10 minutes,
`/etc/cron.d/website-twitter`:

```bash
MAILTO=root
*/10 * * * * root /usr/local/bin/poll_twitter.sh 2>&1 | logger -tpoll_twitter
```

### Hemres: newsletter sending

Hemres is used to create and send newsletters. The newsletters need to be sent via a script that calls the `hemres_send` management command, `/usr/local/bin/send_newsletters.sh`:

```bash
#!/bin/sh
#

PROJECTDIR="/usr/share/website/site/website"
VENVDIR="/usr/share/website/site/env"
RUNAS="website"

sudo -u ${RUNAS} -H bash -c "source $VENVDIR/bin/activate; ${PROJECTDIR}/manage.py hemres_send /tmp/hemres.lock"
```

Create a cronjob to run the script every 10 minutes, `/etc/cron.d/website-twitter`:

```bash
MAILTO=root
*/10 * * * * root /usr/local/bin/send_newsletters.sh 2>&1 | logger -themres_send
```

### Hemres: daily cleanup

Hemres needs a daily cleanup to delete the contact information of people who are no longer subscribed to any newsletters. The cleanup nees to be run via a script that calls the `hemres_cleanup` managemnt command, `/usr/local/bin/hemres_cleanup.sh`:

```bash
#!/bin/sh
#

PROJECTDIR="/usr/share/website/site/website"
VENVDIR="/usr/share/website/site/env"
RUNAS="website"

sudo -u ${RUNAS} -H bash -c "source $VENVDIR/bin/activate; ${PROJECTDIR}/manage.py hemres_cleanup"
```

Create a cronjob to run the script every day, `/etc/cron.d/website-hemres-cleanup`:

```bash
MAILTO=root
18 4 * * * root /usr/local/bin/hemres_cleanup.sh 2>&1 | logger -themres_cleanup
```

## Day-to-day administration

Some tasks come up during day-to-day administration of the website. Here is how to perform them.

### Set up a development version of the website

In order to run acceptance tests, it may be nice to run a second version of the website in parallel from the first.

1. Make a full copy of the MySQL database into another database. Create a user with full access to this secondary database.
1. 

### Deploy new code

New code is introduced by pulling it from GitHub.

1. Change to user website: `su -s/bin/bash website`.
1. Fetch the new code from GitHub: `git fetch`.
1. Checkout the new version tag: `git checkout <version_tag_name>`.
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
