from tictactoe import *

def test_terminal():
    assert terminal([[X, EMPTY, EMPTY],
                    [EMPTY, EMPTY, EMPTY],
                    [EMPTY, EMPTY, EMPTY]]) == False

def test_player():
    assert player(initial_state()) == X
    assert player( [[X, EMPTY, EMPTY],
                    [EMPTY, EMPTY, EMPTY],
                    [EMPTY, EMPTY, EMPTY]]) == O
    
def test_actions():
    assert actions([[X, O, X],
                    [O, EMPTY, X],
                    [O, X, O]]) == {(1, 1)}
    
def test_result():
    assert result( [[X, O, X],
                    [O, EMPTY, X],
                    [O, X, O]], (1, 1)) == [[X, O, X],
                                            [O, X, X],
                                            [O, X, O]]
    
def test_winner():
    assert winner( [[X, EMPTY, EMPTY],
                    [EMPTY, EMPTY, EMPTY],
                    [EMPTY, EMPTY, EMPTY]]) == None
    assert winner( [[X, O, X],
                    [O, X, O],
                    [O, X, X]]) == X
    assert winner( [[X, O, X],
                    [X, O, O],
                    [O, X, X]]) == None
    
def test_utility():
    assert utility([[X, O, X],
                    [O, X, O],
                    [O, X, X]]) == 1
    assert utility([[X, O, X],
                    [O, O, O],
                    [X, X, EMPTY]]) == -1
    assert utility([[X, O, X],
                    [X, O, O],
                    [O, X, X]]) == 0