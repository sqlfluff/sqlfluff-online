"""Export global config variables."""
import sqlfluff

SQLFLUFF_VERSION = sqlfluff.__version__

# manually updated on version bump
VALID_DIALECTS = (
    "ansi",
    "bigquery",
    "mysql",
    "teradata",
    "postgres",
    "snowflake",
    "exasol",
    "exasol_fs",
)


# dict mapping string rule names to descriptions
VALID_RULES = {
    r.code: r.description
    for r in sqlfluff.core.rules.std_rule_set.get_rulelist(sqlfluff.core.FluffConfig())
}
