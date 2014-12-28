<h1>Database</h1>

## Introduction

## Migrations
A [database migration](https://docs.djangoproject.com/en/1.7/topics/migrations/) needs to be created after database structure changes in `models.py`,  
`$ python website/manage.py makemigrations <app_label>`  
The generated migration file is committed together with changes in `models.py`.  
Migrations have to be carefully managed between different branches, so keep track of other branches and prepare for a merge.
 
