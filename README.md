# Thought Industries Data Engineering Code Challenge

Congratulations on making it to the code challenge step of the interview process!

This challenge is designed to test your knowledge of Python, ETL, LookML and data modeling.
This readme will outline how to get started and what's expected of the two challenge components.

## Getting Started

To get started with the challenge, please try and leverage GitHub by either creating a **private** repository from
this template or creating a **private** fork and setting that up on your machine. As a last resort, you can download
a zip file. 

Once you have the code on your machine, you're ready to begin the ETL portion of the challenge.

### Data Model
For the both the ETL and Looker challenges, please refer to the following data model.

![data-model](data-model.png?raw=true "Data Model")

## ETL Challenge

The ETL challenge will test your Python and ETL skills by requiring you to 
implement the extract and load functions of a Python library.
The documentation within the code outlines what's expected. 

The goal is to move data from a RethinkDB instance into a PostgreSQL instance. 
You're work is verified via pytest cases. 

The system requirements, general procedure and rules are outlined below.

### System Requirements
1. UNIX-based environment (MacOS, Ubuntu/Linux). Windows systems should work, 
but may require tweaks to the setup and run scripts, but these can also be performed manually.
2. Docker

### Procedure
The code is written to be run within a docker compose deployment to reduce local system dependencies.
All commands to deploy and run the ETL test are in the `run` script.

2. Review and run the `run` script. The tests will fail, but you'll get familiar with how the system runs.
3. Review the code in `tests/test.py` and `lib/etl.py` to see what needs to be implemented.
4. Implement the necessary functions
5. When confident in your solution, confirm that the run script runs successfully and all tests are passing.

If you want to keep the docker-compose deployment up so you can interactively run code 
in the Python container as you make changes, just run `docker-compose up -d`. 
Just remember that RethinkDB and Postgres need initialization when initially deployed.

### Rules
1. No modifying of the `test.py` file
2. The functions should be implemented as outlined by the docs, 
no adding of parameters or changing of return types.
2. Your solution can be as simple or complex as you like, so long as the tests pass.

## Looker Challenge

This section will test your Looker/LookML and data modeling skills. 
You will be implementing code necessary to expose data within Looker, namely views, models and explores.

Unless you have a Looker instance to develop in, this will be free hand coding (a Looker instance is not required for this challenge).
You are expected to follow LookML syntax to the best of your ability. If you are not familiar with 
LookML, please check out their free [course](https://training.looker.com/looker-development-foundations) 
and [documentation](https://docs.looker.com/data-modeling/learning-lookml/lookml-intro).

All code should be stored in the `looker` folder in their respective folders.

### Procedure
1. Create one view for each table in the data model, stored in the views folder. There should be one dimension for each field, 
as well as a count measure.
2. Create a model called `ti` and additional `ti_shared.lkml` file stored in the models folder. 
The `ti` model should contain includes for `ti_shared.lkml` and the explores. 
This should be accomplished using only 2 include statements. The model should also contain a connection string for a connection named `postgres`.
3. In `ti_shared.lkml` use access grants to create three levels of access based on a `access_level` user attribute.
These access levels should be called internal, company and client. Access should be additive starting from internal
(internal also gets company and client access, company gets client access).
4. Create one explore file for each view, stored in the explore folder. Explores files should be structured so
that there is one base explore (extension required) which is extended once per access level defined in `ti_shared`. Each explore
should have joins for all related tables, with join conditions and relationship (cardinality) defined. Explores with 
Explore file names should match the names of the view they are based on.<br/><br/>
For access levels of company and client, add access filters for company and client users attributes (mapped to the company and client dimensions of the base view). Company access needs access filters for company, while client access needs filters for both company and client. 

## Completion
When you have completed all sections, ensure your work is pushed up to GitHub, then invite 
matt.girard@thoughtindustries.com as a collaborator to your fork/repo and reply to the code challenge e-mail with a link to the fork/repo.

If you decided to not use GitHub, please send a zip file of your work instead.

Once you've shared your work, it will be reviewed and you will be notified of next steps.



