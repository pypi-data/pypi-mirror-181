"""
Collected rules from RFC 2616.
https://www.rfc-editor.org/rfc/rfc2616.html

Though RFC 2616 is largely obsolete, some later RFCs, not obsolete, 
still incorporate grammar from RFC 2616; in particular, RFC 6265.
Here we collect grammar from RFC 2616 as needed for use with other RFC grammars.
"""


from abnf.parser import Rule as _Rule
from .misc import load_grammar_rules


@load_grammar_rules()
class Rule(_Rule):
    """Rule objects generated from ABNF in RFC 5234."""

    grammar = []
