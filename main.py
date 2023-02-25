#!/usr/bin/env python3
# main.py
# ColdMacaroni 2023. Licensed under GPLv3
# A script that pulls the weekly schedule for this week and saves to a file

import requests
import textwrap
import tabulate
import bs4
from datetime import datetime, date, timedelta
from dotenv import load_dotenv
from os import getenv

# Where to go for info, and where to save it- from a .env file
load_dotenv()

LINK = getenv("LINK")
LAST_UPDATE_FN = getenv("LAST_UPDATE_FN")
SCHEDULE_OUT_FN = getenv("SCHEDULE_OUT_FN")

# This determines how many days before the day defined in WEEK_STARTS the file
# SCHEDULE_OUT_FN should be updated. This update happens ALWAYS. This is so you
# have time to process the week before it actually starts
UPDATE_DAYS_BEFORE_START = 3

# This determines how old the last schedule should be allowed to be. This is in
# case the schedule is updated within the same week can be received.
# SCHED_EXP = SCHEDULE_EXPIRATION
SCHED_EXP_HOURS = 24

MAX_COLUMN_WIDTH = 30

# These dates determine the monday for each week.
# These are for: Trimester 1
WEEK_STARTS = (date.fromisoformat('2023-02-27'),
               date.fromisoformat('2023-03-06'),
               date.fromisoformat('2023-03-13'),
               date.fromisoformat('2023-03-20'),
               date.fromisoformat('2023-03-27'),
               date.fromisoformat('2023-04-03'),
               date.fromisoformat('2023-04-24'),
               date.fromisoformat('2023-05-01'),
               date.fromisoformat('2023-05-08'),
               date.fromisoformat('2023-05-15'),
               date.fromisoformat('2023-05-22'),
               date.fromisoformat('2023-05-29'))

def get_schedule_webpage(link: str | None = None) -> str:
    """
    Simply gets the HTML from the given link via request.
    Raises ValueError if code 200 is not received!
    """
    if link is None:
        link = LINK

    res = requests.get(LINK)
    
    if res.status_code != 200:
        raise ValueError(f"Request to {LINK} returned {res.status_code}")
    
    return res.text


def find_week(day: date | datetime) -> int:
    """
    Find which week the given day belongs to. Returns the index of the given
    week and the day that week starts (Monday). This depends on
    UPDATE_DAYS_BEFORE_START and WEEK_STARTS.
    The starting date returned ignores UPDATE_DAYS_BEFORE_START
    """
    # WEEK_STARTS are type date, we have to convert to be able to compare
    if isinstance(day, datetime):
        day = day.date()

    for idx, week in enumerate(WEEK_STARTS):
        if (week - timedelta(days=UPDATE_DAYS_BEFORE_START)) <= day:
            current_week_idx = idx
            break
    else:
        return None

    return current_week_idx


def format_week_table(tab: bs4.Tag, strip_header: int = 0) -> str:
    # What to put at the top
    headers = ["", "Day/Date", "Topic", "Slides", "TODOs"]

    # Some have empty spaces as children, which is really annoying
    tbody = tab.select("tbody")
    table_ls = []
    for tb in tbody:
        for ch in tb.children:
            # These are all empty for whatever reason
            if isinstance(ch, bs4.NavigableString):
                assert len(ch.text), "NavigableString len is not 1"
                continue

            ls = []

            for content in ch.children:
                # These are all empty for whatever reason
                if isinstance(ch, bs4.NavigableString):
                    assert len(ch.text), "NavigableString len is not 1"
                    continue

                ls.append('\n'.join(textwrap.wrap(content.text.strip(), MAX_COLUMN_WIDTH)))

            # Get rid of empty strings
            ls = list(filter(bool, ls))

            table_ls.append(ls)

    table_ls = table_ls[strip_header:]

    txt = tabulate.tabulate(table_ls, headers=headers, tablefmt='fancy_grid')

    return txt

def main():
    """
    Checks and updates the local schedule if needed. Making use of expiration
    dates and days before start. The schedule for the week then gets formatted
    and written to a file if updated. Otherwise, nothing happens.
    """
    update_needed = False

    now = datetime.now()

    # Get stored time of the last update
    with open(LAST_UPDATE_FN, "r") as file_lastup:
        last_update = datetime.fromtimestamp(
            float(file_lastup.read().strip())
        )

    # cur_wk = current_week
    cur_wk_idx = find_week(now)

    # - Check if the schedule needs to be updated
    # Check if it has expired
    time_since_update = now - last_update

    # timedeltas are stored in days, seconds, and microseconds.
    # (https://docs.python.org/3/library/datetime.html#timedelta-objects)
    # We only care for days & seconds because we're comparing hours. They're
    # stored such that they all add up to the actual delta.

    hrs_since_update = time_since_update.days * 24\
                       + (time_since_update.seconds / 60 / 60)

    update_needed = (hrs_since_update >= SCHED_EXP_HOURS)

    # Check if we need to change to the next week. Using or so we dont ignore last check.
    update_needed = (find_week(last_update) != cur_wk_idx) or update_needed

    # Stop everything if no update is needed
    if not update_needed:
        print("No update needed!")
        return

    # - Get the new page!
    # Grab the page. Exception will be raised if request fails

    html = get_schedule_webpage()
    
    # Soupify :D
    page_soup = bs4.BeautifulSoup(html, features="lxml")

    # The tables with the weekly info have the tag <table class="foswikiTable">  
    week_tables = page_soup.select(".foswikiTable")

    # For SOME REASON, some tables are fused into one singular table. Rather unfortunate.
    # I will hardcode the script to deal with those in some way, but I'm leaving this check in case it gets fixed
    assert len(week_tables) == 9, "There are no longer 9 tables on the website."

    # Some tables are fucked up, easiest way to tell is because they have more than one header.
    # We skip the first week and mark it as ok because it includes orientation info.
    bad_table_list = [len(tab.select("th")) != 2 for tab in week_tables[1:]]
    bad_table_list.insert(0, False)

    if not bad_table_list[cur_wk_idx]:
        wk_tab = week_tables[cur_wk_idx]

        # Ignore orientation info if it's the first week
        strip_header = 0
        if cur_wk_idx == 0:
            strip_header = 2
        tab_txt = format_week_table(wk_tab, strip_header)

    else:
        # Cry
        tab_txt = f"This week is fucked up on the website. You're currently on week {cur_wk_idx + 1}."

    tab_txt = f"Link: {LINK}\n" + f"Last Updated: {now.date().isoformat()}\n" + f"You're on Week {cur_wk_idx + 1}. This week starts on {WEEK_STARTS[cur_wk_idx].isoformat()}\n" + tab_txt + '\n'

    print(tab_txt)

    # Update day
    with open(LAST_UPDATE_FN, "w") as f:
        f.write(str(now.timestamp()))

    # Update stored table
    with open(SCHEDULE_OUT_FN, "w") as f:
        f.write(tab_txt)
    

if __name__ == "__main__":
    main()
