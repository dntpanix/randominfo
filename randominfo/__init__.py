from __future__ import unicode_literals

import csv
import glob
import shutil
import pytz
import sys

from datetime import datetime, timezone
from math import ceil
from os import access, W_OK
from os.path import abspath, join, dirname, split
from PIL import Image, ImageDraw, ImageFont
from random import randint, choice, sample, randrange

sys.path.append("/randominfo/")
__title__ = 'randominfo'
__version__ = '2.0.2'
__author__ = 'Bhuvan Gandhi'
__license__ = 'MIT'


def get_absolute_path(filename):
    return abspath(join(dirname(__file__), filename))


csv_file_path = get_absolute_path('data.csv')


def get_id(length=6, seq_number=None, step=1, prefix=None, postfix=None):
    generated_id = ""
    if seq_number is None:
        for _ in range(length):
            generated_id += str(randint(0, 9))
    else:
        if type(seq_number).__name__ != 'int' or type(step).__name__ != 'int':
            raise TypeError("Sequence number must be an integer.")
        else:
            generated_id = str(seq_number + step)

    if prefix is not None:
        prefix += generated_id
        generated_id = prefix

    if postfix is not None:
        generated_id += postfix

    return generated_id


def get_first_name(gender=None):
    filtered_data = []

    with open(csv_file_path, 'r') as first_name_file:
        csv_reader = csv.reader(first_name_file)
        if gender is None:
            for data in csv_reader:
                if data[0] != '':
                    filtered_data.append(data)
        else:
            if gender.lower() == "male":
                for data in csv_reader:
                    if data[0] != '':
                        if data[2] == "male":
                            filtered_data.append(data)
            elif gender.lower() == "female":
                for data in csv_reader:
                    if data[0] != '':
                        if data[2] == "female":
                            filtered_data.append(data)
            else:
                raise ValueError("Enter gender male or female.")
    return choice(filtered_data)[0]


def get_last_name():
    filtered_data = []

    with open(csv_file_path, 'r') as last_name_file:
        csv_reader = csv.reader(last_name_file)

        for data in csv_reader:
            if data[1] != '':
                filtered_data.append(data[1])

    return choice(filtered_data)


def get_gender(first_name):
    gender = ""
    with open(csv_file_path, 'r') as first_name_file:
        csv_reader = csv.reader(first_name_file)
        for data in csv_reader:
            if data[0] != '' and data[0] == first_name:
                gender = data[2]
                break
    return gender


def get_country(first_name=None):
    country = ""
    with open(csv_file_path, 'r') as country_file:
        csv_reader = csv.reader(country_file)
        if first_name is not None:
            for data in csv_reader:
                if data[0] != '' and data[0] == first_name:
                    filtered_data = data[8]
                    country = ''.join(['India, ', str(filtered_data)])
                    break
            if country == "":
                print("Specified user data is not available. Tip: Generate random country.")
        else:
            filtered_data = []
            for data in csv_reader:
                if data[8] != '':
                    filtered_data.append(data[8])
            country = 'India, ' + choice(filtered_data)
    return country


def get_full_name(gender=None):
    return get_first_name(gender) + " " + get_last_name()


def get_otp(length=6, digit=True, alpha=True, lowercase=True, uppercase=True):
    lwr_chars = "qwertyuioplkjhgfdsazxcvbnm"
    upr_chars = "QWERTYUIOPLKJHGFDSAZXCVBNM"
    digs = "0123456789"
    chars = ""
    otp = ""
    if digit is not False or alpha is not False:
        if digit:
            chars += digs
        if alpha:
            if lowercase:
                chars += lwr_chars
            if uppercase:
                chars += upr_chars
        for _ in range(length):
            otp += str(chars[randint(0, len(chars) - 1)])
        return otp
    else:
        raise ValueError("From parameters 'digit' and 'alpha' anyone must be True.")


def get_formatted_datetime(out_format, str_date, str_format="%d-%m-%Y %H:%M:%S"):
    return datetime.strptime(str_date, str_format).strftime(out_format)


def get_email(pers=None):
    domains = ["gmail", "yahoo", "hotmail", "express", "yandex", "nexus", "online", "omega", "institute", "finance",
               "company", "corporation", "community"]
    extensions = ['com', 'in', 'jp', 'us', 'uk', 'org', 'edu', 'au', 'de', 'co', 'me', 'biz', 'dev', 'ngo', 'site',
                  'xyz', 'zero', 'tech']

    if pers is None:
        pers = Person()

    c = randint(0, 2)
    dmn = '@' + choice(domains)
    ext = choice(extensions)

    if c == 0:
        email = pers.first_name + get_formatted_datetime("%Y", pers.birthdate, "%d %b, %Y") + dmn + "." + ext
    elif c == 1:
        email = pers.last_name + get_formatted_datetime("%d", pers.birthdate, "%d %b, %Y") + dmn + "." + ext
    else:
        email = pers.first_name + get_formatted_datetime("%y", pers.birthdate, "%d %b, %Y") + dmn + "." + ext
    return email


def random_password(length=8, special_chars=True, digits=True):
    spec_chars = ['!', '@', '#', '$', '%', '^', '&', '*']
    alpha = "QWERTYUIOPLKJHGFDSAZXCVBNMmnbvcxzasdfghjklpoiuytrewq"
    spec_char_len = dig_char_len = 0
    chars = ""

    if special_chars:
        spec_char_len = randint(1, ceil(length / 4))
        for _ in range(spec_char_len):
            chars += choice(spec_chars)
    if digits:
        dig_char_len = randint(1, ceil(length / 3))
        for _ in range(dig_char_len):
            chars += str(randint(0, 9))
    for _ in range(length - (dig_char_len + spec_char_len)):
        chars += choice(alpha[randint(0, len(alpha) - 1)])

    password = ''.join(sample(chars, len(chars)))
    return password


def get_phone_number(country_code=True):
    phone = ""
    if country_code:
        c_codes = [91, 144, 141, 1, 44, 86, 52, 61, 32, 20, 33, 62, 81, 31, 7]
        phone = "+"
        phone += str(choice(c_codes))
        phone += " "
    for i in range(0, 10):
        if i == 0:
            phone += str(randint(6, 9))
        else:
            phone += str(randint(0, 9))
    return phone


def get_alphabetic_profile_img(char, file_path, img_name, char_color=None, bg_color=None):
    chars = "qwertyuioplkjhgfdsazxcvbnmQAZXSWEDCVFRTGBNHYUJMKLIOP0123456789 ,.+=-_()[]{}"
    if all((c in chars) for c in img_name):
        if access(dirname(file_path), W_OK):
            if char_color is not None:
                if not char_color.isalpha():
                    raise ValueError("Character color must be a name of color.")
            if bg_color is not None:
                if not bg_color.isalpha():
                    raise ValueError("Background color must be a name of color.")
            char = char[:1].upper()
            if bg_color is None:
                colors = ['red', 'green', 'royalblue', 'violet', 'pink', 'indigo', 'grey', 'yellowgreen', 'teal']
                bg_color = choice(colors)
            if char_color is None:
                char_color = (40, 40, 40)
            img = Image.new('RGB', (512, 512), color=bg_color)
            d = ImageDraw.Draw(img)
            font = ImageFont.truetype("Candara.ttf", 280)
            d.text((170, 140), char, fill=char_color, font=font)
            file_path = file_path + "\\" + str(img_name) + ".jpg"
            img.save(file_path)
        else:
            raise OSError("Invalid or insufficient privileges for specified file path.")
    else:
        raise OSError(
            "Invalid image name. Image name must contains character including digits, alphabets, white space, dot, "
            "comma, ( ) [ ] { } _ + - =.")
    return file_path


def get_face_profile_img(file_path, img_name, gender=None):
    dir_name, file_name = split(abspath(__file__))
    chars = "qwertyuioplkjhgfdsazxcvbnmQAZXSWEDCVFRTGBNHYUJMKLIOP0123456789 ,.+=-_()[]{}"
    if all((c in chars) for c in img_name):
        if access(dirname(file_path), W_OK):
            if gender is None:
                orig_file = choice(glob.glob(dir_name + "\\images\\people\\*.jpg"))
            elif gender.lower() == "female":
                orig_file = choice(glob.glob(dir_name + "\\images\\people\\female_*.jpg"))
            elif gender.lower() == "male":
                orig_file = choice(glob.glob(dir_name + "\\images\\people\\male_*.jpg"))
            else:
                return ValueError("Invalid gender. It must be male or female.")
            return shutil.copy(orig_file, file_path + "\\" + str(img_name) + ".jpg")
        else:
            raise OSError("Invalid or insufficient privileges for specified file path.")
    else:
        raise OSError(
            "Invalid image name. Image name must contains character including digits, alphabets, white space, dot, "
            "comma, ( ) [ ] { } _ + - =.")


startRange = datetime(1970, 1, 1, 0, 0, 0, 0, pytz.UTC)
endRange = datetime.today()


def get_today(_format="%d-%m-%Y %H:%M:%S"):
    return datetime.today().strftime(_format)


def get_date(tstamp=None, _format="%d/%m/%Y"):
    if tstamp is None:
        start_ts = startRange.timestamp()
        end_ts = datetime.timestamp(endRange)
        tstamp = randrange(int(start_ts), int(end_ts))
    else:
        if type(tstamp).__name__ != 'int':
            raise ValueError("Timestamp must be an integer.")
    return datetime.fromtimestamp(tstamp, timezone.utc).strftime(_format)


def get_birthdate(start_age=None, end_age=None, _format="%d %b, %Y"):
    start_range = datetime.today()
    end_range = datetime(1970, 1, 1, 0, 0, 0, 0, pytz.UTC)
    if start_age is not None:
        if type(start_age).__name__ != 'int':
            raise ValueError("Starting age value must be integer.")
    if end_age is not None:
        if type(end_age).__name__ != 'int':
            raise ValueError("Ending age value must be integer.")
    if start_age is not None and end_age is not None:  # If both are given in arg
        if start_age >= end_age:
            raise ValueError("Starting age must be less than ending age.")
        else:
            start_range = datetime(datetime.now().year - start_age, 12, 31, 23, 59, 59, 0, pytz.UTC)
            end_range = datetime(datetime.now().year - end_age, 1, 1, 0, 0, 0, 0, pytz.UTC)
    elif start_age is not None or end_age is not None:  # If anyone is given in arg
        age_year = start_age if start_age is not None else end_age
        start_range = datetime(datetime.now().year - age_year, 12, 31, 23, 59, 59, 0, pytz.UTC)
        end_range = datetime(datetime.now().year - age_year, 1, 1, 0, 0, 0, 0, pytz.UTC)
    else:
        pass
    start_ts = start_range.timestamp()
    end_ts = end_range.timestamp()
    return datetime.fromtimestamp(randrange(int(end_ts), int(start_ts))).strftime(_format)


def get_address():
    addr_param = ['street address', 'landmark', 'area', 'city', 'state', 'pincode']

    with open(csv_file_path, 'r') as addr_file:
        csv_reader = csv.reader(addr_file)
        next(csv_reader)

        valid_rows = [row for row in csv_reader if all(item != '' for item in row[4:])]

        if valid_rows:
            selected_address = choice(valid_rows)
            full_addr = dict(zip(addr_param, selected_address[4:]))
            return full_addr
        else:
            return get_address()


def get_hobbies():
    all_hobbies = []

    with open(csv_file_path, 'r') as hobbies_file:
        csv_reader = csv.reader(hobbies_file)
        for data in csv_reader:
            if data[4] != '':
                all_hobbies.append(data[3])
    hobbies = [choice(all_hobbies) for _ in range(randint(2, 6))]
    return hobbies


class Person:
    def __init__(self, gender=None):
        first_name = get_first_name(gender)
        self.first_name = first_name
        self.last_name = get_last_name()
        self.full_name = self.first_name + " " + self.last_name
        self.birthdate = get_birthdate()
        self.phone = get_phone_number()
        self.email = get_email(self)
        self.gender = get_gender(first_name)
        self.country = get_country(first_name)
        self.password = random_password()
        self.hobbies = get_hobbies()
        self.address = get_address()
        self.customAttr = {}

    def set_attr(self, attr_name, value=None):
        if attr_name.isalnum():
            if attr_name[0].isalpha():
                self.customAttr[attr_name] = value
                print("Attribute '" + str(attr_name) + "' added.")
            else:
                raise ValueError("First character of attribute must be an alphabet.")
        else:
            raise ValueError("Attribute name only contains alphabets and digits.")

    def get_attr(self, attr_name):
        if attr_name.isalnum():
            if attr_name[0].isalpha():
                if attr_name in self.customAttr.keys():
                    return self.customAttr[attr_name]
                else:
                    raise AttributeError("Specified attribute is not exists.")
            else:
                raise ValueError("First character of attribute must be an alphabet.")
        else:
            raise ValueError("Attribute name only contains alphabets and digits.")

    def get_details(self):
        result = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "birthdate": self.birthdate,
            "gender": self.gender,
            "email": self.email,
            "phone": self.phone,
            "password": self.password,
            "country": self.country,
            "hobbies": self.hobbies,
            "address": self.address,
        }
        if self.customAttr:
            result["other_attr"] = self.customAttr
        return result


'''
REFERENCE:
http://www.first-names-meanings.com/country-indian-names.html
https://www.familyeducation.com/baby-names/browse-origin/surname/indian
https://thispersondoesnotexist.com/
https://en.wikipedia.org/wiki/List_of_hobbies
'''

if __name__ == '__main__':

    print(get_id())  # 969650
    print(get_first_name())  # Mukta
    print(get_last_name())  # Amble
    print(get_gender('Nilam'))  # female
    print(get_country())  # India, Uttar Pradesh
    print(get_full_name())  # Abhilasha Khare
    print(get_otp())  # yoZ52u
    print(get_email())  # Minali2014@express.xyz
    print(random_password())  # 6t&RLIs6
    print(get_phone_number())  # +20 8227855907
    print(get_today())  # 23-01-2024 19:55:29
    print(get_date())  # 05/06/1974
    print(get_birthdate())  # 29 Nov, 1979
    print(get_address())
    # {'street address': 'Ap #376-4538 Nam St.', 'landmark': 'After Highfield', 'area': 'Chintarlapalli',
    # 'city': 'ANANTHAPUR', 'state': 'Andhra Pradesh', 'pincode': '515767'}

    print(get_hobbies())  # ['Magic', 'Lego building', 'Do it yourself', 'Karaoke']
    print(get_formatted_datetime('%H:%M:%S %d-%m-%Y', '22-01-2024 15:55:51'))  # 15:55:51 22-01-2024

    person = Person()
    print(person.get_details())
    # {'first_name': 'Kiran', 'last_name': 'Kuruvilla', 'full_name': 'Kiran Kuruvilla', 'birthdate': '20 May, 1985',
    # 'gender': 'female', 'email': 'Kiran1985@nexus.tech', 'phone': '+33 6459149125', 'password': '1kU64Li*',
    # 'country': 'India, Andhra Pradesh', 'hobbies': ['Craft', 'Needlepoint', 'Fantasy sports', 'Fashion',
    # 'Lapidary', 'Homebrewing'], 'address': {'street address': '3770 Ut Rd.', 'landmark': 'After Goldwilde',
    # 'area': 'Basinepalli', 'city': 'ANANTHAPUR', 'state': 'Andhra Pradesh', 'pincode': '515402'}}

    person.set_attr('test', '123')  # Attribute 'test' added.
    print(person.get_details())
    # {'first_name': 'Kiran', 'last_name': 'Kuruvilla', 'full_name': 'Kiran Kuruvilla', 'birthdate': '20 May, 1985',
    # 'gender': 'female', 'email': 'Kiran1985@nexus.tech', 'phone': '+33 6459149125', 'password': '1kU64Li*',
    # 'country': 'India, Andhra Pradesh', 'hobbies': ['Craft', 'Needlepoint', 'Fantasy sports', 'Fashion',
    # 'Lapidary', 'Homebrewing'], 'address': {'street address': '3770 Ut Rd.', 'landmark': 'After Goldwilde',
    # 'area': 'Basinepalli', 'city': 'ANANTHAPUR', 'state': 'Andhra Pradesh', 'pincode': '515402'}, 'other_attr': {
    # 'test': '123'}}

    print(person.get_attr('test'))  # 123
