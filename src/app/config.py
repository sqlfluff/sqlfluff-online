"""Export global config variables."""
import sqlfluff

SQLFLUFF_VERSION = sqlfluff.__version__

VALID_DIALECTS = tuple(d.name for d in sqlfluff.list_dialects())

# dict mapping string rule names to descriptions
VALID_RULES = {r.code: r.description for r in sqlfluff.list_rules()}
