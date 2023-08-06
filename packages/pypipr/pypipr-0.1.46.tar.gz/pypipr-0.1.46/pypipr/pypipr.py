""" PYPIPR Module """
from . import iconstant

"""PYTHON Standard Module"""
import datetime
import zoneinfo
import re
import subprocess
import platform
import pathlib
import urllib.request
import random
import webbrowser
import json
import shutil
import uuid
import math
import time
import threading
import asyncio
import multiprocessing

WINDOWS = platform.system() == "Windows"
LINUX = platform.system() == "Linux"

if WINDOWS:
    import msvcrt as _getch


"""PYPI Module"""
import colorama
import lxml.html

if LINUX:
    import getch as _getch


colorama.init()


class Pypipr:
    @staticmethod
    def test_print():
        """Print simple text to test this module is working"""
        print("Hello from PyPIPr")


class idatetime:
    # ubah variabel debug saat development untuk menampilkan informasi yg berguna
    debug = False

    regex_for_parse_input = r"(?:\d|\w|\-|\+|\:|\.|\'|\/)+"

    timestamp_regex = r"\d{10,22}"

    date_year_front = "(\d{3,4})"
    date_year_back = "(\d{1,4})"
    date_month = r"(0?[1-9]|1[012]|(?:jan(?:uary)?)|(?:feb(?:ruary)?)|(?:mar(?:ch)?)|(?:apr(?:il)?)|may|(?:ju(?:ne?|ly?))|(?:aug(?:ust)?)|(?:sep(?:tember)?)|(?:oct(?:ober)?)|(?:(?:nov|dec)(?:ember)?))"
    date_day = r"(0?[1-9]|[12][0-9]|3[01])"
    date_separator = "[^a-zA-Z0-9:]+"
    date_regex = rf"(?:{date_year_front}{date_separator})?(?:{date_month}{date_separator})?{date_day}(?(2)|{date_separator}{date_month})?(?(1)|{date_separator}{date_year_back})?"

    time_hour_24 = r"([01]?\d|2[0-4])"
    time_hour_12 = "(0?\d|1[012])"
    time_minute = r"([0-5]?\d)"
    time_second = r"([0-5]?\d)"
    time_milisecond = r"(\d{5,9})"
    time_am = "([ap]m)"
    time_separator = "(?:[^a-zA-Z0-9\/\-]+)"
    time_regex = rf"(?:{time_hour_12}|{time_hour_24})(?:(?:{time_separator}{time_minute})(?:{time_separator}{time_second}(?:{time_separator}{time_milisecond})?)?)?(?(1){time_separator}?{time_am})?"

    tz_separator = "[^a-zA-Z0-9]"
    tz_benua = "([a-zA-Z_]+)"
    tz_kota = "([a-zA-Z_]+)"
    tz_plus = "(\+|\-)"
    tz_hour = "(\d{1,2})"
    tz_minute = "(\d{2})"
    tz_second = "(\d{2})"
    tz_microssecond = "(\d{3,6})"
    tz_regex = rf"(?:{tz_benua}{tz_separator})?{tz_kota}?(?:{tz_plus}{tz_hour}(?:{tz_separator}?{tz_minute}(?:{tz_separator}?{tz_second}(?:{tz_separator}?{tz_microssecond})?)?)?)?"

    datetime_separator = "[^a-zA-Z0-9]"
    datetime_regex = rf"({date_regex})?{datetime_separator}({time_regex})?{datetime_separator}?({tz_regex})?"

    year_regex = r"(\d{4}|\'\d{2})"

    list_regex = {
        "timestamp": timestamp_regex,
        # "datetime": datetime_regex,
        "date": date_regex,
        "time": time_regex,
        "tzinfo": tz_regex,
        "year": year_regex,
        "month": date_month,
        "day": date_day,
        "hour": time_hour_24,
        "minute": time_minute,
        "second": time_second,
        "microsecond": time_milisecond,
    }

    def __init__(
        self,
        human_string_datetime,
        default_year=1900,
        default_month=1,
        default_day=1,
        overwrite=None,
    ):
        """
        Membuat idatetime object dengan input teks yg mengandung unsur waktu dan tanggal.
        defaul_*    : digunakan untuk mengisikan nilai awal
        overwrite   : digunakan untuk mengubah hasil proses menjadi datetime yg di khususkan

        contoh:
        self.overwrite_date= {
            "tzinfo": int type,
            "year": int type,
            "month": int type,
            "day": int type,
            "hour": int type,
            "minute": int type,
            "second": int type,
            "microsecond": int type,
        }
        """

        self.result = {
            "tzinfo": [],
            "year": [],
            "month": [],
            "day": [],
            "hour": [],
            "minute": [],
            "second": [],
            "microsecond": [],
        }

        self.default_date = {
            "year": default_year,
            "month": default_month,
            "day": default_day,
        }

        self.overwrite_date = overwrite if overwrite else {}

        for text in self.parse_string(human_string_datetime):
            for index, value in self.list_regex.items():
                if r := re.fullmatch(value, text, re.IGNORECASE):
                    r = self.sanitize_regex_result(r)
                    if n := getattr(self, f"parse_{index}")(r):
                        for i, v in n.items():
                            self.result[i].append(v)

    def to_datetime(self):
        """
        Return idatetime menjadi python standard library datetime object.

        Langkah:
        - Python datetime memerlukan Year, Month, Day untuk diisikan, jadi digunakan
            default year, month, day
        - Kemudian diupdate dengan data hasil proses program
        - Kemudian diupdate kembali dengan data overwrite yg diinputkan
        """

        """
        Fungsi ini masih belum sempurna.
        Fungsi ini harus dapat menentukan nilai yg tepat untuk variabel.
        Fungsi ini berjalan masih menggunakan nilai pertama yg ditemukan.
        """
        d = self.default_date
        c = {x: y[0] for x, y in self.result.items() if len(y) and y[0] is not None}
        d.update(c)
        d.update(self.overwrite_date)

        if self.debug:
            print(self.result)
            print(c)
            print(d)

        return datetime.datetime(**d)

    def parse_string(self, s):
        """
        Parse string yg diinput.
        Parse menjadi bagian-bagian perkata.
        """
        if self.debug:
            print_log(s)
        return re.findall(self.regex_for_parse_input, s)

    def sanitize_regex_result(self, r):
        """
        Menjadikan hasil regex sesuai dengan type nya.
        """
        result = []
        for x in r.groups():
            try:
                v = x
                v = float(x)
                v = int(x)
            except:
                pass
            result.append(v)
        return result

    def parse_tzinfo(self, r):
        """
        Parse timezone berdasarkan tzname atau utcoffset.
        Diutamakan untuk analisa menggunakan utcoffset.
        Apabila utcoffset tidak tersedia, maka gunakan tzname.
        """
        tzinfo = None

        if r[3]:
            # Analisa utcoffset
            tzinfo = self.tzinfo_from_timedelta(
                sign=r[2],
                hours=r[3],
                minutes=r[4],
                seconds=r[5],
                microseconds=r[6],
            )
        elif r[0] or r[1]:
            # Analisa tzname
            tzinfo = self.tzinfo_from_tzname(r[1] or r[0])

        return {"tzinfo": tzinfo}

    def tzinfo_from_timedelta(self, sign, hours, minutes, seconds, microseconds):
        time_delta = {
            "hours": hours,
            "minutes": minutes,
            "seconds": seconds,
            "microseconds": microseconds,
        }
        td = {i: v for i, v in time_delta.items() if v is not None}
        tds = datetime.timedelta(**td)
        if sign == "-":
            return datetime.timezone(-tds)
        return datetime.timezone(tds)

    def tzinfo_from_tzname(self, kota):
        kota = kota.lower()
        for v in iconstant.zoneinfo_available_timezones:
            for i in v:
                if i.lower() == kota:
                    return zoneinfo.ZoneInfo("/".join(v))
        return None

    def parse_datetime(self, r):
        print_colorize(r)
        return None

    def parse_date(self, r):
        year = r[0] or r[4]
        month = r[1] or r[3]
        day = r[2]

        c = len([x for x in [year, month, day] if x is not None])
        if c > 1:
            return (
                self.parse_year([year])
                | self.parse_month([month])
                | self.parse_day([day])
            )
        return None

    def parse_time(self, r):
        hour = r[0] or r[1]
        minute = r[2]
        second = r[3]
        microsecond = r[4]

        c = len([x for x in [hour, minute, second, microsecond] if x is not None])
        if c > 1:
            return {
                "hour": hour,
                "minute": minute,
                "second": second,
                "microsecond": microsecond,
            }
        return None

    def parse_year(self, r):
        return {"year": r[0]}

    def parse_month(self, r):
        month = r[0]
        if type(month) is str:
            month_str = month.lower()
            for i, v in enumerate(iconstant.months, 1):
                if v.startswith(month_str):
                    month = i
        return {"month": month}

    def parse_day(self, r):
        return {"day": r[0]}

    def parse_hour(self, r):
        return {"hour": r[0]}

    def parse_minute(self, r):
        return {"minute": r[0]}

    def parse_second(self, r):
        return {"second": r[0]}

    def parse_microsecond(self, r):
        return {"microsecond": r[0]}


def print_colorize(
    text,
    color=colorama.Fore.GREEN,
    bright=colorama.Style.BRIGHT,
    color_end=colorama.Style.RESET_ALL,
    text_start="",
    text_end="\n",
):
    """Print text dengan warna untuk menunjukan text penting"""
    print(f"{text_start}{color + bright}{text}{color_end}", end=text_end, flush=True)


def log(text):
    """
    Melakukan print ke console untuk menginformasikan proses yg sedang berjalan didalam program.
    """

    def inner_log(func):
        def callable_func(*args, **kwargs):
            print_log(text)
            result = func(*args, **kwargs)
            return result

        return callable_func

    return inner_log


def print_log(text):
    print_colorize(f">>> {text}")


def console_run(command):
    """Menjalankan command seperti menjalankan command di Command Terminal"""
    return subprocess.run(command, shell=True)


def input_char(prompt=None, prompt_ending="", newline_after_input=True):
    """Meminta masukan satu huruf tanpa menekan Enter. Masukan tidak ditampilkan."""
    if prompt:
        print(prompt, end=prompt_ending, flush=True)
    g = _getch.getch()
    if newline_after_input:
        print()
    return g


def input_char_echo(prompt=None, prompt_ending="", newline_after_input=True):
    """Meminta masukan satu huruf tanpa menekan Enter. Masukan akan ditampilkan."""
    if prompt:
        print(prompt, end=prompt_ending, flush=True)
    g = _getch.getche()
    if newline_after_input:
        print()
    return g


def datetime_now(timezone=None):
    """
    Datetime pada timezone tertentu
    """
    if timezone:
        return datetime.datetime.now(zoneinfo.ZoneInfo(timezone))
    else:
        return datetime.datetime.now()


def sets_ordered(iterator):
    """
    Hanya mengambil nilai unik dari suatu list
    """
    r = {i: {} for i in iterator}
    for i, v in r.items():
        yield i


def list_unique(iterator):
    """Sama seperti sets_ordered()"""
    return sets_ordered(iterator)


def chunck_array(array, size, start=0):
    """
    Membagi array menjadi potongan-potongan sebesar size
    """
    for i in range(start, len(array), size):
        yield array[i : i + size]


def regex_multiple_replace(data, regex_replacement_list, flags=0):
    """
    Melakukan multiple replacement untuk setiap list.

    regex_replacement_list = [
        {"regex":r"", "replacement":""},
        {"regex":r"", "replacement":""},
        {"regex":r"", "replacement":""},
    ]
    """
    for v in regex_replacement_list:
        data = re.sub(v["regex"], v["replacement"], data, flags=flags)
    return data


def github_push(commit=None):
    def console(t, c):
        print_log(t)
        console_run(c)

    def console_input(prompt, default):
        print_colorize(prompt, text_end="")
        if default:
            print(default)
            return default
        else:
            return input()

    print_log("Menjalankan Github Push")
    console("Checking files", "git status")
    msg = console_input("Commit Message if any or empty to exit : ", commit)
    if msg:
        console("Mempersiapkan files", "git add .")
        console("Menyimpan files", f'git commit -m "{msg}"')
        console("Mengirim files", "git push")
    print_log("Selesai Menjalankan Github Push")


def github_pull():
    print_log("Git Pull")
    console_run("git pull")


def file_get_contents(filename):
    """
    Membaca seluruh isi file ke memory.
    Apabila file tidak ada maka akan return None.
    Apabila file ada tetapi kosong, maka akan return empty string
    """
    try:
        f = open(filename, "r")
        r = f.read()
        f.close()
        return r
    except:
        return None


def file_put_contents(filename, contents):
    """
    Menuliskan content ke file.
    Apabila file tidak ada maka file akan dibuat.
    Apabila file sudah memiliki content maka akan di overwrite.
    """
    f = open(filename, "w")
    r = f.write(contents)
    f.close()
    return r


def write_file(filename, contents):
    """
    Sama seperti file_put_contents()
    """
    return file_put_contents(filename, str(contents))


def read_file(filename):
    """
    Sama seperti file_get_contents()
    """
    return file_get_contents(filename)


def create_folder(folder_name):
    """
    Membuat folder.
    Membuat folder secara recursive dengan permission.
    """
    pathlib.Path(folder_name).mkdir(parents=True, exist_ok=True)


def iscandir(folder_name=".", glob_pattern="*", recursive=True):
    """
    Mempermudah scandir untuk mengumpulkan folder, subfolder dan file
    """
    if recursive:
        return pathlib.Path(folder_name).rglob(glob_pattern)
    else:
        return pathlib.Path(folder_name).glob(glob_pattern)


def scan_folder(folder_name="", glob_pattern="*", recursive=True):
    """
    Hanya mengumpulkan nama-nama folder dan subfolder.
    Tidak termasuk [".", ".."].
    """
    p = iscandir(
        folder_name=folder_name,
        glob_pattern=glob_pattern,
        recursive=recursive,
    )
    for i in p:
        if i.is_dir():
            yield i


def scan_file(folder_name="", glob_pattern="*", recursive=True):
    """
    Hanya mengumpulkan nama-nama file dalam folder dan subfolder.
    """
    p = iscandir(
        folder_name=folder_name,
        glob_pattern=glob_pattern,
        recursive=recursive,
    )
    for i in p:
        if i.is_file():
            yield i


def html_get_contents(url, xpath=None, regex=None, css_select=None):
    """
    Mengambil content html dari url.

    Return :
    - String            : Apabila hanya url saja yg diberikan
    - List of etree     : Apabila xpath diberikan
    - False             : Apabila terjadi error
    """
    url_req = urllib.request.Request(
        url=url,
        headers={
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36"
        },
    )
    url_open = urllib.request.urlopen(url_req)
    try:
        if xpath:
            return lxml.html.parse(url_open).findall(xpath)
        if regex:
            return re.findall(regex, url_open.read().decode())
        if css_select:
            return lxml.html.parse(url_open).getroot().cssselect(css_select)
        return url_open.read().decode()
    except:
        return False


def url_get_contents(url, xpath=None, regex=None, css_select=None):
    """
    Sama seperti html_get_contents()
    """
    return html_get_contents(url, xpath, regex, css_select)


def get_filesize(filename):
    """
    Mengambil informasi file size dalam bytes
    """
    return pathlib.Path(filename).stat().st_size


def get_filemtime(filename):
    """
    Mengambil informasi file size dalam bytes
    """
    return pathlib.Path(filename).stat().st_mtime_ns


def datetime_from_string(*args, **kwargs):
    return idatetime(*args, **kwargs).to_datetime()


def dict_first(d: dict) -> tuple:
    """
    Mengambil nilai (key, value) pertama dari dictionary dalam bentuk tuple
    """
    for k, v in d.items():
        return (k, v)


def random_bool() -> bool:
    """
    Menghasilkan nilai random antara 1 atau 0.
    fungsi ini merupkan fungsi tercepat untuk mendapatkan random bool value
    """
    return random.getrandbits(1)
