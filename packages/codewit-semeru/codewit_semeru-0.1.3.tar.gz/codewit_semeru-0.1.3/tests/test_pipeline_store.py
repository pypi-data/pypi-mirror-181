import pytest
from codewit_semeru.backend.pipeline_store import PipelineStore
from codewit_semeru.backend.pipeline import Pipeline


def test_add_pipeline():
    store = PipelineStore()
    pipe = Pipeline("gpt2", "Hello World")
    assert not store.pipelines #is empty

    store.add_pipeline(pipe)
    assert len(store.pipelines) == 1 #has one pipeline

def test_remove_existing_pipeline():
    store = PipelineStore()
    pipe = Pipeline("gpt2", "Hello World", "test")

    assert not store.pipelines #is empty
    store.add_pipeline(pipe)
    assert len(store.pipelines) == 1 #has one pipeline
    store.remove_pipeline("gpt2<>test")
    assert not store.pipelines #is empty

def test_remove_non_existing_pipeline():
    with pytest.raises(Exception, match="remove: invalid id"):
        store = PipelineStore()
        pipe = Pipeline("gpt2", "Hello World", "test")

        store.add_pipeline(pipe)
        store.remove_pipeline("gpt2<>test2")
        assert store.pipelines #is not empty
        assert store.get_pipeline("gpt2<>test").id == pipe.id

def test_remove_from_empty_store():
    with pytest.raises(Exception, match="remove: empty store"):
        store = PipelineStore()
        store.remove_pipeline("gpt2<>test")

def test_get_existing_pipeline():
    store = PipelineStore()
    pipe = Pipeline("gpt2", "Hello World", "test")

    store.add_pipeline(pipe)
    assert len(store.pipelines) == 1 #has one pipeline

    pipe1 = store.get_pipeline("gpt2<>test")

    assert pipe.id == pipe1.id
    
def test_get_non_existing_pipeline():
    store = PipelineStore()

    pipe1 = store.get_pipeline("gpt2<>test")

    assert pipe1 == None

def test_run_existing_pipelines():
    store = PipelineStore()
    pipe = Pipeline("gpt2", ["Hello World", "this is a list", "Duke Ignat Eli Langston Young"], "test")

    store.add_pipeline(pipe)
    store.run_pipelines()

    assert store.get_pipeline("gpt2<>test").completed == True

def test_run_pipelines_when_empty():
    store = PipelineStore()

    store.run_pipelines()

    assert True

def test_run_existing_pipe():
    store = PipelineStore()
    pipe = Pipeline("gpt2", ["Hello World", "this is a list", "Duke Ignat Eli Langston Young"], "test")

    store.add_pipeline(pipe)
    store.run_pipe("gpt2<>test")
    assert store.get_pipeline("gpt2<>test").completed == True

def test_run_non_existing_pipe():
    with pytest.raises(Exception, match="run: pipeline not in store"):
        store = PipelineStore()

        assert store.run_pipe("gpt2<>test") == None

def test_size():
    store = PipelineStore()
    pipe = Pipeline("gpt2", "Hello World", "test")

    assert store.size() == 0
    store.add_pipeline(pipe)   
    assert store.size() == 1

    store.remove_pipeline("gpt2<>test")
    assert store.size() == 0


