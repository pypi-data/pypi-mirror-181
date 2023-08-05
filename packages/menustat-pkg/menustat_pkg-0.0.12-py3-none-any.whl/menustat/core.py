import csv
import sys
import math
import glob
from pathlib import Path

import pandas
import sqlalchemy
from tqdm import tqdm
from selenium import webdriver
from sqlalchemy import desc
from sqlalchemy.orm.exc import NoResultFound
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from menustat.log import logger, wrap, writelog
from menustat.utils import *
# add_meta, loop_string_replace, return_range,
from menustat.orm import Franchise, MenuItem, AnnualItemData, return_largest_id_plusone
from menustat.settings import YEAR, engine, session, config
from menustat.scraper import Calculator, WebTable, WebTableReactive, Pdf, MultiPdf, WebSite
from menustat.collecteddf import CollectedDf, check_df_for_issues


classmapper = {
    "calculator":Calculator,
    "pdf":Pdf,
    "pdf.multi":MultiPdf,
    "webtable":WebTable,
    "webtable.reactive":WebTableReactive,
    "website":WebSite,
}


def run_factory(f, driver):
    classargs = {
        "name": f.name,
        "f_id": f.id,
        "headquarters": f.headquarters,
        "nutr_url": f.nutr_url,
        "menu_url": f.menu_url,
        "nutr_scraper":f.nutr_scraper,
        "driver":driver,
        "year":YEAR
    }
    nav_args = config['scrapers']['web_scrapers'][f.name] if f.name\
            in config['scrapers']['web_scrapers'] else {}
    logger.info("nav_args:%s", nav_args)
    classargs.update(nav_args)
    aClass = classmapper[f.nutr_scraper]
    return aClass(**classargs)



def start_selenium(headless=True):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.headless = headless
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
    chrome_options.add_argument(f'user-agent={user_agent}')
    try:

        # driver = webdriver.Remote("http://host.docker.internal:4444/wd/hub",
        #             DesiredCapabilities.CHROME, options=chrome_options)
        driver = webdriver.Chrome(chrome_options=chrome_options)

    except Exception as e:
        # try:
        #     logger.warning("selenium driver startup failed. Using chromedriver"
        #             " autoinstaller instead; this may take a moment.\n"
        #             "Error:{}".format(e), exc_info=True)
        #     chromedriver_autoinstaller.install()
        # except Exception:
        logger.warning("Selenium driver startup failed. Skipping unscraped franchises"
            " requiring selenium-based web scraping.\nError: %s", e, exc_info=True)
        driver = None
    return driver



### COLLECTION METHODS ###
@wrap(writelog, writelog)
def collect_and_clean_annualitemdata(headless_conf=True, dryrun=False, subset=None):
    """ Scrape all menu items from sources listed in franchise table.
    Parameters
    ----------
    headless_conf : bool, optional
        Run Selenium without visible browser window (default is True)
    dryrun : bool, optional
        Execute method without writing to database (default is False)
    subset : int or list, optional
        Execute method on franchise subset (default is None)
        If int, select only franchise with matching id.
        If list, select franchises with ids equal to and between listed ints.
    """

    driver = start_selenium(headless=headless_conf)
    menustat_query = session.query(Franchise).\
        filter(sqlalchemy.not_(Franchise.nutr_scraper == "")).\
        filter(sqlalchemy.not_(Franchise.nutr_scraper.like('%.manual')))
    if type(subset) is int:
        menustat_query = menustat_query.filter(Franchise.id == subset)
    elif type(subset) is tuple:
        menustat_query = menustat_query\
                .filter(Franchise.id >= subset[0])\
                .filter(Franchise.id <= subset[1])
    elif type(subset) is list:
        menustat_query = menustat_query.filter(Franchise.id.in_(subset))
    queue = tqdm(menustat_query.all())
    for f in queue:
        queue.set_postfix_str("{} {}: {}".format(f.id, f.name, f.nutr_scraper))
        try:
            scraped = run_factory(f, driver)
            scraped.collect_clean_sequence()
            logger.debug("pre-clean, in collect_and_clean_annualitemdata")
        except Exception as e:
            logger.warning("\nFAILURE TO COLLECT FRANCHISE ----------------------------"
                    "\nfranchise %s, name %s, scraper %s; passed without entry\n"
                    "Error:\n%s\n------------------------------------------",
                    f.id, f.name, f.nutr_scraper, e, exc_info=True)
            continue
        try:
            df_obj = CollectedDf(f.name, f.id, scraped.nutr_df)
            df_obj.clean()
            df_obj.nutr_df = df_obj.nutr_df.where(pandas.notnull(df_obj.nutr_df), None)
            # df_obj.fillna(np.nan,inplace=True)
            # df_obj.add_df_to_db(dryrun=True)
            df_add = df_obj.nutr_df['menu_item_id'].apply(lambda x: return_menuitem_data(x))
            df_add.rename(columns={
                                0:'matched_item_name',
                                1:'food_category',
                                2:'limited_time_offer',
                                3:'regional',
                                4:'shareable',
                                5:'combo_meal',
                                6:'kids_meal'
                        }, inplace=True)
            df_add.replace(False, "0", inplace=True)
            print("3")
            df_add.replace(True, "1", inplace=True)
            df_obj.nutr_df = df_obj.nutr_df.join(df_add)
            df_obj.nutr_df = df_obj.nutr_df[["matched_item_name", "menu_item_id",
                "food_category", "item_name", "item_description", "serving_size",
                "serving_size_text", "serving_size_unit", "serving_size_household",
                "calories", "total_fat", "saturated_fat", "trans_fat", "cholesterol",
                "sodium", "potassium", "carbohydrates", "protein", "sugar", "dietary_fiber",
                "calories_text", "total_fat_text", "saturated_fat_text", "trans_fat_text",
                "cholesterol_text", "sodium_text", "potassium_text", "carbohydrates_text",
                "protein_text", "sugar_text", "dietary_fiber_text",'kids_meal',
                'limited_time_offer', 'regional', 'shareable', 'combo_meal', "notes"]]
            save_to_csv_for_review(df_obj.nutr_df, f.name, f.nutr_url, f.id, f.nutr_scraper, f.menu_scraper)
        except Exception as e:
            print(e)
            logger.warning("\nFAILURE TO CLEAN FRANCHISE----------------------------"
                    "\nfranchise %s, name %s, scraper %s; passed without entry"
                    "\nError:\n%s\n------------------------------------------",
                                f.id, f.name, f.nutr_scraper, e, exc_info=True)

    driver = None if not driver else driver.quit()


def export_csv(csv_path, table, overwrite=False):
    """Export a database table to csv.

    Parameters
    ----------
    csv_path : string
        Filepath for exported csv.
    table :
    overwrite : (optional) boolean, default False
    """
    if not overwrite:
        if Path(csv_path).exists():
            print("File already exists! Please change the name of the "
                            "existing file or the file to be created.")
            sys.exit(1)
    else:
        check = input("\nATTENTION: This function will overwrite the file at the current path ({}). Is this okay?"+' (y/n): ').lower().strip()
        if check == 'y':
            print("y -- writing table to csv.")
        elif check == 'n':
            print("n -- ending program without writing to csv")
            sys.exit(1)
        else:
            print("input not recognized; closing the program.")
            sys.exit(1)

    fmt = '%Y-%m-%d'
    table_df = pandas.read_sql_table(table, engine,
            parse_dates={"created_at": fmt, "updated_at": fmt})
    table_df.to_csv(csv_path, index=False)


def update_franchise_table_from_csv(csv_import):
    """Add rows from selected csv to franchise database table
    Try updating existing entry; if no entry exists, add new entry.

    Parameters
    ----------
    csv_import : filepath
        file must have identical layout and structure to db table.
    """
    new_db_entries = []
    new_id = return_largest_id_plusone(Franchise, session)
    with open(csv_import, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                query = session.query(Franchise).get(row['id'])
                if not query:
                    raise NoResultFound("no result found")
                if query.name == row["name"]:
                    ud = {k:v for k, v in row.items() if v != getattr(query, k)}
                    ud = add_meta(ud)

                    session.query(Franchise).\
                            filter(Franchise.id == row['id']).\
                            update(ud, synchronize_session = False)
                else:
                    raise ValueError("franchise name-id mismatch!")
            except NoResultFound:
                logger.info("No match:%s\nAdding row", row["franchise"])
                entryargs = {k:v for k, v in row.items()}
                entryargs = add_meta(entryargs, created=True)
                entryargs['id'] = new_id
                new_db_entries.append(Franchise(**entryargs))
                new_id += 1
            except ValueError as err:
                logger.warning("%s id %s:%s; skipping row.", row["name"], row['id'], err)
    session.add_all(new_db_entries)
    session.commit()


### REVIEW FUNCTIONS ###
def return_menuitem_data(menu_item_id):
    if menu_item_id not in [None, np.nan] and not math.isnan(menu_item_id):
        print(menu_item_id)
        menu_item = session.query(MenuItem).filter(MenuItem.id == menu_item_id).one()
        try:
            logger.warning("Adding new MenuItem:\n %s, %s, %s, %s, %s, %s, %s",
                            menu_item.item_name, menu_item.food_category,
                            menu_item.limited_time_offer, menu_item.regional,
                            menu_item.shareable, menu_item.combo_meal, menu_item.kids_meal)
            return pandas.Series([
                                menu_item.item_name,
                                menu_item.food_category,
                                menu_item.limited_time_offer,
                                menu_item.regional,
                                menu_item.shareable,
                                menu_item.combo_meal,
                                menu_item.kids_meal
                                ])
        except Exception as e:
            logger.info(e)
            return pandas.Series([None, None, None, None, None, None, None])
    else:
        return pandas.Series([None, None, None, None, None, None, None])

def check_dfs_for_issues():
    """ Run check_df_for_issues method on all csvs in dfs_for_review directory.
    """
    csvs = glob.glob("./data/dfs_for_review/*")
    for csv_ in csvs:
        df = pandas.read_csv(csv_)
        name = str(df.loc[3, "item_name"])
        check_df_for_issues(name, df)

    # add condition to check number of entries without matches

def return_matched_value(mi_id, field):
    if mi_id not in [None, np.nan] and not math.isnan(mi_id):
        past_entry = session.query(AnnualItemData).filter(
                AnnualItemData.menu_item_id == mi_id).order_by(
                desc(AnnualItemData.year)).first()
        return getattr(past_entry, field)
    return None

def save_to_csv_for_review(nutr_df, name, url, f_id, nutr_scraper, menu_scraper):
    to_csv_df = nutr_df.copy()
    to_csv_df['name'] = name
    if "iurl" not in to_csv_df:
        to_csv_df['iurl'] = url
    to_csv_df['f_id'] = f_id
    to_csv_df['nutr_scraper'] = nutr_scraper
    to_csv_df['menu_scraper'] = menu_scraper
    to_csv_df.insert(1, 'matched_item_description', None)
    to_csv_df['matched_item_description'] = to_csv_df['menu_item_id'].apply(
                        lambda x: return_matched_value(x, "item_description"))
    for column in ["_household", "_text", "_unit", ""]:
        colname = "serving_size" + column
        matched_colname = "matched_"+ colname
        to_csv_df.insert(2, matched_colname, None)
        to_csv_df[matched_colname] = to_csv_df['menu_item_id'].apply(
                                    lambda x: return_matched_value(x, colname))
    prepped_id = "{}{}".format("0"*(3-len(str(f_id))),f_id)
    to_csv_df.to_csv("data/dfs_for_review/{}-{}.csv".format(prepped_id,\
            name.lower().replace("/", "_")), index=False)
