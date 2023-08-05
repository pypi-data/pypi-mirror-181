import os

def write_html(zipcode,html_css,html_style,heat_zip,flood_zip,fire_zip,realtor_link, climate_url, redfin_link,address,plot_zip, plot_state):
        f = open('zipcode_risk.html', 'w')
        f.write(html_style.format(css=html_css,
                                  zipcode=zipcode,
                                  minimal_heat=heat_zip.loc[zipcode, "minimal"],
                                  minor_heat=heat_zip.loc[zipcode, "minor"],
                                  major_heat=heat_zip.loc[zipcode, "major"],
                                  severe_heat=heat_zip.loc[zipcode, "severe"],
                                  extreme_heat=heat_zip.loc[zipcode, "extreme"],
                                  minimal_heat_percent=heat_zip.loc[zipcode, "minimal_p"],
                                  minor_heat_percent=heat_zip.loc[zipcode, "minor_p"],
                                  major_heat_percent=heat_zip.loc[zipcode, "major_p"],
                                  severe_heat_percent=heat_zip.loc[zipcode, "severe_p"],
                                  extreme_heat_percent=heat_zip.loc[zipcode, "extreme_p"],
                                  minimal_fire=fire_zip.loc[zipcode, "minimal"],
                                  minor_fire=fire_zip.loc[zipcode, "minor"],
                                  major_fire=fire_zip.loc[zipcode, "major"],
                                  severe_fire=fire_zip.loc[zipcode, "severe"],
                                  extreme_fire=fire_zip.loc[zipcode, "extreme"],
                                  minimal_fire_percent=fire_zip.loc[zipcode, "minimal_p"],
                                  minor_fire_percent=fire_zip.loc[zipcode, "minor_p"],
                                  major_fire_percent=fire_zip.loc[zipcode, "major_p"],
                                  severe_fire_percent=fire_zip.loc[zipcode, "severe_p"],
                                  extreme_fire_percent=fire_zip.loc[zipcode, "extreme_p"],
                                  minimal_flood=flood_zip.loc[zipcode, "minimal"],
                                  minor_flood=flood_zip.loc[zipcode, "minor"],
                                  major_flood=flood_zip.loc[zipcode, "major"],
                                  severe_flood=flood_zip.loc[zipcode, "severe"],
                                  extreme_flood=flood_zip.loc[zipcode, "extreme"],
                                  minimal_flood_percent=flood_zip.loc[zipcode, "minimal_p"],
                                  minor_flood_percent=flood_zip.loc[zipcode, "minor_p"],
                                  major_flood_percent=flood_zip.loc[zipcode, "major_p"],
                                  severe_flood_percent=flood_zip.loc[zipcode, "severe_p"],
                                  extreme_flood_percent=flood_zip.loc[zipcode, "extreme_p"],
                                  realtor_link=realtor_link,
                                  redfin_link=redfin_link,
                                  climate_url=climate_url,
                                  address=address,
                                  html_graph=plot_zip,
                                  html_graph2=plot_state
                                  ))

        f.close()
        os.system("open zipcode_risk.html")