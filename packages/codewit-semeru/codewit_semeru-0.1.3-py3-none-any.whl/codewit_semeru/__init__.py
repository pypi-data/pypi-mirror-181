"""
codewit_semeru

What-if-tool Code. A Visual Tool for Understanding Machine Learning Models for Software Engineering
"""

__version__ = "0.1.3"
__author__ = "Ignat Miagkov, Duke Tran, Eli Svoboda, Langston Lee, Young Qi"
__credits__ = "College of William & Mary"


from typing import List
from .frontend.server import CodeWITServer

import os


def WITCode(model: str = "gpt2", dataset: List[str] = [], dataset_id: str = "") -> None:
    server = CodeWITServer(model, dataset, dataset_id)
    server.run()