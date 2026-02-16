import pytest
from cognova.frameworks.registry import (
    get_framework,
    list_frameworks,
    get_framework_choices,
    get_frameworks_by_category,
    get_core_frameworks,
    validate_framework,
    format_framework_table,
    FrameworkCategory,
    FRAMEWORKS,
)


def test_get_framework_wrong_name():
    with pytest.raises(ValueError):
        get_framework("wrong_name")


def test_get_framework_proper_name():
    framework = get_framework("robot")
    assert framework.name == "Robot Framework"
    assert framework.category == FrameworkCategory.BDD
    assert framework.language == "Python"
    assert framework.extension == ".robot"


@pytest.mark.parametrize(
    "invalid_input",
    [
        "RoBoT",
        " robot ",
        "",
        "12345",
        "@robot!",
    ],
)
def test_get_framework_invalid_input_raises_valueerror(invalid_input):
    with pytest.raises(ValueError):
        get_framework(invalid_input)


@pytest.mark.parametrize(
    "non_str_input",
    [
        None,
        1234,
    ],
)
def test_get_framework_non_str_input_raises_valueerror(non_str_input):
    with pytest.raises(ValueError):
        get_framework(non_str_input)


def test_list_frameworks_when_no_filter():
    frameworks = list_frameworks()
    assert len(frameworks) == 25


@pytest.mark.parametrize(
    "category_filter, expected_count",
    [
        (FrameworkCategory.UNIT, 4),
        (FrameworkCategory.E2E, 4),
        (FrameworkCategory.BDD, 5),
        (FrameworkCategory.PERFORMANCE, 5),
        (FrameworkCategory.SECURITY, 3),
        (FrameworkCategory.API, 4),
        (FrameworkCategory.MOBILE, 0),
    ],
)
def test_list_frameworks_with_category_filter(category_filter, expected_count):
    frameworks = list_frameworks(category=category_filter)
    assert len(frameworks) == expected_count


@pytest.mark.parametrize(
    "invalid_category",
    [
        "invalid_category",
        123,
    ],
)
def test_list_frameworks_invalid_category_returns_empty(invalid_category):
    frameworks = list_frameworks(category=invalid_category)
    assert frameworks == []


@pytest.mark.parametrize(
    "category_priority, expected_count",
    [
        (0, 11),
        (1, 6),
        (2, 8),
    ],
)
def test_list_frameworks_with_priority_filter(category_priority, expected_count):
    frameworks = list_frameworks(priority=category_priority)
    assert len(frameworks) == expected_count


def test_list_frameworks_sorted_by_priority_then_name():
    frameworks = list_frameworks()
    for i in range(len(frameworks) - 1):
        current, next_fw = frameworks[i], frameworks[i + 1]
        assert (current.priority, current.name) <= (next_fw.priority, next_fw.name)


@pytest.mark.parametrize(
    "priority_filter",
    [
        0,
        1,
        2,
    ],
)
def test_list_frameworks_priority_filter_returns_correct_priority(priority_filter):
    frameworks = list_frameworks(priority=priority_filter)
    assert all(fw.priority == priority_filter for fw in frameworks)


@pytest.mark.parametrize(
    "invalid_priority_filter",
    [
        -1,
        3,
        99,
    ],
)
def test_list_frameworks_invalid_priority_filter_returns_empty(invalid_priority_filter):
    frameworks = list_frameworks(priority=invalid_priority_filter)
    assert frameworks == []


@pytest.mark.parametrize(
    "language, min_expected",
    [
        ("Python", 8),
        ("JavaScript", 4),
        ("Java", 3),
        ("TypeScript", 2),
    ],
)
def test_list_frameworks_with_language_filter(language, min_expected):
    frameworks = list_frameworks(language=language)
    assert len(frameworks) >= min_expected
    assert all(fw.language == language for fw in frameworks)


@pytest.mark.parametrize(
    "language_variation",
    ["python", "Python", "PYTHON", "PyThOn"],
)
def test_list_frameworks_language_filter_case_insensitive(language_variation):
    frameworks = list_frameworks(language=language_variation)
    assert len(frameworks) >= 8
    assert all(fw.language.lower() == "python" for fw in frameworks)


@pytest.mark.parametrize(
    "invalid_language",
    [
        "NonExistentLanguage",
        "",
        "12345",
        "@Python!",
        "Ruby",
        "Go",
    ],
)
def test_list_frameworks_invalid_language_returns_empty(invalid_language):
    frameworks = list_frameworks(language=invalid_language)
    assert frameworks == []


def test_list_frameworks_combined_category_and_language():
    frameworks = list_frameworks(category=FrameworkCategory.UNIT, language="Python")
    assert len(frameworks) == 1
    assert frameworks[0].name == "pytest"
    assert all(fw.category == FrameworkCategory.UNIT for fw in frameworks)
    assert all(fw.language == "Python" for fw in frameworks)


def test_list_frameworks_combined_category_and_priority():
    frameworks = list_frameworks(category=FrameworkCategory.E2E, priority=0)
    assert len(frameworks) == 2
    assert all(fw.category == FrameworkCategory.E2E for fw in frameworks)
    assert all(fw.priority == 0 for fw in frameworks)


def test_list_frameworks_combined_language_and_priority():
    frameworks = list_frameworks(language="Python", priority=0)
    assert len(frameworks) >= 4
    assert all(fw.language == "Python" for fw in frameworks)
    assert all(fw.priority == 0 for fw in frameworks)


def test_list_frameworks_combined_all_filters():
    frameworks = list_frameworks(category=FrameworkCategory.BDD, language="Python", priority=0)
    assert len(frameworks) == 2
    assert all(fw.category == FrameworkCategory.BDD for fw in frameworks)
    assert all(fw.language == "Python" for fw in frameworks)
    assert all(fw.priority == 0 for fw in frameworks)


def test_list_frameworks_combined_filters_no_match():
    frameworks = list_frameworks(category=FrameworkCategory.UNIT, language="Scala", priority=0)
    assert frameworks == []


def test_list_frameworks_with_explicit_none_filters():
    frameworks_none = list_frameworks(category=None, language=None, priority=None)
    frameworks_default = list_frameworks()
    assert frameworks_none == frameworks_default


def test_get_framework_choices_output():
    choices = get_framework_choices()
    frameworks = list_frameworks()
    assert len(choices) == len(frameworks)
    for choice in choices:
        fw = get_framework(choice)
        assert fw in frameworks


def test_get_framework_choices_with_keys():
    choices = get_framework_choices()
    for choice, key in zip(choices, sorted(FRAMEWORKS.keys())):
        assert choice == key


def test_get_frameworks_by_category():
    frameworks = get_frameworks_by_category()
    assert len(frameworks) == len(FrameworkCategory)
    for category, fw_list in frameworks.items():
        for fw in fw_list:
            assert fw.category == category


def test_get_frameworks_by_category_all_counts():
    frameworks = get_frameworks_by_category()
    total_count = sum(len(fw_list) for fw_list in frameworks.values())
    assert total_count == len(FRAMEWORKS)


@pytest.mark.parametrize(
    "category, expected_count",
    [
        (FrameworkCategory.UNIT, 4),
        (FrameworkCategory.E2E, 4),
        (FrameworkCategory.BDD, 5),
        (FrameworkCategory.PERFORMANCE, 5),
        (FrameworkCategory.SECURITY, 3),
        (FrameworkCategory.API, 4),
        (FrameworkCategory.MOBILE, 0),
    ],
)
def test_get_frameworks_by_category_counts(category, expected_count):
    frameworks = get_frameworks_by_category()
    assert len(frameworks[category]) == expected_count


def test_get_frameworks_by_category_empty_categories():
    frameworks = get_frameworks_by_category()
    for category in FrameworkCategory:
        assert category in frameworks


def test_get_frameworks_by_category_sorted_by_priority_then_name():
    frameworks = get_frameworks_by_category()
    for _, fw_list in frameworks.items():
        for i in range(len(fw_list) - 1):
            current, next_fw = fw_list[i], fw_list[i + 1]
            assert (current.priority, current.name) <= (next_fw.priority, next_fw.name)


def test_get_core_frameworks():
    frameworks = FRAMEWORKS.values()
    core_frameworks = get_core_frameworks()
    total_count = sum(1 for fw in frameworks if fw.priority == 0)
    assert len(core_frameworks) == total_count


def test_get_core_frameworks_all_priority_zero():
    core_frameworks = get_core_frameworks()
    assert all(fw.priority == 0 for fw in core_frameworks)


def test_get_core_frameworks_sorted_by_name():
    core_frameworks = get_core_frameworks()
    for i in range(len(core_frameworks) - 1):
        current, next_fw = core_frameworks[i], core_frameworks[i + 1]
        assert current.name <= next_fw.name


@pytest.mark.parametrize("valid_name", ["pytest", "jest", "playwright-py", "k6"])
def test_validate_framework_valid_names(valid_name):
    assert validate_framework(valid_name) is True


@pytest.mark.parametrize(
    "invalid_name",
    ["invalid", "PyTest", " pytest", "", "unknown-framework"],
)
def test_validate_framework_invalid_names(invalid_name):
    assert validate_framework(invalid_name) is False


def test_validate_framework_all_registered():
    for name in FRAMEWORKS.keys():
        assert validate_framework(name) is True


def test_format_framework_table_returns_string():
    result = format_framework_table()
    assert isinstance(result, str)


def test_format_framework_table_contains_header():
    result = format_framework_table()
    assert "Supported Frameworks:" in result
    assert "Framework" in result
    assert "Category" in result
    assert "Language" in result


def test_format_framework_table_contains_all_frameworks():
    result = format_framework_table()
    for name in FRAMEWORKS.keys():
        assert name in result


def test_format_framework_table_contains_total_count():
    result = format_framework_table()
    assert f"Total: {len(FRAMEWORKS)} frameworks" in result


def test_format_framework_table_contains_priority_labels():
    result = format_framework_table()
    assert "Core" in result
    assert "Standard" in result
    assert "Extended" in result
