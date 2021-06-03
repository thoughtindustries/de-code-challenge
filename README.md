# Thought Industries Data Engineering Code Challenge

Congratulations on making it to the code challenge step of the interview process!

This challenge is designed to test your knowledge of Python, ETL, LookML and data modeling.
This readme will outline how to get started and what's expected of the two challenge components.

## Getting Started

To get started with the challenge, you can either download a zip file of this repo, 
or create your own fork in GitHub.

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
but may require tweaks to the setup and run scripts, but these can be performed manually.
2. Docker

### Procedure
1. Run the `setup` script, this installs pyenv, installs the necessary Python version, 
sets up a virtual environment and installs the necessary Python packages
2. Review and run the `run` script. The pytests will fail, but you'll get familiar with how the system runs.
3. Review the code in `test.py` and `src/etl.py` to see what needs to be implemented.
4. Implement the necessary functions
5. When confident in your solution, confirm that the run script runs successfully and all tests are passing.

### Rules
1. No touching of the `test.py` file
2. The functions should be implemented as outlined by the docs, 
no adding of parameters or changing of return types.
2. Your solution can be as simple or complex as you like, so long as the tests pass.

## Looker

This section will test your Looker/LookML and data modeling skills. 
You will be implementing code necessary to expose data within Looker, namely views, models and explores.

Unless you happen to have a Looker instance running locally to develop in, this will be free hand coding.
You are expected to follow LookML syntax to the best of your ability. 

All code should be stored in the `looker` folder in their respective folders.

### Procedure
1. Create one view for each table in the data model, stored in the views folder. There should be one dimension for each field, 
as well as a count measure.
2. Create a model called `ti` and additional `ti_shared.lkml` file stored in the models folder. 
The `ti` model should contain includes for `ti_shared.lkml` and the views and the explores. 
This should be accomplished using only include 3 statements. The model should also contain a connection string for a connection named `postgres`.
3. In `ti_shared.lkml` use access grants to create three levels of access based on a `access_level` user attribute.
These access levels should be called internal, company and client. Access should be additive starting from internal
(internal also gets company and client access).
4. Create one explore file for each view, stored in the explore folder. Explores files should be structured so
that there is one base explore which is extended once per access level defined in `ti_shared`. Each explore
should have joins for all related tables, with join conditions and relationship (cardinality) defined.
Explore file names should match names of the view they are based on.

## Completion
When you have completed both sections, you can either share a link to your GitHub fork, 
or zip up your files and share via e-mail.

You will be notified of your results and next steps in a timely manner.



