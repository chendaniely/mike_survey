import nose
import random
import glob
import goals


def test_pick_condition_file():
    random.seed(2)
    expected_file = "./messageConditions/condition_4_onetime_fair.txt"
    assert goals.pick_condition_file() == expected_file


def test_read_condition_file():
    random.seed(2)
    condition = goals.pick_condition_file()
    condition_responses = goals.read_condition_file_to_list(condition)
    print condition_responses
    assert len(condition_responses) == 11
