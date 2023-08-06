# content of test_sample.py
def func(x):
    return x + 1


import pytest


TEST_VAL = [1, 2, 3]
TEST_DICT = {"a": {"b": {"c": TEST_VAL}}}

from addict import Dict, walker as dict_walker


@pytest.fixture
def prop():
    return Dict()


@pytest.fixture
def trackerprop():
    return Dict(track_changes=True)


@pytest.fixture
def populated_trackerprop():
    mydict = Dict(track_changes=True)
    mydict.a.b = 1
    mydict.a.c = 1
    mydict.x = "4"
    return mydict


@pytest.fixture
def freezed_populated_trackerprop(populated_trackerprop):
    populated_trackerprop.freeze()
    return populated_trackerprop


@pytest.fixture
def dict():
    return Dict


@pytest.mark.skip(reason="no way of currently testing this")
class TestBasicDictOps:
    def test_set_one_level_item(self, prop):
        some_dict = {"a": TEST_VAL}
        prop["a"] = TEST_VAL
        assert prop == some_dict

    def test_set_two_level_items(self, prop):
        some_dict = {"a": {"b": TEST_VAL}}
        prop["a"]["b"] = TEST_VAL
        assert prop == some_dict

    def test_set_three_level_items(self, prop):
        prop["a"]["b"]["c"] = TEST_VAL
        assert prop == TEST_DICT

    def test_set_one_level_property(self, prop):
        prop.a = TEST_VAL
        assert prop == {"a": TEST_VAL}

    def test_set_two_level_properties(self, prop):
        prop.a.b = TEST_VAL
        assert prop == {"a": {"b": TEST_VAL}}

    def test_set_three_level_properties(self, prop):
        prop.a.b.c = TEST_VAL
        assert prop == TEST_DICT

    def test_init_with_dict(self, prop):
        assert TEST_DICT == Dict(TEST_DICT)

    def test_init_with_kws(self):
        # TODO: how to use fixtures here:
        prop = Dict(a=2, b={"a": 2}, c=[{"a": 2}])
        assert prop == {"a": 2, "b": {"a": 2}, "c": [{"a": 2}]}

    def test_init_with_tuples(self, dict):
        prop = dict((0, 1), (1, 2), (2, 3))
        assert prop == {0: 1, 1: 2, 2: 3}

    def test_init_with_list(self, dict):
        prop = dict([(0, 1), (1, 2), (2, 3)])
        assert prop == {0: 1, 1: 2, 2: 3}

    def test_init_with_generator(self, dict):
        prop = dict(((i, i + 1) for i in range(3)))
        assert prop == {0: 1, 1: 2, 2: 3}

    def test_init_with_tuples_and_empty_list(self, dict):
        prop = dict((0, 1), [], (2, 3))
        assert prop == {0: 1, 2: 3}


# port rest of tests from addict


# @pytest.mark.skip(reason="temporarly turning off")
class TestTracking:
    def test_has_track_changes_attr(self, trackerprop):
        assert getattr(trackerprop, "__track_changes") == True

    def test_with_one_level_item(self, trackerprop):
        trackerprop["a"] = 1
        assert list(trackerprop.get_changed_history()) == ["/a"]

    def test_with_one_level_two_item(self, trackerprop):
        trackerprop["a"] = 3
        trackerprop["g"] = 5
        assert list(trackerprop.get_changed_history()) == ["/a", "/g"]

    def test_with_two_level_two_item(self, trackerprop):
        trackerprop.a.b = 3
        trackerprop.a.c = 5
        assert list(trackerprop.get_changed_history()) == ["/a/b", "/a/c"]

    def test_with_two_level_two_list_item(self, trackerprop):
        trackerprop.a.b = [1, [1]]
        trackerprop.a.c = [2, [2, [3]]]
        assert list(trackerprop.get_changed_history()) == [
            "/a/b/0",
            "/a/b/1/0",
            "/a/c/0",
            "/a/c/1/0",
            "/a/c/1/1/0",
        ]

    def test_with_two_level_two_dict_item(self, trackerprop):
        trackerprop.a.b = {"a": 1}
        trackerprop.a.c = {"b": 2}

        assert list(trackerprop.get_changed_history()) == [
            "/a/b",
            "/a/c",
        ]

    def test_with_two_level_two_tuple_item(self, trackerprop):
        trackerprop.a.b = ("a", "b")
        trackerprop.a.c = ("a", "c")
        print("in tuple")
        assert list(trackerprop.get_changed_history()) == [
            "/a/b",
            "/a/c",
        ]

    def test_clear_changed_history(self, populated_trackerprop):
        populated_trackerprop.clear_changed_history()
        assert list(populated_trackerprop.get_changed_history()) == []

    # This test currently failing
    def test_clear_changed_history_list(self, trackerprop):
        trackerprop.a.b = [1, [1]]
        trackerprop.a.c = [2, [2, [3]]]
        trackerprop.clear_changed_history()
        assert list(trackerprop.get_changed_history()) == []

    def test_clear_changed_history_dict(self, trackerprop):
        trackerprop.a.b = {"a": 1}
        trackerprop.a.c = {"b": 1}
        trackerprop.clear_changed_history()
        assert list(trackerprop.get_changed_history()) == []

    def test_clear_changed_history_tupe(self, trackerprop):
        trackerprop.a.b = (1, 2)
        trackerprop.a.c = (1, 2)
        trackerprop.clear_changed_history()
        assert list(trackerprop.get_changed_history()) == []


# TODO: test list, test clear_history, review code.


class TestMisc:
    @pytest.mark.skip(reason="temporarly turning off")
    def test_walker(self, populated_trackerprop):
        assert {("/a/b", 1), ("/x", "4"), ("/a/c", 1)} == {
            _ for _ in dict_walker(populated_trackerprop)
        }

    @pytest.mark.skip(reason="temporarly turning off")
    def test_walker_with_guards(self, populated_trackerprop):
        res = {_ for _ in dict_walker(populated_trackerprop, guards=["/a"])}

        # TODO: improve assertion; currently blocked on Dict being unhashable type
        assert len([("/a", {"b": 1, "c": 1}), ("/x", "4")]) == len(res)

    @pytest.mark.skip(reason="temporarly turning off")
    def test_modify_frozen(self, populated_trackerprop):
        """
        try to modify a nested
        """
        populated_trackerprop.freeze()
        with pytest.raises(KeyError) as excinfo:
            populated_trackerprop.z = 5
        assert "z" in str(excinfo.value)

    @pytest.mark.skip(reason="temporarly turning off")
    def test_modify_nested_frozen(self, populated_trackerprop):
        """
        freeze and modify a nested key. Check to see if frozen is
        not superficial.
        """
        populated_trackerprop.r.nested_key = Dict()
        populated_trackerprop.freeze()
        with pytest.raises(KeyError) as excinfo:
            populated_trackerprop.r.nested_key.dd = 5

        assert "dd" in str(excinfo.value)

    def test_unfreeze(self, freezed_populated_trackerprop):
        freezed_populated_trackerprop.unfreeze()
        freezed_populated_trackerprop.kk = 5
        assert freezed_populated_trackerprop.kk == 5

    # def test_delete_attr(self, populated_trackerprop):
    #     pass


# TODO: test to_dict, deepcopy, __missing__,


@pytest.mark.skip(reason="temporarly turning off")
class TestInitialization:
    def test_init_tuple(self):
        mydict = Dict((("a", 1), ("b", "2")))
        assert mydict == {"a": 1, "b": "2"}

    # TODO: test other initialization; mainly nested tuple;
    # some test cases covered in original repo
