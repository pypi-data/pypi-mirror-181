from .pypipr import *


""""""

Pypipr.test_print()

""""""

array = [2, 3, 12, 3, 3, 42, 42, 1, 43, 2, 42, 41, 4, 24, 32, 42, 3, 12, 32, 42, 42]
print([i for i in sets_ordered(array)])

""""""

array = [2, 3, 12, 3, 3, 42, 42, 1, 43, 2, 42, 41, 4, 24, 32, 42, 3, 12, 32, 42, 42]
print([i for i in list_unique(array)])

""""""

array = [2, 3, 12, 3, 3, 42, 42, 1, 43, 2, 42, 41, 4, 24, 32, 42, 3, 12, 32, 42, 42]
print([i for i in chunck_array(array, 5)])

""""""

print_colorize("Print Colorize")

""""""


@log("Percobaan print log decorator")
def contoh_fungsi():
    pass


contoh_fungsi()

""""""

print_log("Percobaan print log standalone")

""""""

console_run("ls")
console_run("dir")

""""""

input_char("Input Char tanpa ditampilkan : ")

""""""

input_char_echo("Input Char dengan ditampilkan : ")

""""""

print(f"Is Windows : {WINDOWS}")

""""""

print(f"Is Linux : {LINUX}")

""""""

d = datetime_now()
print(f"Time now                : {d}")
d_jakarta = datetime_now("Asia/Jakarta")
print(f"Timezone Asia/Jakarta   : {d_jakarta}")
d_gmt = datetime_now("GMT")
print(f"Timezone GMT            : {d_gmt}")
d_utc = datetime_now("UTC")
print(f"Timezone UTC            : {d_utc}")
d_universal = datetime_now("Universal")
print(f"Timezone Universal      : {d_universal}")
d_gmt7 = datetime_now("Etc/GMT+7")
print(f"Timezone Etc/GMT+7      : {d_gmt7}")

""""""

file_put_contents("ifile_test.txt", "Contoh menulis content")

""""""

print(file_get_contents("ifile_test.txt"))

""""""

create_folder("contoh_membuat_folder")
create_folder("contoh/membuat/folder/recursive")
create_folder("./contoh_membuat_folder/secara/recursive")

""""""

for i in iscandir(recursive=False):
    print(i)

""""""

for i in scan_folder():
    print(i)

""""""

for i in scan_file():
    print(i)

""""""

regex_replacement_list = [
    {"regex": r"\{\{\s*(ini)\s*\}\}", "replacement": r"itu dan \1"},
    {"regex": r"\{\{\s*sini\s*\}\}", "replacement": "situ"},
]
data = "{{ ini }} adalah ini. {{sini}} berarti kesini."
data = regex_multiple_replace(data, regex_replacement_list, re.IGNORECASE)
print(data)

""""""

# print(html_get_contents("https://google.com/"))
print(r := url_get_contents("https://google.com/"))
assert r != False

""""""

a = html_get_contents("https://animekompi.net/", xpath="//a")
for i in a:
    print(f"{i.text} : {i.attrib}")

""""""

a = html_get_contents(
    "https://animekompi.net/", regex=r"(<a.[^>]+>(?:(?:\s+)?(.[^<]+)(?:\s+)?)<\/a>)"
)
for i in a:
    print(i)

""""""

a = html_get_contents("https://animekompi.net/", css_select="a")
for i in a:
    print(f"{i.text} : {i.attrib}")

""""""

print(get_filesize(__file__))

""""""

print(get_filemtime(__file__))

""""""

print(datetime_from_string("13-10-1993"))
print(datetime_from_string("1-Jan-2001"))
print(datetime_from_string("5-5-5"))
print(datetime_from_string("12:56 31-10-2022"))
# print(datetime_from_string("12:56 PM 31-10-2022"))
# print(datetime_from_string("2022 13 10"))
print(datetime_from_string("11:59 Monday, October 31, 2022 (GMT+7)"))
print(datetime_from_string("oct 1"))
print(datetime_from_string("10:50"))
print(datetime_from_string("10:50:22"))
print(datetime_from_string("10:50", default_year=2022))
print(datetime_from_string("10:50", overwrite={"hour": 21}))
print(datetime_from_string("-056033"))
print(datetime_from_string("GMT+7"))
print(datetime_from_string("+0700"))
print(datetime_from_string("+112233"))
print(datetime_from_string("+112233445566"))
print(datetime_from_string("+7:07"))
print(datetime_from_string("Asia/Jakarta"))
print(datetime_from_string("Africa/Addis_Ababa"))
print(datetime_from_string("Etc/GMT"))
print(datetime_from_string("Etc/GMT-5"))
print(datetime_from_string("jakarta"))
print(datetime_from_string("asia"))
print(datetime_from_string("africa"))
print(datetime_from_string("europe/jakarta"))
print(datetime_from_string("2022-05-12T05:04:03+07:07:12"))
print(datetime_from_string("2022-05-12 05:04:03+07:07:12"))
print(datetime_from_string("2022-05-12 05:04:03 +07:07:12"))
print(datetime_from_string("05:04:03 2022-05-12 +07:07:12"))
print(datetime_from_string("05:04:03 12-05-2022 +07:07:12"))
print(datetime_from_string("Jakarta, 13-10-1993"))
print(datetime_from_string("Jakarta, 13 october 1993"))

""""""

d = {
    "key1": "value1",
    "key2": "value2",
    "key3": "value3",
}
print(dict_first(d))

""""""

print(random_bool())

""""""
