# storm-mcp-common

Helpers compartilhados pelos MCPs do Storm Lab. Centraliza lógica que antes
estava duplicada em cada MCP (validators de nome, env parsing, etc.).

## Instalar num consumidor

Via path local (editable, ótimo pra dev):

```bash
cd ~/workspace/<seu-mcp>
.venv/bin/pip install -e ../storm-mcp-common
```

E declara no `pyproject.toml` do consumidor:

```toml
dependencies = [
    "storm-mcp-common",
    # ...
]
```

## API

### `validators`

```python
from storm_mcp_common import (
    validate_container_name,  # alfanum + -_.
    validate_loja_name,       # alfanum + -_ (sem dot)
    validate_tag,             # alfanum + -_.
    validate_run_id,          # alfanum + -_
    validate_identifier,      # alfanum + -_. (genérico)
    validate_name,            # customizável (kind, extra_chars)
    is_safe_name,             # predicate (True/False)
)
```

Todos levantam `ValueError` com mensagem incluindo `kind`.

### `env`

```python
from storm_mcp_common import require_env, int_env, bool_env

token = require_env("TELEGRAM_BOT_TOKEN")  # RuntimeError se vazio/ausente
interval = int_env("INTERVAL_SECONDS", default=1800)
verbose = bool_env("VERBOSE", default=False)
```

## Rodar testes

```bash
.venv/bin/pip install -e '.[dev]'
.venv/bin/pytest
```
