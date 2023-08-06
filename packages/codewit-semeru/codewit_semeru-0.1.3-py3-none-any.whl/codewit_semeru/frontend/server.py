from typing import List
from uuid import uuid4
import traceback
from jupyter_dash import JupyterDash
from plotly.graph_objs._figure import Figure
import plotly.figure_factory as ff
import plotly.express as px
import numpy as np
from dash import dcc, html, Input, Output

from ..backend.model import preprocess
from ..backend.pipeline import Pipeline
from ..backend.pipeline_store import PipelineStore
from .layout import graph_settings_components


DUMMY_DATA = [{"label": str(uuid4()), "value": ["This is some chunk of code that I wish to analyze"]},
              {"label": str(uuid4()),
               "value": ["Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."]},
              {"label": str(uuid4()), "value": ["def foo(bar): print(bar) foo(123)"]}]

models = [{"label": "GPT-2", "value": "gpt2"}, {"label": "Codeparrot", "value": "codeparrot/codeparrot-small"},
          {"label": "Codegen", "value": "Salesforce/codegen-350M-mono"}, {"label": "GPT-Neo", "value": "EleutherAI/gpt-neo-125M"}]  # add codebert, neox?

pipes = PipelineStore()


class CodeWITServer():
    def __init__(self, model: str, dataset: List[str], dataset_id: str):
        self.app = JupyterDash(__name__)

        self.model_1 = model
        self.dataset_1 = dataset if dataset else DUMMY_DATA[0]["value"]

        self.model_2, self.dataset_2 = "", []

        dataset_id = next((d["label"] for d in DUMMY_DATA if d["value"] == dataset), "")
        if not dataset_id:
            dataset_id = str(uuid4())
            DUMMY_DATA.append({"label": dataset_id, "value": dataset})

        input_pipe = Pipeline(model, dataset, dataset_id)
        pipes.add_pipeline(input_pipe)
        pipes.run_pipelines()

        self.FLAT_DUMMY = [{"label": dataset["label"], "value": " ".join(
            dataset["value"])} for dataset in DUMMY_DATA]

        self.app.layout = html.Div([
            # html.Div(data_editor_components, className="dataEditor"),
            html.Div([
                html.Div([
                    html.Div([
                        "View:",
                        dcc.Dropdown(["single graph", "two graph comparison"], value="two graph comparison", id="view_dropdown", clearable=False)]),
                    html.Div([
                        graph_settings_components(
                            1, self.FLAT_DUMMY, " ".join(self.dataset_1), models, self.model_1),
                        graph_settings_components(
                            2, self.FLAT_DUMMY, " ".join(self.dataset_2), models, self.model_2)])
                ], className="graphSettings")
            ], className="graphSettings"),
            html.Div([
                dcc.Graph(id="graph1"),
                dcc.Graph(id="graph2")
            ], className="graph")
        ])

    def update_data_and_chart(self, selected_model: str, selected_dataset: List[str], selected_stat: str, selected_graph: str) -> Figure:
        # ? #60 - can this be done another way given dataset dropdown vs. input?
        dataset_id = next((d["label"] for d in self.FLAT_DUMMY if d["value"] == selected_dataset), "")
        selected_dataset_id = dataset_id if dataset_id else ""

        dataset = next((d["value"] for d in DUMMY_DATA if d["label"] == selected_dataset_id), [])
        selected_dataset = dataset if dataset else []

        if not selected_dataset:
            raise LookupError

        print(
            f"Processing {Pipeline.pipe_id(selected_model, selected_dataset_id)}\nPlease wait...")

        df = preprocess(selected_model, selected_dataset,
                        selected_dataset_id, selected_stat, selected_graph)
        print("Done!")

        if selected_graph == "basic_token_hist":
            # return px.bar(df, x="frequency", y="token", labels={"frequency": f"{selected_stat} token frequency for model {selected_model}"})
            return px.bar(df, x="frequency", y="token", labels={"frequency": str(selected_stat) + " token frequency"})
        
        elif selected_graph == "token_type_graph":
            return px.bar(df, x="frequency", y="token_type", labels={"frequency": str(selected_stat) + " token type frequency"})

        elif selected_graph == "token_dist_graph":
            frequencies = df["frequency"].tolist()
            return px.histogram(df, x=frequencies, color="token", marginal="violin", hover_data=df.columns, nbins=20,
                                title="token frequencies in output sequences", labels={"x": "frequency ranges"},
                                histfunc="count", barmode="overlay", log_y=True, opacity=0.5)

        elif selected_graph == "type_dist_graph":
            frequencies = df["frequency"].tolist()
            return px.histogram(df, x=frequencies, color="token_type", marginal="violin", hover_data=df.columns, nbins=20,
                                title="token frequencies in output sequences", labels={"x": "frequency ranges"},
                                histfunc="count", barmode="overlay", log_y=True, opacity=0.5)

        return px.bar()

    def run(self) -> None:
        # TODO: update so string representations of tokens are shown rather than tokens themselves
        @self.app.callback(Output("graph1", "figure"), Input("dataset_dropdown_1", "value"), Input("model_dropdown_1", "value"), Input("desc_stats_1", "value"), Input("graph_type_1", "value"))
        def update_bar_graph1(selected_dataset: List[str] = self.dataset_1, selected_model: str = self.model_1, selected_stat: str = "mean", selected_graph: str = "basic_token_hist"):
            try:
                return self.update_data_and_chart(selected_model, selected_dataset, selected_stat, selected_graph)
            except LookupError:
                print("error: dataset not found!")
            return px.bar()

        @self.app.callback(Output("graph2", "figure"), Input("dataset_dropdown_2", "value"), Input("model_dropdown_2", "value"), Input("desc_stats_2", "value"), Input("graph_type_2", "value"))
        def update_bar_graph2(selected_dataset: List[str] = self.dataset_2, selected_model: str = self.model_2, selected_stat: str = "mean", selected_graph: str = "basic_token_hist"):
            if selected_dataset and selected_model:
                try:
                    return self.update_data_and_chart(selected_model, selected_dataset, selected_stat, selected_graph)
                except LookupError:
                    traceback.print_exc()
                    print("error: dataset not found!")
            return px.bar()

        self.app.run_server(mode="inline", debug=True)
