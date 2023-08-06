from typing import List, Dict, Union
from dash import dcc, html

filler = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer dictum hendrerit quam ac convallis. Maecenas laoreet nibh rutrum tortor porta, sed faucibus ex tincidunt. Sed sed est dolor. Fusce convallis dui sed tortor posuere scelerisque et non nisl. Maecenas sollicitudin non nisl ut lobortis. Proin ultrices vel erat quis ultricies. Nunc accumsan purus nibh, eu luctus odio eleifend id. Etiam eget lectus sed erat tincidunt imperdiet. Donec rutrum mauris lacinia eros ultrices, rutrum interdum tortor pulvinar. Donec id libero ut dolor ultrices maximus. Vivamus dictum ultrices metus in pharetra. In in viverra est. Praesent velit eros, viverra a ultricies quis, pellentesque in ipsum. Suspendisse lacus justo, placerat eget dignissim quis, laoreet non nisi."

desc_stats = ["mean", "median", "std dev", "mode", "max", "min"]

graph_types = [{"label": "Basic Token Histogram", "value": "basic_token_hist"}, 
               {"label": "Token Distribution Graph", "value": "token_dist_graph"}, 
               {"label": "Token Type Graph", "value": "token_type_graph"},
               {"label": "Type Distrubtion Graph", "value": "type_dist_graph"},]

data_editor_components = [
    html.P(
        ["Datapoint Name"],
        className="dataLabel"
    ),
    html.Div([
        html.Label(["Raw Input:"], htmlFor="input"),
        html.Textarea([filler], id="input", name="input", rows="4", cols="18")],
        className="dataField"),
    html.Div([
        html.Label(["Vectorized input 1:"], htmlFor="data1"),
        dcc.Input(type="text", id="data1", name="data1"),
        html.Label(["Vectorized input 2:"], htmlFor="data2"),
        dcc.Input(type="text", id="data2", name="data2"),
        html.Label(["Vectorized input 3:"], htmlFor="data3"),
        dcc.Input(type="text", id="data3", name="data3"),
        html.Label(["Vectorized input 4:"], htmlFor="data4"),
        dcc.Input(type="text", id="data4", name="data4"),
        html.Label(["Vectorized input 5:"], htmlFor="data5"),
        dcc.Input(type="text", id="data5", name="data5")
    ], className="dataField"),
    html.Div(["Predictions:", html.Br(), "[Insert table here]"], className="dataOutput")]


def graph_settings_components(num: int, datasets: List[Dict[str, str]], dataset: str, models: List[Dict[str, str]], model: str):
    return html.Div([
        "Dataset:",
        dcc.Dropdown(datasets, value=dataset,
                     id=f"dataset_dropdown_{num}", clearable=False),
        "Model:",
        dcc.Dropdown(models, value=model, id=f"model_dropdown_{num}", clearable=False),
        "Descriptive Stat:",
        dcc.Dropdown(desc_stats, value="mean", id=f"desc_stats_{num}", clearable=False),
        "Num Tokens:",
        dcc.Input(type="text", id=f"num_token_{num}"),
        html.Br(),
        "Num Input Sequences:",
        dcc.Input(type="text", id=f"input_seq_{num}"),
        html.Br(),
        "Graph type:",
        dcc.Dropdown(graph_types, value=graph_types[0]["value"], id=f"graph_type_{num}", clearable=False)
    ], className="graphSettingsFill")


graph_display_components = [
    html.Div([
        html.Div([
            dcc.Graph(id="graph1")],
            className="graphFill"),
        html.Div([
            dcc.Graph(id="graph2")],
            className="graphFill")],
        className="graph")]
