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


# def test_test_bp_and_pulse():
#     d, s, p = goals.take_bp_and_pulse()
#     assert d == 120
#     assert s == 80
#     assert p == 60


def test_parse_condition_file_to_int():
    file_dir = "./messageConditions/condition_4_onetime_fair.txt"
    condition_num = goals.parse_condition_file_to_int(file_dir)
    assert condition_num == '4'
