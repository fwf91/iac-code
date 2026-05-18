"""Parse shell commands into structured ASTs via tree-sitter (bash grammar)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

import tree_sitter_bash as tsbash
from tree_sitter import Language, Node, Parser

from iac_code.i18n import _

DANGEROUS_BUILTINS = frozenset({"eval", "exec", "source", "."})

_BASH_LANGUAGE = Language(tsbash.language())
_parser = Parser(_BASH_LANGUAGE)

_TOO_COMPLEX_TYPES = frozenset({"command_substitution", "process_substitution", "subshell"})


@dataclass
class SimpleCommand:
    text: str
    argv: list[str] = field(default_factory=list)
    redirects: list[str] = field(default_factory=list)


@dataclass
class ParseResult:
    kind: Literal["simple", "too_complex", "parse_error"]
    commands: list[SimpleCommand] = field(default_factory=list)
    reason: str = ""


def parse_command(command: str) -> ParseResult:
    source = command.encode("utf-8")
    tree = _parser.parse(source)
    root = tree.root_node

    if root.has_error or _tree_contains_error(root):
        return ParseResult(kind="parse_error", reason=_("parse error"))

    if _scan_too_complex(root, source):
        return ParseResult(kind="too_complex", reason=_("unsupported shell construct"))

    commands = _extract_simple_commands(root, source)
    return ParseResult(kind="simple", commands=commands)


def _node_text(node: Node, source: bytes) -> str:
    return source[node.start_byte : node.end_byte].decode("utf-8", errors="replace")


def _tree_contains_error(node: Node) -> bool:
    if node.type == "ERROR" or node.is_missing:
        return True
    for child in node.children:
        if _tree_contains_error(child):
            return True
    return False


def _strip_outer_shell_quotes(s: str) -> str:
    if len(s) >= 2 and s[0] == s[-1] and s[0] in {'"', "'"}:
        return s[1:-1]
    return s


def _argv_text_from(node: Node, source: bytes) -> str:
    kind = node.type
    if kind == "concatenation":
        return "".join(_argv_text_from(ch, source) for ch in node.named_children)
    if kind == "command_name":
        return "".join(_argv_text_from(ch, source) for ch in node.named_children)
    if kind in {"string", "raw_string"}:
        return _strip_outer_shell_quotes(_node_text(node, source))
    if kind in {"word", "simple_expansion", "number", "declare"}:
        return _node_text(node, source)
    return ""


def _command_argv(command_node: Node, source: bytes) -> list[str]:
    argv: list[str] = []
    for ch in command_node.named_children:
        if ch.type == "variable_assignment":
            continue
        if ch.type == "command_name":
            frag = _argv_text_from(ch, source)
            if frag:
                argv.append(frag)
        elif ch.type in {"word", "string", "raw_string", "concatenation", "simple_expansion", "number"}:
            frag = _argv_text_from(ch, source)
            if frag:
                argv.append(frag)
    return argv


def _declaration_argv(decl_node: Node, source: bytes) -> list[str]:
    argv: list[str] = []
    for ch in decl_node.named_children:
        if ch.type == "variable_assignment":
            argv.append(_node_text(ch, source))
        elif ch.type in {"declare", "word", "string", "raw_string", "concatenation", "simple_expansion", "number"}:
            frag = _argv_text_from(ch, source)
            if frag:
                argv.append(frag)
    return argv


def _command_invoked_name(command_node: Node, source: bytes) -> str | None:
    for ch in command_node.named_children:
        if ch.type == "command_name":
            raw = _argv_text_from(ch, source).strip()
            if not raw:
                return None
            return raw.split(None, 1)[0]
    return None


def _scan_too_complex(node: Node, source: bytes) -> bool:
    if node.type in _TOO_COMPLEX_TYPES:
        return True
    if node.type == "expansion" and "`" in _node_text(node, source):
        return True
    if node.type == "command":
        name = _command_invoked_name(node, source)
        if name is not None and name in DANGEROUS_BUILTINS:
            return True
    for child in node.children:
        if _scan_too_complex(child, source):
            return True
    return False


def _build_simple_command(
    node: Node,
    source: bytes,
    *,
    redirects: list[str],
    text_override: str | None = None,
) -> SimpleCommand:
    text = text_override if text_override is not None else _node_text(node, source)
    return SimpleCommand(text=text, argv=_command_argv(node, source), redirects=list(redirects))


def _extract_redirected_statement(node: Node, source: bytes) -> list[SimpleCommand]:
    redirects: list[str] = []
    body: Node | None = None
    for ch in node.named_children:
        if "redirect" in ch.type:
            redirects.append(_node_text(ch, source))
        elif body is None:
            body = ch
    if body is None:
        return []
    if body.type == "command":
        return [_build_simple_command(body, source, redirects=redirects, text_override=_node_text(node, source))]
    # Body is a compound (list, pipeline, etc.) — recurse to collect subcommands
    # and attach the redirects to the last subcommand (matching bash semantics).
    inner = _collect_commands(body, source)
    if inner and redirects:
        last = inner[-1]
        inner[-1] = SimpleCommand(text=last.text, argv=list(last.argv), redirects=list(last.redirects) + redirects)
    return inner


def _extract_simple_commands(root: Node, source: bytes) -> list[SimpleCommand]:
    return _collect_commands(root, source)


def _collect_commands(node: Node, source: bytes) -> list[SimpleCommand]:
    kind = node.type
    if kind in {"program", "list", "pipeline", "compound_statement"}:
        out: list[SimpleCommand] = []
        for ch in node.named_children:
            out.extend(_collect_commands(ch, source))
        return out
    if kind == "redirected_statement":
        return _extract_redirected_statement(node, source)
    if kind == "command":
        return [_build_simple_command(node, source, redirects=[])]
    if kind == "declaration_command":
        return [SimpleCommand(text=_node_text(node, source), argv=_declaration_argv(node, source))]

    out = []
    for ch in node.named_children:
        out.extend(_collect_commands(ch, source))
    return out
