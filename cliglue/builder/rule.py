from typing import List, Any, Set, Optional, TypeVar

from dataclasses import dataclass, field

from .typedef import Action, ChoiceProvider, TypeOrParser


@dataclass
class CliRule(object):
    pass


@dataclass
class KeywordRule(CliRule):
    keywords: Set[str] = field(default_factory=lambda: set())


@dataclass
class HelpRule(CliRule):
    help: str = None


@dataclass
class DefaultActionRule(CliRule):
    run: Action = None


@dataclass
class ParentRule(KeywordRule):
    run: Action = None
    subrules: List['CliRule'] = field(default_factory=lambda: [])

    def has(self, *subrules: CliRule) -> 'ParentRule':
        self.subrules += subrules
        return self


@dataclass
class SubcommandRule(ParentRule, HelpRule):
    pass


@dataclass
class PrimaryOptionRule(ParentRule, HelpRule):
    pass


@dataclass
class FlagRule(HelpRule, KeywordRule):
    pass


@dataclass
class ValueRule(CliRule):
    name: Optional[str] = None
    required: bool = False
    default: Any = None
    type: TypeOrParser = Any
    choices: ChoiceProvider = None


@dataclass
class ParameterRule(HelpRule, ValueRule, KeywordRule):
    pass


@dataclass
class PositionalArgumentRule(HelpRule, ValueRule):
    pass


# TODO parse allarguments with types the same as the positional ones
@dataclass
class AllArgumentsRule(CliRule):
    name: str
    joined_with: str


TCliRule = TypeVar('TCliRule', bound=CliRule)
