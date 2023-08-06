
from codewit_semeru.backend.pipeline import Pipeline

def test_pipeline():
    pipe = Pipeline("gpt2", ["Hello World", "this is a list", "Duke Ignat Eli Langston Young"], "test") 

    assert pipe.api_url == f"https://api-inference.huggingface.co/models/gpt2"
    assert pipe.id == "gpt2<>test"
    assert pipe.model == "gpt2"
    assert pipe.dataset == ["Hello World", "this is a list", "Duke Ignat Eli Langston Young"]
    assert pipe.dataset_id == "test"
    
    assert not pipe.output_group_freqs
    assert not pipe.output_tok_freqs
    assert not pipe.completed

def test_pipeline_run():
    pipe = Pipeline("gpt2", ["Hello World", "this is a list", "Duke Ignat Eli Langston Young"])
    pipe.run()

    assert pipe.completed == True
    assert pipe.output_group_freqs
    assert pipe.output_tok_freqs #output str list not empty
