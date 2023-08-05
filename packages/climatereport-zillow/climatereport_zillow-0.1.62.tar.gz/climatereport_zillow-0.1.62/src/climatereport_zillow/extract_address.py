import re

def make_zipcode(url):
    zip_code = re.search('\D(-\D{2}-\d{5})', url)
    zip_code = zip_code[1]
    zip_code = zip_code.split('-')
    zip_code = zip_code[2]
    zip_code = int(zip_code)
    return zip_code

def make_state(url):
    zip_code = re.search('\D(-\D{2}-\d{5})', url)
    zip_code = zip_code[1]
    zip_code = zip_code.split('-')
    state = zip_code[1]
    return state


def make_address(url,zip):
    address = re.search('.+?(?=\D(\d{5})\D)', url)
    address = address[0]
    address = address.replace("-", " ")
    address = address + " " + str(zip)
    return address