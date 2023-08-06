from typing import Union
from .pipeline import Pipeline


class PipelineStore(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(PipelineStore, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        self.pipelines = {}

    def add_pipeline(self, pipe: Pipeline) -> None:
        self.pipelines[pipe.id] = pipe

    def remove_pipeline(self, id: str) -> None:
        if not self.size():
            raise Exception("remove: empty store")
        if id not in self.pipelines:
            raise Exception("remove: invalid id")
        del self.pipelines[id]

    def get_pipeline(self, id: str) -> Union[Pipeline, None]:
        if id not in self.pipelines:
            return None
        return self.pipelines[id]

    def run_pipelines(self) -> None:
        for _, pipe in self.pipelines.items():
            if not pipe.completed:
                pipe.run()

    def run_pipe(self, id: str) -> None:
        if id not in self.pipelines:
            raise Exception("rerun: pipeline not in store")
        self.pipelines[id].run()

    def size(self) -> int:
        return len(self.pipelines)
