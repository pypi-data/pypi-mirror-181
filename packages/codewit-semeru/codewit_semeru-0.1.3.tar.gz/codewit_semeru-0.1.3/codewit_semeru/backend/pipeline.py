import sys
import io
import os
import json
import requests
import time
from collections import Counter, defaultdict
from dotenv import load_dotenv
from typing import List
from transformers import AutoTokenizer
import torch
import tokenize

path = f"{sys.path[0]}/codewit_semeru/backend/config/.env"
load_dotenv(path)

HF_API_KEY = os.getenv("HF_API_TOKEN")
assert HF_API_KEY is not None

headers = {"Authorization": f"Bearer {HF_API_KEY}"}


class Pipeline:
    # TODO https://github.com/tensorflow/tensorflow/issues/53529
    device = "cuda:0" if torch.cuda.is_available() else "cpu"

    @staticmethod
    def pipe_id(model: str, dataset_id: str) -> str:
        return "<>".join([model, dataset_id])

    def __init__(self, model: str, dataset: List[str], dataset_id: str = "") -> None:
        self.model: str = model
        self.dataset: List[str] = dataset
        self.dataset_id: str = dataset_id

        self.id: str = Pipeline.pipe_id(model, dataset_id)

        self.tokenizer = AutoTokenizer.from_pretrained(model)

        self.api_url = f"https://api-inference.huggingface.co/models/{self.model}"

        self.output_tok_freqs = defaultdict(list)
        self.output_group_freqs = defaultdict(list)

        self.completed: bool = False
        self.error_dict = {"TokenError": [], "IndentationError": []}



    def query_model(self):
        print("Querying HF API, this will take a moment...")
        data = json.dumps({"inputs": self.dataset, "parameters": {
                          "return_full_text": False, "max_new_tokens": 50, "max_time": 30}})
        response = requests.request(
            "POST", self.api_url, headers=headers, data=data)
        return json.loads(response.content.decode("utf-8"))

    def run(self) -> None:
        res = self.query_model()
        while type(res) is dict and res["error"]:
            print("error: ", res["error"])
            if "estimated_time" not in res:
                raise RuntimeError("pipeline run")

            print("Retrying in ", res["estimated_time"], "seconds")
            time.sleep(res["estimated_time"])
            print("Retrying...")
            res = self.query_model()

        output_seqs = [data[0]["generated_text"] for data in res]
        # for item in output_seqs:
        #     print(f"NEW ITEM == {item}")
        # Insert python-src-tokenizer here
        python_src_tuples = [self.python_src_tokenizer(seq, 0) for seq in output_seqs]

        group_tkns = []

        for item in python_src_tuples:
            temp = []
            for tuple in item:
                temp.append(tokenize.tok_name[tuple.exact_type])
            group_tkns.append(temp)

        # Counter for group types, extended zeroes
        for tkns in group_tkns:
            cts = Counter(tkns)
            for tkn in cts:
                self.output_group_freqs[tkn].append(cts[tkn])

        # extend zeroes similar to output_tok_freqs
        for tkn in self.output_group_freqs:
            seq_diff = len(group_tkns) - len(self.output_group_freqs[tkn])
            self.output_group_freqs[tkn].extend([0] * seq_diff)

        # Start ind tokens here
        output_tkns = [self.tokenizer.tokenize(seq) for seq in output_seqs]

        for i in range(len(output_tkns)):
            for j in range(len(output_tkns[i])):
                output_tkns[i][j] = self.tokenizer.convert_tokens_to_ids(output_tkns[i][j])
                output_tkns[i][j] = self.tokenizer.decode(output_tkns[i][j])

        for tkns in output_tkns:
            cts = Counter(tkns)
            for tkn in cts:
                self.output_tok_freqs[tkn].append(cts[tkn])
        
        # add 0 freq counts for tokens which were not within all predicted sequences
        for tkn in self.output_tok_freqs:
            seq_diff = len(output_tkns) - len(self.output_tok_freqs[tkn])
            self.output_tok_freqs[tkn].extend([0] * seq_diff)

        # print(f"predicted strings:")
        # print(*output_seqs, sep="\n---------------------------------\n")
        self.completed = True
        print(f"Pipeline completed for pipe {self.id}")

    # Template for python_src_tokenizer
    # TODO change return type to just token group and follow same process as other types
    def python_src_tokenizer(self, s: str, id: int) -> List[tokenize.TokenInfo]:
        fp = io.StringIO(s)
        filter_types = [tokenize.ENCODING, tokenize.ENDMARKER, tokenize.ERRORTOKEN]
        tokens = []
        token_gen = tokenize.generate_tokens(fp.readline)
        while True:
            try:
                token = next(token_gen)
                if token.string and token.type not in filter_types:
                    tokens.append(token)
            except tokenize.TokenError:
                self.error_dict["TokenError"].append(id)
                break
            except StopIteration:
                break
            except IndentationError:
                self.error_dict["IndentationError"].append(id)
                continue
        return tokens