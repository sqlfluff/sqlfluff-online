"""Export global config variables."""

import sqlfluff

SQLFLUFF_VERSION = sqlfluff.__version__

# Shared SQL character limit used by frontend and backend validation.
SQL_CHAR_LIMIT = 3000

VALID_DIALECTS = {d.label: d.name for d in sqlfluff.list_dialects()}

# dict mapping string rule names to descriptions
VALID_RULES = {r.code: r.description for r in sqlfluff.list_rules()}
