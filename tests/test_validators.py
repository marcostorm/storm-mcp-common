import pytest

from storm_mcp_common.validators import (
    is_safe_name,
    validate_container_name,
    validate_identifier,
    validate_loja_name,
    validate_run_id,
    validate_tag,
)


class TestIsSafeName:
    def test_alphanumeric(self):
        assert is_safe_name("abc123")

    def test_with_default_extras(self):
        assert is_safe_name("my-container_1.0")

    def test_empty_rejected(self):
        assert not is_safe_name("")

    def test_dot_outside_extras_rejected(self):
        # loja não aceita dot
        assert not is_safe_name("my.loja", extra_chars="-_")

    @pytest.mark.parametrize(
        "payload",
        [
            "a b",       # espaço
            "a;b",       # command chain
            "a&b",       # background
            "a|b",       # pipe
            "a>b",       # redirect
            "a/b",       # path separator
            "a\\b",      # escape
            "a$b",       # var expansion
            "a`b",       # command substitution
            "a'b",       # single quote
            'a"b',       # double quote
            "a\nb",      # newline
            "\x00",      # null byte
        ],
    )
    def test_rejects_shell_metachars(self, payload):
        assert not is_safe_name(payload)


class TestContainerName:
    def test_accepts_normal(self):
        validate_container_name("loja-demo-app-1")

    def test_accepts_dots(self):
        validate_container_name("app.v2")

    def test_rejects_shell_meta(self):
        with pytest.raises(ValueError, match="container"):
            validate_container_name("a;b")


class TestLojaName:
    def test_rejects_dot(self):
        with pytest.raises(ValueError, match="loja"):
            validate_loja_name("my.loja")

    def test_accepts_dash_underscore(self):
        validate_loja_name("loja_demo-1")

    def test_rejects_slash(self):
        with pytest.raises(ValueError):
            validate_loja_name("../etc/passwd")


class TestTag:
    def test_accepts_timestamp(self):
        validate_tag("20261105-1430")

    def test_accepts_semver(self):
        validate_tag("v1.2.3")

    def test_rejects_slash_breaks_sed(self):
        # Garantia explícita: tags que quebrariam o `sed -i` do deploy.sh
        with pytest.raises(ValueError, match="tag"):
            validate_tag("a/b")


class TestRunId:
    def test_accepts_timestamped(self):
        validate_run_id("deploy-loja-demo-20261105-143000")

    def test_rejects_dot(self):
        with pytest.raises(ValueError, match="run_id"):
            validate_run_id("deploy.run.1")


class TestIdentifier:
    def test_accepts_default_extras(self):
        validate_identifier("storm-commerce.v1_rc")

    def test_rejects_space(self):
        with pytest.raises(ValueError, match="identificador"):
            validate_identifier("foo bar")
