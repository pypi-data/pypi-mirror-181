import bs4
import requests
import re

def google_result(search_address, site):
    """
    Searches google results for listings of an address on a specific website.

    Parameters
    ----------
    address : string
      A string representation of the address you want to search.

    site : string
      A string representation of the website you would like filter search results by.

    Returns
    ----------
    string
        A string result of a URL that matched your search parameters, or message that there were no results.

    Examples
    ----------
    >>> from climatereport_zillow import google_result
    >>> google_result("110 Legacy Trace Dr Huntsville AL 35806","realtor")
    "https://www.realtor.com/realestateandhomes-detail/110-Legacy-Trace-Dr_Huntsville_AL_35806_M75539-67014"
    """
    search_address = search_address.replace(" ", "+")
    query = search_address + "site:%3A" + site + ".com"
    url = 'https://google.com/search?q=' + query
    request_result=requests.get( url )
    soup = bs4.BeautifulSoup(request_result.text,
        "html.parser")
    if re.search("unusual traffic",str(soup)):
        result = "Could not check for results at this time."
    else:
        links = []
        for link in soup.find_all('a',class_='BVG0Nb'):
            links.append(link.get('href'))
        result = ""
        if links == []:
            result = "Link to address not found in first result."
        else:
            result = links[0].split("imgrefurl=")
            result = result[1]
            result = result.split("&h")
            result = result[0]
        if result == []:
            result = "Link to address not found in first result."
    return result
