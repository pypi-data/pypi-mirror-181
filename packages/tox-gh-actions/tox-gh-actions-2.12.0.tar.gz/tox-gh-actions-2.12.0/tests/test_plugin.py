import pytest
from tox.config import Config

from tox_gh_actions import plugin


def test_start_grouping_if_necessary(capsys, mocker):
    envconfig = mocker.MagicMock()
    envconfig.envname = "test123"
    envconfig.description = "This is a test environment."
    venv = mocker.MagicMock()
    venv.envconfig = envconfig

    # Start grouping in the first call
    plugin.start_grouping_if_necessary(venv)
    out1, _ = capsys.readouterr()
    assert out1 == "::group::tox: test123 - This is a test environment.\n"

    # Should not start groping again in the second call
    plugin.start_grouping_if_necessary(venv)
    out2, _ = capsys.readouterr()
    assert out2 == ""


def test_start_grouping_ignores_isolated_build_env(capsys, mocker):
    envconfig = mocker.MagicMock()
    envconfig.envname = ".package"
    envconfig.description = "isolated packaging environment"
    envconfig.config.isolated_build_env = ".package"
    venv = mocker.MagicMock()
    venv.envconfig = envconfig

    # Start grouping in the first call
    plugin.start_grouping_if_necessary(venv)
    out, _ = capsys.readouterr()
    assert out == ""


@pytest.mark.parametrize(
    "config,expected",
    [
        (
            {
                "gh-actions": {
                    "python": """2.7: py27
3.5: py35
3.6: py36
3.7: py37, flake8"""
                }
            },
            {
                "python": {
                    "2.7": ["py27"],
                    "3.5": ["py35"],
                    "3.6": ["py36"],
                    "3.7": ["py37", "flake8"],
                },
                "env": {},
                "fail_on_no_env": False,
                "problem_matcher": True,
            },
        ),
        (
            {
                "gh-actions": {
                    "python": """2.7: py27
3.8: py38""",
                    "fail_on_no_env": "True",
                    "problem_matcher": "False",
                },
                "gh-actions:env": {
                    "PLATFORM": """ubuntu-latest: linux
macos-latest: macos
windows-latest: windows"""
                },
            },
            {
                "python": {
                    "2.7": ["py27"],
                    "3.8": ["py38"],
                },
                "env": {
                    "PLATFORM": {
                        "ubuntu-latest": ["linux"],
                        "macos-latest": ["macos"],
                        "windows-latest": ["windows"],
                    },
                },
                "fail_on_no_env": True,
                "problem_matcher": False,
            },
        ),
        (
            {"gh-actions": {}},
            {
                "python": {},
                "env": {},
                "fail_on_no_env": False,
                "problem_matcher": True,
            },
        ),
        (
            {},
            {
                "python": {},
                "env": {},
                "fail_on_no_env": False,
                "problem_matcher": True,
            },
        ),
    ],
)
def test_parse_config(config, expected):
    assert plugin.parse_config(config) == expected


@pytest.mark.parametrize(
    "config,version,environ,expected",
    [
        (
            {
                "python": {
                    "2.7": ["py27", "flake8"],
                    "3.8": ["py38", "flake8"],
                },
                "unknown": {},
            },
            ["2.7", "2"],
            {},
            ["py27", "flake8"],
        ),
        # Get factors using less precise Python version
        (
            {
                "python": {
                    "2": ["py2", "flake8"],
                    "3": ["py3", "flake8"],
                },
                "unknown": {},
            },
            ["3.8", "3"],
            {},
            ["py3", "flake8"],
        ),
        # Get factors only from the most precise Python version
        (
            {
                "python": {
                    "2": ["py2", "flake8"],
                    "3": ["py3", "flake8"],
                    "3.10": ["py310"],
                },
                "unknown": {},
            },
            ["3.10", "3"],
            {},
            ["py310"],
        ),
        (
            {
                "python": {
                    "2.7": ["py27", "flake8"],
                    "3.8": ["py38", "flake8"],
                },
                "env": {
                    "SAMPLE": {
                        "VALUE1": ["fact1", "fact2"],
                        "VALUE2": ["fact3", "fact4"],
                    },
                },
            },
            ["2.7", "2"],
            {
                "SAMPLE": "VALUE1",
                "HOGE": "VALUE3",
            },
            ["py27-fact1", "py27-fact2", "flake8-fact1", "flake8-fact2"],
        ),
        (
            {
                "python": {
                    "2.7": ["py27", "flake8"],
                    "3.8": ["py38", "flake8"],
                },
                "env": {
                    "SAMPLE": {
                        "VALUE1": ["fact1", "fact2"],
                        "VALUE2": ["fact3", "fact4"],
                    },
                    "HOGE": {
                        "VALUE3": ["fact5", "fact6"],
                        "VALUE4": ["fact7", "fact8"],
                    },
                },
            },
            ["2.7", "2"],
            {
                "SAMPLE": "VALUE1",
                "HOGE": "VALUE3",
            },
            [
                "py27-fact1-fact5",
                "py27-fact1-fact6",
                "py27-fact2-fact5",
                "py27-fact2-fact6",
                "flake8-fact1-fact5",
                "flake8-fact1-fact6",
                "flake8-fact2-fact5",
                "flake8-fact2-fact6",
            ],
        ),
        (
            {
                "python": {
                    "2.7": ["py27", "flake8"],
                    "3.8": ["py38", "flake8"],
                },
                "env": {
                    "SAMPLE": {
                        "VALUE1": ["django18", "flake8"],
                        "VALUE2": ["django18"],
                    },
                },
            },
            ["2.7", "2"],
            {
                "SAMPLE": "VALUE1",
                "HOGE": "VALUE3",
            },
            [
                "py27-django18",
                "py27-flake8",
                "flake8-django18",
                "flake8-flake8",
            ],
        ),
        (
            {
                "python": {
                    "2.7": ["py27", "flake8"],
                    "3.8": ["py38", "flake8"],
                },
                "env": {
                    "SAMPLE": {
                        "VALUE1": ["fact1", "fact2"],
                        "VALUE2": ["fact3", "fact4"],
                    },
                },
                "unknown": {},
            },
            ["2.7", "2"],
            {
                "SAMPLE": "VALUE3",
            },
            ["py27", "flake8"],
        ),
        (
            {
                "python": {
                    "2.7": ["py27", "flake8"],
                    "3.8": ["py38", "flake8"],
                },
                "env": {
                    "SAMPLE": {
                        "VALUE1": [],
                    },
                },
                "unknown": {},
            },
            ["3.8", "3"],
            {
                "SAMPLE": "VALUE2",
            },
            ["py38", "flake8"],
        ),
        (
            {
                "python": {
                    "3.8": ["py38", "flake8"],
                },
            },
            ["2.7", "2"],
            {},
            [],
        ),
        (
            {
                "python": {},
            },
            "3.8",
            {},
            [],
        ),
    ],
)
def test_get_factors(mocker, config, version, environ, expected):
    mocker.patch("tox_gh_actions.plugin.os.environ", environ)
    result = normalize_factors_list(plugin.get_factors(config, version))
    expected = normalize_factors_list(expected)
    assert result == expected


def normalize_factors_list(factors):
    """Utility to make it compare equality of a list of factors"""
    result = [tuple(sorted(f.split("-"))) for f in factors]
    result.sort()
    return result


@pytest.mark.parametrize(
    "envlist,factors,expected",
    [
        (
            ["py27", "py37", "flake8"],
            ["py37", "flake8"],
            ["py37", "flake8"],
        ),
        (
            ["py27", "py37", "flake8"],
            [],
            [],
        ),
        (
            [],
            ["py37", "flake8"],
            [],
        ),
        (
            ["py27-dj111", "py37-dj111", "py37-dj20", "flake8"],
            ["py37", "flake8"],
            ["py37-dj111", "py37-dj20", "flake8"],
        ),
        (
            ["py27-django18", "py37-django18", "flake8"],
            [
                "py27-django18",
                "py27-flake8",
                "flake8-django18",
                "flake8-flake8",
            ],
            ["py27-django18", "flake8"],
        ),
    ],
)
def test_get_envlist_from_factors(envlist, factors, expected):
    assert plugin.get_envlist_from_factors(envlist, factors) == expected


@pytest.mark.parametrize(
    "version,info,expected",
    [
        (
            "3.8.1 (default, Jan 22 2020, 06:38:00) \n[GCC 9.2.0]",
            (3, 8, 1, "final", 0),
            ["3.8", "3"],
        ),
        (
            "3.6.9 (1608da62bfc7, Dec 23 2019, 10:50:04)\n"
            "[PyPy 7.3.0 with GCC 7.3.1 20180303 (Red Hat 7.3.1-5)]",
            (3, 6, 9, "final", 0),
            ["pypy-3.6", "pypy-3", "pypy3"],
        ),
        (
            "2.7.13 (724f1a7d62e8, Dec 23 2019, 15:36:24)\n"
            "[PyPy 7.3.0 with GCC 7.3.1 20180303 (Red Hat 7.3.1-5)]",
            (2, 7, 13, "final", 42),
            ["pypy-2.7", "pypy-2", "pypy2"],
        ),
    ],
)
def test_get_version_keys(mocker, version, info, expected):
    mocker.patch("tox_gh_actions.plugin.sys.version", version)
    mocker.patch("tox_gh_actions.plugin.sys.version_info", info)
    assert plugin.get_python_version_keys() == expected


def test_get_version_keys_on_pyston(mocker):
    mocker.patch(
        "tox_gh_actions.plugin.sys.pyston_version_info",
        (2, 2, 0, "final", 0),
        create=True,  # For non-Pyston implementation
    )
    mocker.patch(
        "tox_gh_actions.plugin.sys.version",
        "3.8.8 (heads/rel2.2:6287d61, Apr 29 2021, 15:46:12)\n"
        "[Pyston 2.2.0, GCC 9.3.0]",
    )
    mocker.patch(
        "tox_gh_actions.plugin.sys.version_info",
        (3, 8, 8, "final", 0),
    )
    assert plugin.get_python_version_keys() == ["pyston-3.8", "pyston-3"]


@pytest.mark.parametrize(
    "environ,expected",
    [
        ({"GITHUB_ACTIONS": "true"}, True),
        ({"GITHUB_ACTIONS": "false"}, False),
        ({}, False),
    ],
)
def test_is_running_on_actions(mocker, environ, expected):
    mocker.patch("tox_gh_actions.plugin.os.environ", environ)
    assert plugin.is_running_on_actions() == expected


def is_running_on_container_returns_false_on_non_linux(mocker):
    mocker.patch("tox_gh_actions.plugin.os.path.exists", False)
    assert not plugin.is_running_on_container()


def is_running_on_container_returns_false_on_linux_host(mocker):
    mocker.patch("tox_gh_actions.plugin.os.path.exists", True)
    mock_open = mocker.mock_open(
        read_data="""12:perf_event:/
11:devices:/init.scope
10:cpu,cpuacct:/init.scope
9:freezer:/
8:pids:/init.scope
7:memory:/init.scope
6:cpuset:/
5:hugetlb:/
4:blkio:/init.scope
3:net_cls,net_prio:/
2:rdma:/
1:name=systemd:/init.scope
0::/init.scope"""
    )
    mocker.patch("tox_gh_actions.plugin.open", mock_open)
    assert plugin.is_running_on_container()


def is_running_on_container_returns_true_on_linux_container(mocker):
    mocker.patch("tox_gh_actions.plugin.os.path.exists", True)
    mock_open = mocker.mock_open(
        read_data="""12:pids:/actions_job/3d81
11:net_cls,net_prio:/actions_job/3d81
10:devices:/actions_job/3d81
9:freezer:/actions_job/3d81
8:cpuset:/actions_job/3d81
7:cpu,cpuacct:/actions_job/3d81
6:memory:/actions_job/3d81
5:blkio:/actions_job/3d81
4:perf_event:/actions_job/3d81
3:rdma:/
2:hugetlb:/actions_job/3d81
1:name=systemd:/actions_job/3d81
0::/system.slice/containerd.service"""
    )
    mocker.patch("tox_gh_actions.plugin.open", mock_open)
    assert plugin.is_running_on_container()


@pytest.mark.parametrize(
    "environ,parallel,parallel_live,expected",
    [
        ({"GITHUB_ACTIONS": "true"}, 0, False, True),
        ({"GITHUB_ACTIONS": "true"}, 1, False, True),
        ({"GITHUB_ACTIONS": "true"}, 8, False, True),
        ({"GITHUB_ACTIONS": "true"}, 0, True, True),
        ({"GITHUB_ACTIONS": "true"}, 1, True, True),
        ({"GITHUB_ACTIONS": "true"}, 8, True, False),
        ({"GITHUB_ACTIONS": "true"}, 0, False, True),
        ({"GITHUB_ACTIONS": "false"}, 0, False, False),
        ({"GITHUB_ACTIONS": "false"}, 8, False, False),
        ({"GITHUB_ACTIONS": "false"}, 0, True, False),
        ({"GITHUB_ACTIONS": "false"}, 8, True, False),
    ],
)
def test_is_log_grouping_enabled(mocker, environ, parallel, parallel_live, expected):
    mocker.patch("tox_gh_actions.plugin.os.environ", environ)
    config = mocker.MagicMock()
    config.option.parallel = parallel
    config.option.parallel_live = parallel_live
    assert plugin.is_log_grouping_enabled(config) == expected


@pytest.mark.parametrize(
    "option_env,environ,expected",
    [
        (None, {"TOXENV": "flake8"}, True),
        (["py27,py38"], {}, True),
        (["py27", "py38"], {}, True),
        (["py27"], {"TOXENV": "flake8"}, True),
        (None, {}, False),
    ],
)
def test_is_env_specified(mocker, option_env, environ, expected):
    mocker.patch("tox_gh_actions.plugin.os.environ", environ)
    option = mocker.MagicMock()
    option.env = option_env
    config = Config(None, option, None, mocker.MagicMock(), [])
    assert plugin.is_env_specified(config) == expected
