# Format adapted from CodePen
# https://codepen.io/hexagoncircle/pen/WNbzJMZ
def make_html_style():
    html_style_var ='''
    {css}
    <html>
    <header class="placeholder-section">
      <h1>{zipcode} Zip Code Climate Risk Report <br> {address} </h1>
    </header>
    <nav class="nav-sections">
      <ul class="menu">
        <li class="menu-item"><a class="menu-item-link" href="#links">Links</a></li>
        <li class="menu-item"><a class="menu-item-link" href="#riskfactor">Risk Factors</a></li>
        <li class="menu-item"><a class="menu-item-link" href="#resources">Resources</a></li>
        <li class="menu-item"><a class="menu-item-link" href="#documentation">Documentation</a></li>
        <div class="active-line"></div>
      </ul>
    </nav>
    <main id="main-content" class="page-sections">
      <section class="page-section">
        <h2 class="section-title" id="about">Links</h2>
        <p>Links to climate data on your Zillow property: {address}</p>
        <ul>
          <li>ClimateCheck: <br> <a href="{climate_url}">{climate_url}</a> </li>
          <li>Realtor.com: <br> <a href="{realtor_link}">{realtor_link}</a> </li>
          <li>Redfin.com: <br> <a href="{redfin_link}">{redfin_link}</a> </li>
          <li> You can also search the address at <a href="https://riskfactor.com/"> https://riskfactor.com/ </a> </li>
        </ul>
      </section>
      <section class="page-section">
        <h2 class="section-title" id="about">Risk Factors</h2>
        <p>Risk Factor by the First Street Foundation is a tool to find your home and area's environmental risk from flooding, wildfire, and extreme heat. Compiled below is a report on the risk of {zipcode} zip code from the Risk Factor publicly available data. <br> <br> If there is a zero for every category, RiskFactor data was not available for that zip code in the publicly available dataset.</p>
        <h3>General Risk</h3>
        <p>{html_graph}</p>
        <p>{html_graph2}</p>
        <h3>HeatFactor</h3>
        <p>Below are the number and percent of properties in {zipcode} zip code for each level of HeatFactor risk:</p>
        <ul>
          <li>Minimal: {minimal_heat} - {minimal_heat_percent}%</li>
          <li>Minor: {minor_heat} - {minor_heat_percent}%</li>
          <li>Major: {major_heat} - {major_heat_percent}%</li>
          <li>Severe: {severe_heat} - {severe_heat_percent}%</li>
          <li>Extreme: {extreme_heat} - {extreme_heat_percent}%</li>
        </ul>
        <h3>FireFactor</h3>
        <p>Below are the number and percent of properties in {zipcode} zip code for each level of FireFactor risk:</p>
        <ul>
          <li>Minimal: {minimal_fire} - {minimal_fire_percent}%</li>
          <li>Minor: {minor_fire} - {minor_fire_percent}%</li>
          <li>Major: {major_fire} - {major_fire_percent}%</li>
          <li>Severe: {severe_fire} - {severe_fire_percent}%</li>
          <li>Extreme: {extreme_fire} - {extreme_fire_percent}%</li>
        </ul>
        <h3>FloodFactor</h3>
        <p>Below are the number and percent of properties in {zipcode} zip code for each level of FloodFactor risk:</p>
        <ul>
          <li>Minimal: {minimal_flood} - {minimal_flood_percent}%</li>
          <li>Minor: {minor_flood} - {minor_flood_percent}%</li>
          <li>Major: {major_flood} - {major_flood_percent}%</li>
          <li>Severe: {severe_flood} - {severe_flood_percent}%</li>
          <li>Extreme: {extreme_flood} - {extreme_flood_percent}%</li>
        </ul>
      </section>
      <section class="page-section">
      <h2 class="section-title" id="resources">Resources</h2>
      <p>Risk Factor provides guides on how individuals can protect their homes against flood, heat, and fire risk in the links below:</p>
          <li>Heat: <a href="https://riskfactor.com/solutions/heat#personalsolutions">https://riskfactor.com/solutions/heat#personalsolutions</a> </li>
          <li>Fire: <a href="https://riskfactor.com/solutions/fire#personalsolutions">https://riskfactor.com/solutions/fire#personalsolutions</a> </li>
          <li>Flood: <a href="https://riskfactor.com/solutions/flood#personalsolutions">https://riskfactor.com/solutions/flood#personalsolutions</a> </li>
      <section class="page-section">
        <h2 class="section-title" id="documentation">Documentation</h2>
        <p>HeatFactor, FloodFactor, and FireFactor scores are coded as: </p>
        <ul>
          <li>1: Minimal</li>
          <li>2: Minor</li>
          <li>3-4: Moderate</li>
          <li>5-6: Major</li>
          <li>7-8: Severe</li>
          <li>9-10: Extreme</li>
        </ul>
        <p>Information on the publicly available Risk Factor data can be found <a href="https://firststreet.org/data-access/public-access/">here</a>. It is shared under the <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/"> Attribution-NonCommercial-ShareAlike 4.0 International License</a>. Data was downloaded in November 2022: fire data is version 1.1, heat data is version 1.1, and flood data is version 2.1.</p>
      </section>
    </main>
    <footer class="placeholder-section">
    </footer>
    </html>
    '''
    return html_style_var