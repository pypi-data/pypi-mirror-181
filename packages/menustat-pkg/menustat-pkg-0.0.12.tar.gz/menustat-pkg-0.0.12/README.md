# MenuStat Project Repository

This module is written and maintained to automate tasks related to the collection, cleaning, validation, and storage of nutrition data for the MenuStat database stewarded by Harvard University FAS Research Computing.


## Repository Overview

### `core.py`
core functions and CollectedDf class.

### `exceptions.py`
Exceptions.

### `log.py`
Logger.

### `orm.py`
SQLAlchemy ORM classes.

### `scraper.py`
Scraper classes and subclasses.

### `settings.py`
Settings - will need to be manually set by the user.

### `utils.py`
Utility functions.

### `templates/menustat_config.yaml`
Template of the config file needed to run the application.

## Using the Module
The primary purpose of this module is to automatically collect data for the franchises listed in the database's `franchises` table.

To review and update the contents of the database's `franchises` table:
1. `from menustat import core`, then `core.export_csv("2021_menustat_franchise_table.csv", "franchises")`
2. Update the franchise entries as needed.
3. Update the database table with the csv by running the command `core.import_csv("2021_menustat_franchise_table.csv", core.Franchise)`

To run the scraper on all franchises in the table, run:

    core.collect_and_enter_annualitemdata(dryrun=True)

To run the scraper on, for example, a franchise with the ID number 30, run:

    core.collect_and_enter_annualitemdata(dryrun=True, subset=30)
