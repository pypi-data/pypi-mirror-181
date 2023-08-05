
def make_vars_zip(file, risk):
    file.columns = file.columns.str.replace(risk, "risk")
    file["minimal_p"] = round(file["count_riskfactor1"] / file["count_property"], 3) * 100
    file["minor_p"] = round(file["count_riskfactor2"] / file["count_property"], 3) * 100
    file["moderate_p"] = round((file["count_riskfactor3"] + file["count_riskfactor4"]) / file["count_property"],
                               3) * 100
    file["major_p"] = round(((file["count_riskfactor5"] + file["count_riskfactor6"]) / file["count_property"]), 3) * 100
    file["severe_p"] = round(((file["count_riskfactor7"] + file["count_riskfactor8"]) / file["count_property"]),
                             3) * 100
    file["extreme_p"] = round(((file["count_riskfactor9"] + file["count_riskfactor10"]) / file["count_property"]),
                              3) * 100

    file["minimal"] = file["count_riskfactor1"]
    file["minor"] = file["count_riskfactor2"]
    file["moderate"] = (file["count_riskfactor3"] + file["count_riskfactor4"])
    file["major"] = (file["count_riskfactor5"] + file["count_riskfactor6"])
    file["severe"] = (file["count_riskfactor7"] + file["count_riskfactor8"])
    file["extreme"] = (file["count_riskfactor9"] + file["count_riskfactor10"])