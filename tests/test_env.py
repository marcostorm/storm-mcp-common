import pytest

from storm_mcp_common.env import bool_env, int_env, require_env


class TestRequireEnv:
    def test_returns_value_when_set(self, monkeypatch):
        monkeypatch.setenv("STORM_TEST_FOO", "bar")
        assert require_env("STORM_TEST_FOO") == "bar"

    def test_raises_when_missing(self, monkeypatch):
        monkeypatch.delenv("STORM_TEST_FOO", raising=False)
        with pytest.raises(RuntimeError, match="STORM_TEST_FOO"):
            require_env("STORM_TEST_FOO")

    def test_empty_counts_as_missing(self, monkeypatch):
        monkeypatch.setenv("STORM_TEST_FOO", "")
        with pytest.raises(RuntimeError):
            require_env("STORM_TEST_FOO")


class TestIntEnv:
    def test_default_when_missing(self, monkeypatch):
        monkeypatch.delenv("STORM_TEST_INT", raising=False)
        assert int_env("STORM_TEST_INT", 42) == 42

    def test_parses_set_value(self, monkeypatch):
        monkeypatch.setenv("STORM_TEST_INT", "7")
        assert int_env("STORM_TEST_INT", 42) == 7

    def test_raises_on_non_numeric(self, monkeypatch):
        monkeypatch.setenv("STORM_TEST_INT", "foo")
        with pytest.raises(ValueError):
            int_env("STORM_TEST_INT", 42)


class TestBoolEnv:
    @pytest.mark.parametrize(
        "val,expected",
        [
            ("1", True), ("true", True), ("TRUE", True),
            ("yes", True), ("on", True),
            ("0", False), ("false", False), ("no", False), ("off", False),
        ],
    )
    def test_canonical(self, monkeypatch, val, expected):
        monkeypatch.setenv("STORM_TEST_BOOL", val)
        assert bool_env("STORM_TEST_BOOL", default=not expected) is expected

    def test_empty_uses_default(self, monkeypatch):
        monkeypatch.setenv("STORM_TEST_BOOL", "")
        assert bool_env("STORM_TEST_BOOL", default=True) is True
        assert bool_env("STORM_TEST_BOOL", default=False) is False

    def test_missing_uses_default(self, monkeypatch):
        monkeypatch.delenv("STORM_TEST_BOOL", raising=False)
        assert bool_env("STORM_TEST_BOOL", default=True) is True

    def test_unknown_uses_default(self, monkeypatch):
        # valor não-reconhecido cai pro default (não lança)
        monkeypatch.setenv("STORM_TEST_BOOL", "maybe")
        assert bool_env("STORM_TEST_BOOL", default=False) is False
        assert bool_env("STORM_TEST_BOOL", default=True) is True
