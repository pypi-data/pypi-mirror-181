from climatereport_zillow.extract_address import make_address, make_zipcode, make_state
from climatereport_zillow.google_result import google_result
from climatereport_zillow.link_tests import site_in_link, address_in_link
from climatereport_zillow.make_dataframes import create_file_zip, create_file_state
from climatereport_zillow.make_plots import make_plot_zip, make_plot_state
from climatereport_zillow.html_style import make_html_style
from climatereport_zillow.html_css import make_html_css
from climatereport_zillow.create_html import write_html
from climatereport_zillow import heat_zip_file, heat_state_file, fire_zip_file, fire_state_file, flood_zip_file, flood_state_file


def climatereport_zillow(zillow_url):
    """
    Creates a report on the climate risk of a property from a Zillow listing.

    Parameters
    ----------
    zillow_url : string
      A string representation of the url of the zillow listing.

    Returns
    ----------
    html
        The new climate risk report in the form of an HTML document.

    Examples
    ----------
    >>> from climatereport_zillow import climatereport_zillow
    >>> #climatereport_zillow.climatereport_zillow("https://www.zillow.com/homedetails/110-Legacy-Trace-Dr-Huntsville-AL-35806/109397143_zpid/")
    "The report zipcode_risk.html will automatically open."
    """

    url = str(zillow_url)
    url = url.split('homedetails/')
    url = url[1]

    zip_code = make_zipcode(url)
    state = make_state(url)
    address = make_address(url, zip_code)


    # Generate ClimateCheck url
    climate_url = "https://climatecheck.com/report?address=" + address.replace(" ","%20")

    # Search for redfin and realtor listings
    realtor_link = google_result(address, "realtor")
    redfin_link = google_result(address, "redfin")

    #Check links
    if not realtor_link == "Could not check for results at this time.":
        realtor_link = address_in_link(address, realtor_link)
        realtor_link = site_in_link("realtor",realtor_link)

    if not redfin_link == "Could not check for results at this time.":
        redfin_link = address_in_link(address, redfin_link)
        redfin_link = site_in_link("redfin", redfin_link)


    #Create data files
    fire_zip = create_file_zip("fire",fire_zip_file)
    flood_zip = create_file_zip("flood",flood_zip_file)
    heat_zip = create_file_zip("heat",heat_zip_file)
    fire_state = create_file_state("fire",fire_state_file)
    flood_state = create_file_state("flood",flood_state_file)
    heat_state = create_file_state("heat",heat_state_file)

    # Make Plots and HTML
    html_style = make_html_style()
    html_css = make_html_css()
    plot_zip = make_plot_zip(zip_code,heat_zip, flood_zip,fire_zip)
    plot_state = make_plot_state(state,heat_state, flood_state,fire_state)

    write_html(zip_code,html_css,html_style,heat_zip,flood_zip,fire_zip,realtor_link, climate_url, redfin_link,address,plot_zip, plot_state)
    print("The report zipcode_risk.html will automatically open.")

