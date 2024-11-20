from pagerank import *

def test_transition_model():
    assert transition_model(crawl("corpus0"),"2.html",damping_factor=DAMPING) == None