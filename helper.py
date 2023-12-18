import sqlite3
import os
from datetime import datetime


def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


def get_email_template(course_name: int, enquirer_type: str, blocks: list[str]) -> str:
    """Creates email template to be rendered by the webpage"""
    email_template = ""

    with open(
        os.path.join(os.path.dirname(__file__), "templates/email_template.html"), "r"
    ) as file:
        email_template = " ".join((email_template, file.read()))

    email_template = email_template.format_map({"blocks": get_blocks(blocks)})

    course_info = updated_dict(get_course_info(course_name))

    key_dates = get_key_dates(course_name, enquirer_type)
    course_info["key_dates"] = key_date_string_generator(
        key_dates, datetime.today().date(), 30
    )

    email_template = email_template.format_map(course_info)

    return email_template


def replace_strings(replacements: dict, string: str):
    for key, value in replacements.items():
        if key in string:
            string = string.replace(key, value)

    return string


def course_url(course_info: dict) -> str:
    replacements = {" ": "-", "(": "", ")": ""}
    course_name = replace_strings(
        replacements=replacements, string=course_info["course_name"].lower()
    )

    url = f"https://www.mq.edu.au/study/find-a-course/courses/{course_name}"

    return url


def get_blocks(blocks: list[str]) -> str:
    blocks_template = ""

    for id in blocks:
        id = int(id)
        conn = get_db()
        cur = conn.cursor()
        block_html = cur.execute(
            "SELECT block FROM html_blocks WHERE id = ?", (id,)
        ).fetchone()
        blocks_template = " ".join((blocks_template, block_html["block"]))

    return blocks_template


def get_course_info(course_id: int):
    conn = get_db()
    cur = conn.cursor()
    degree_info = dict(
        cur.execute("SELECT * FROM degrees WHERE id = ?", (course_id,)).fetchone()
    )

    degree_info["course_url"] = course_url(degree_info)

    return dict(degree_info)


# Ensures that when we format the template we do no have a keyError and instead it leaves that section blank
class updated_dict(dict):
    def __missing__(self, key):
        return ""


def get_key_dates(course_id: int, enquirer_type: str):
    if enquirer_type == "rsl":
        query = """
            SELECT name, key_dates.start_date, key_dates.open_date, key_dates.close_date
            FROM date_link
            JOIN degrees
            ON date_link.degree_id = degrees.id
            JOIN key_dates
            ON date_link.session_id = key_dates.id
            WHERE degrees.id = ? AND key_dates.name IN ('Session 1', 'Term 1', 'Term 2')
        """

    else:
        query = """
            SELECT key_dates.name, key_dates.start_date, key_dates.open_date, key_dates.close_date
            FROM date_link
            JOIN degrees
            ON date_link.degree_id = degrees.id
            JOIN key_dates
            ON date_link.session_id = key_dates.id
            WHERE degrees.id = ?
        """

    conn = get_db()
    cur = conn.cursor()
    cur.execute(query, (course_id,))
    result = cur.fetchall()

    key_dates = [dict(item) for item in result]

    for i, date in enumerate(key_dates):
        key_dates[i]["start_date"] = datetime.strptime(
            date["start_date"], "%Y-%m-%d"
        ).date()
        key_dates[i]["open_date"] = datetime.strptime(
            date["open_date"], "%Y-%m-%d"
        ).date()
        key_dates[i]["close_date"] = datetime.strptime(
            date["close_date"], "%Y-%m-%d"
        ).date()

    return key_dates


def key_date_string_generator(
    study_periods: list[dict], date: datetime.date, close_days: int
):
    strings = []

    for item in study_periods:
        if date > item["close_date"] and (date - item["start_date"]).days < close_days:
            x = f"Applications for {item['name']} {item['start_date'].year} ({clean(item['start_date'])}) closed {clean(item['close_date'])}."
            strings.append(x)
        elif item["open_date"] <= date <= item["close_date"]:
            x = f"Applications are currently open for {item['name']} {item['start_date'].year} ({clean(item['start_date'])}), and will close {clean(item['close_date'])}."
            strings.append(x)
        elif date <= item["open_date"]:
            x = f"Applications for {item['name']} {item['start_date'].year} ({clean(item['start_date'])}) will open {clean(item['open_date'])}, and will close {clean(item['close_date'])}."
            strings.append(x)

    final_string = " ".join(strings)

    return final_string


def clean(date: datetime.date):
    return date.strftime("%d %B %Y")
