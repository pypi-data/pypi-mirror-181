import re

def address_in_link(address,link):
    check_address = re.search('(^\w+)', address)
    check_address = check_address[0]
    test = re.search(check_address, link)
    if test == None:
        link = "Link to address not found in first result."
    return link

def site_in_link(site,link):
    test = re.search(site, link)
    if test == None:
        link = "Link to address not found in first result."
    return link