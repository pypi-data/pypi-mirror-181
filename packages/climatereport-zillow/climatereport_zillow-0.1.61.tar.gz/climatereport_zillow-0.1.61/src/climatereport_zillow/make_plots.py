import numpy as np
import matplotlib.pyplot as plt
import io
import base64

def make_plot_zip(zipcode,heat_zip, flood_zip,fire_zip):
    my_columns = ["count_riskfactor1", "count_riskfactor2", "count_riskfactor3", "count_riskfactor4", "count_riskfactor5",
          "count_riskfactor6", "count_riskfactor7", "count_riskfactor8", "count_riskfactor9", "count_riskfactor10"]
    labels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    y_heat = []
    if zipcode in heat_zip.index:
        for i in my_columns:
            y_heat.append(heat_zip.loc[zipcode, i])
    else:
        y_heat = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    y_flood = []
    if zipcode in flood_zip.index:
        for i in my_columns:
            y_flood.append(flood_zip.loc[zipcode, i])
    else:
        y_flood = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    y_fire = []
    if zipcode in fire_zip.index:
        for i in my_columns:
            y_fire.append(fire_zip.loc[zipcode, i])
    else:
        y_fire = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    x = np.arange(len(labels))
    width = 0.2

    c_flood = ["#538ad5", "#4d86d5", "#4682d6", "#3f7ed6", "#397ad6", "#3276d6", "#2b72d6", "#236ed6", "#1b69d5", "#1265d5"]
    c_heat = ["#d58b50", "#d5874a", "#d58444", "#d5803d", "#d57c37", "#d57930", "#d5752a", "#d57123", "#d56d1b", "#d56912"]
    c_fire = ["#d45a4d", "#d55547", "#d55041", "#d64b3b", "#d64635", "#d6402f", "#d63a28", "#d63422", "#d52d1a", "#d52512"]

    fig, ax = plt.subplots()
    rects1 = ax.bar(x + width, y_flood, width, label='Flood', color=c_flood)
    rects2 = ax.bar(x, y_heat, width, label='Heat', color=c_fire)
    rects3 = ax.bar(x - width, y_fire, width, label="Fire", color=c_heat)
    ax.set_ylabel('Number of Properties')
    ax.set_xlabel('Risk Category (1 = Lowest Risk, 10 = High Risk)')
    ax.set_title('Number of Properties in Risk Categories in Zip Code: ' + str(zipcode))
    ax.set_xticks(x, labels)
    ax.legend()
    fig.tight_layout()

    def fig_to_base64(figure):
        img = io.BytesIO()
        figure.savefig(img, format='png',
               bbox_inches='tight')
        img.seek(0)
        return base64.b64encode(img.getvalue())

    encoded = fig_to_base64(fig)
    graph = '<img src="data:image/png;base64, {}">'.format(encoded.decode('utf-8'))
    return graph


def make_plot_state(state, heat_state,flood_state,fire_state):
    my_columns = ["count_riskfactor1", "count_riskfactor2", "count_riskfactor3", "count_riskfactor4", "count_riskfactor5",
          "count_riskfactor6", "count_riskfactor7", "count_riskfactor8", "count_riskfactor9", "count_riskfactor10"]
    labels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    y_fire_state = []
    for i in my_columns:
        y_fire_state.append(fire_state.loc[state, i])

    y_heat_state = []
    for i in my_columns:
        y_heat_state.append(heat_state.loc[state, i])

    y_flood_state = []
    for i in my_columns:
        y_flood_state.append(flood_state.loc[state, i])

    x = np.arange(len(labels))
    width = 0.2

    c_flood = ["#538ad5", "#4d86d5", "#4682d6", "#3f7ed6", "#397ad6", "#3276d6", "#2b72d6", "#236ed6", "#1b69d5",
               "#1265d5"]
    c_heat = ["#d58b50", "#d5874a", "#d58444", "#d5803d", "#d57c37", "#d57930", "#d5752a", "#d57123", "#d56d1b",
              "#d56912"]
    c_fire = ["#d45a4d", "#d55547", "#d55041", "#d64b3b", "#d64635", "#d6402f", "#d63a28", "#d63422", "#d52d1a",
              "#d52512"]

    fig, ax = plt.subplots()
    rects1 = ax.bar(x + width, y_flood_state, width, label='Flood', color=c_flood)
    rects2 = ax.bar(x, y_heat_state, width, label='Heat', color=c_fire)
    rects3 = ax.bar(x - width, y_fire_state, width, label="Fire", color=c_heat)
    ax.set_ylabel('Number of Properties')
    ax.set_xlabel('Risk Category (1 = Lowest Risk, 10 = High Risk)')
    ax.set_title('Number of Properties in Risk Categories in State: ' + str(state))
    ax.set_xticks(x, labels)
    ax.legend()
    fig.tight_layout()

    def fig_to_base64(figure):
        img = io.BytesIO()
        figure.savefig(img, format='png',
                       bbox_inches='tight')
        img.seek(0)
        return base64.b64encode(img.getvalue())

    encoded = fig_to_base64(fig)
    graph = '<img src="data:image/png;base64, {}">'.format(encoded.decode('utf-8'))

    return graph
