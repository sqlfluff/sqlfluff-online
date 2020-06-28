"""Wrappers around sqlfluff CLI to make things easy.

One day I should learn about the fluff python API enough to not need subprocesses.
"""
import json
import subprocess
import typing

from sqlfluff.rules.std import std_rule_set

VALID_RULES = std_rule_set._register
VALID_DIALECTS = (
    "ansi",
    "bigquery",
    "mysql",
    "teradata",
    "postgres",
    "snowflake",
)


def is_valid_dialect(dialect: str) -> bool:
    """Check that the Dialect is valid."""
    return dialect.strip().lower() in VALID_DIALECTS


def is_valid_rule(rule: str) -> bool:
    """Check if a rule is valid."""
    return rule.strip().upper() in VALID_RULES


def append_dialect_to_command(command: list, dialect: str) -> list:
    """Sanitize the dialect and append to a command object."""
    if dialect is None:
        return command

    dialect = dialect.strip().lower().replace(" ", "")
    if not is_valid_dialect(dialect):
        raise ValueError(f"Invalid dialect: {dialect}.")

    return command + ["--dialect", dialect]


def append_rules_to_command(command: list, rules: typing.List[str]) -> list:
    """Sanitize the rules and append to a command object."""
    if rules is None:
        return command

    for rule in rules:
        if not is_valid_rule(rule):
            raise ValueError(f"Invlid rule: {rule}.")

    return command + ["--rules", ",".join([i.upper().strip() for i in rules])]


def run_with_stdin(command: list, stdin: str) -> str:
    """Run a command and pass in some data as stdin. Return the stdout."""
    p = subprocess.Popen(
        command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = p.communicate(input=stdin.encode())
    p.kill()

    if stderr:
        raise RuntimeError(stderr.decode())
    return stdout.decode()


def lint(sql: str, dialect: str = None, rules: typing.List[str] = None):
    """Run the linter in a subprocess and return the stdout."""
    command = ["sqlfluff", "lint", "-", "--format", "json"]
    command = append_dialect_to_command(command, dialect)
    command = append_rules_to_command(command, rules)
    out = run_with_stdin(command, sql)
    return json.loads(out)


def fix(sql: str, dialect: str = None, rules: typing.List[str] = None):
    """Run the fixer in a subprocess and return the stdout."""
    rules = rules or list(VALID_RULES.keys())
    command = ["sqlfluff", "fix", "-"]
    command = append_dialect_to_command(command, dialect)
    command = append_rules_to_command(command, rules)
    out = run_with_stdin(command, sql)
    return out
