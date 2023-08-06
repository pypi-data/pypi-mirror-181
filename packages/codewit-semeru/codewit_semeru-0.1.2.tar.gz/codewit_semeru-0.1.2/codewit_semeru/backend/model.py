from typing import List
import pandas as pd
import statistics
from .pipeline import Pipeline
from .pipeline_store import PipelineStore


pipes = PipelineStore()


def stats_func(stat: str):
    if stat == "mean":
        return statistics.mean
    elif stat == "median":
        return statistics.median
    elif stat == "std dev":
        return statistics.stdev
    elif stat == "max":
        return max
    elif stat == "min":
        return min
    elif stat == "mode":
        return statistics.mode
    else:
        raise ValueError


def preprocess(model: str, dataset: List[str], dataset_id: str, stat: str, graph: str) -> pd.DataFrame:
    pipe = pipes.get_pipeline(Pipeline.pipe_id(model, dataset_id))
    if not pipe:
        pipe = Pipeline(model, dataset, dataset_id)
        pipes.add_pipeline(pipe)
        pipes.run_pipe(pipe.id)

    if graph == "basic_token_hist":
        token_freq = pd.DataFrame()

        try:
            stat_func = stats_func(stat)
            output_tkn_freqs = {tkn: stat_func(freqs) for tkn, freqs in pipe.output_tok_freqs.items()}

            token_freq = pd.DataFrame.from_dict(output_tkn_freqs, orient="index", columns=[
                                                "frequency"]).rename_axis("token").reset_index()
            token_freq = token_freq.sort_values(by="frequency", ascending=False)

        except ValueError:
            print("Supported statistics are mean, median, std dev, mode, max, and min. Please use one of them.")

        return token_freq.head(20)
    
    elif graph == "token_type_graph":
        token_freq = pd.DataFrame()

        try:
            stat_func = stats_func(stat)
            output_group_freqs = {tkn: stat_func(freqs) for tkn, freqs in pipe.output_group_freqs.items()}

            token_freq = pd.DataFrame.from_dict(output_group_freqs, orient="index", columns=[
                                                "frequency"]).rename_axis("token_type").reset_index()
         
            token_freq = token_freq.sort_values(by="frequency", ascending=False)

        except ValueError:
            print("Supported statistics are mean, median, std dev, mode, max, and min. Please use one of them.")
        
        return token_freq
    
    elif graph == "type_dist_graph":
        output_group_freqs = pipe.output_group_freqs
        group_freq = pd.DataFrame(columns=["token_type", "frequency", "output_sequence"])

        for tkn, freqs in output_group_freqs.items():
            for i, freq in enumerate(freqs):
                row = pd.Series({"token_type": tkn, "frequency": freq, "output_sequence": i+1})
                group_freq = pd.concat([group_freq, row.to_frame().T], ignore_index=True)

        group_freq = group_freq.sort_values(by="frequency", ascending=False)

        return group_freq

    else:
        output_tkn_freqs = pipe.output_tok_freqs
        token_freq = pd.DataFrame(columns=["token", "frequency", "output_sequence"])

        for tkn, freqs in output_tkn_freqs.items():
            for i, freq in enumerate(freqs):
                row = pd.Series({"token": tkn, "frequency": freq, "output_sequence": i+1})
                token_freq = pd.concat([token_freq, row.to_frame().T], ignore_index=True)

        token_freq = token_freq.sort_values(by="frequency", ascending=False)

        return token_freq
