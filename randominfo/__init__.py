from __future__ import unicode_literals
from random import randint, choice, sample, randrange
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from math import ceil
import sys, glob, csv, pytz, shutil
from os import access, W_OK
from os.path import abspath, join, dirname, split

sys.path.append("/randominfo/")

__title__ = 'randominfo'
__version__ = '2.0.2'
__author__ = 'Bhuvan Gandhi'
__license__ = 'MIT'

full_path = lambda filename: abspath(join(dirname(__file__), filename))


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
    elif postfix is not None:
        generated_id += postfix
    return generated_id


def get_first_name(gender=None):
    file = csv.reader(open(full_path('data.csv'), 'r'))

    # Create list with existing 'name' and 'gender' in data.csv
    filtered_data = []
    for data in file:
        if data[0] and data[2] != '':
            filtered_data.append(data)

    if gender is None:
        return choice(filtered_data)[0]

    elif gender.lower() == "male":
        male_names = [data[0] for data in filtered_data if data[2] == 'male']
        return choice(male_names)

    elif gender.lower() == "female":
        female_names = [data[0] for data in filtered_data if data[2] == 'female']
        return choice(female_names)

    else:
        raise ValueError("Enter gender male or female.")


def get_last_name():
    file = csv.reader(open(full_path('data.csv'), 'r'))
    last_names = [data[1] for data in file if data[1] != '']
    return choice(last_names)


def get_gender(first_name):
    file = csv.reader(open(full_path('data.csv'), 'r'))
    for data in file:
        if first_name in data[0]:
            gender = data[2]
            return gender


def get_city(first_name=None):
    file = csv.reader(open(full_path('data.csv'), 'r'))
    city = ""
    if first_name is not None:
        for data in file:
            if data[0] == first_name:
                city = data[7]
                if city == "":
                    print("Specified user data is not available. Tip: Generate random city.")
                    break
    else:
        filtered_cities = []
        for data in file:
            if data[0] != '':
                filtered_cities.append(data[7])
                print(filtered_cities)
        city = choice(filtered_cities)
    return city


def get_full_name(gender=None):
    return get_first_name(gender) + " " + get_last_name()


def get_otp(length=6, digit=True, alpha=True, lowercase=True, uppercase=True):
    lwr_chars = "qwertyuioplkjhgfdsazxcvbnm"
    upr_chars = "QWERTYUIOPLKJHGFDSAZXCVBNM"
    digs = "0123456789"
    chars = ""
    otp = ""
    if digit or alpha:
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


def get_email(prsn=None):
    domains = ["gmail", "yahoo", "hotmail", "express", "yandex", "nexus", "online", "omega", "institute", "finance",
               "company", "corporation", "community"]
    extentions = ['com', 'in', 'jp', 'us', 'uk', 'org', 'edu', 'au', 'de', 'co', 'me', 'biz', 'dev', 'ngo', 'site',
                  'xyz', 'zero', 'tech']

    if prsn is None:
        prsn = Person()

    c = randint(0, 2)
    dmn = '@' + choice(domains)
    ext = choice(extentions)

    if c == 0:
        email = prsn.first_name + get_formatted_datetime("%Y", prsn.birthdate, "%d %b, %Y") + dmn + "." + ext
    elif c == 1:
        email = prsn.last_name + get_formatted_datetime("%d", prsn.birthdate, "%d %b, %Y") + dmn + "." + ext
    else:
        email = prsn.first_name + get_formatted_datetime("%y", prsn.birthdate, "%d %b, %Y") + dmn + "." + ext
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
            "Invalid image name. Image name must contains characher including digits, alphabets, white space, dot, comma, ( ) [ ] { } _ + - =.")
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
            "Invalid image name. Image name must contains characher including digits, alphabets, white space, dot, comma, ( ) [ ] { } _ + - =.")


startRange = datetime(1970, 1, 1, 0, 0, 0, 0, pytz.UTC)
endRange = datetime.today()


def get_today(_format="%d-%m-%Y %H:%M:%S"):
    return datetime.today().strftime(_format)


def get_date(tstamp=None, _format="%d %b, %Y"):
    if tstamp is None:
        start_ts = startRange.timestamp()
        end_ts = datetime.timestamp(endRange)
        tstamp = randrange(int(start_ts), int(end_ts))
    else:
        if type(tstamp).__name__ != 'int':
            raise ValueError("Timestamp must be an integer.")
    return datetime.utcfromtimestamp(tstamp).strftime(_format)


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
    full_addr = []
    addr_param = ['street', 'landmark', 'area', 'city', 'state', 'pincode']
    for i in range(4, 10):
        file = csv.reader(open(full_path('data.csv'), 'r'))
        all_addrs = []
        for addr in file:
            try:
                if addr[i] != '':
                    all_addrs.append(addr[i])
            except:
                IndexError("Address not found")
        full_addr.append(choice(all_addrs))
    full_addr = dict(zip(addr_param, full_addr))
    return full_addr


def get_hobbies():
    file = csv.reader(open(full_path('data.csv'), 'r'))
    all_hobbies = []
    for data in file:
        if data[3] != '':
            all_hobbies.append(data[3])
    hobbies = []
    for _ in range(1, randint(2, 6)):
        hobbies.append(choice(all_hobbies))

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
        self.city = get_city(first_name)
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
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "birthdate": self.birthdate,
            "gender": self.gender,
            "email": self.email,
            "phone": self.phone,
            "password": self.password,
            "city": self.city,
            "hobbies": self.hobbies,
            "address": self.address,
            "other_attr": self.customAttr
        }


person = Person()
print(person.full_name, person.gender, person.address)

'''
REFERENCE:
http://www.first-names-meanings.com/country-indian-names.html
https://www.familyeducation.com/baby-names/browse-origin/surname/indian
https://thispersondoesnotexist.com/
https://en.wikipedia.org/wiki/List_of_hobbies
'''
