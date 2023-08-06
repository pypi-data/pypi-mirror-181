"""
This file is created by "jeffrey.starr@ztoztechnologies.com".

This file contains some modification aimed at fixing bugs and improving the dateinfer library.
The newlines/modification line are preceded with comments indicating the purpose.
"""

import collections
import itertools
import string
import calendar
import re
import pytz

class If(object):
    """
    Top-level rule
    """

    def __init__(self, condition, action):
        """
        Initialize the rule with a condition clause and an action clause that will be executed
        if condition clause is true.
        """
        self.condition = condition
        self.action = action

    def execute(self, elem_list):
        """
        If condition, return a new elem_list provided by executing action.
        """
        if self.condition.is_true(elem_list):
            return self.action.act(elem_list)
        else:
            return elem_list


class ConditionClause(object):
    """
    Abstract class for a condition clause
    """

    def is_true(self, elem_list):
        """
        Return true if condition is true for the given input.
        """
        raise NotImplementedError()


class ActionClause(object):
    """
    Abstract class for an action clause
    """

    def act(self, elem_list):
        """
        Return a new instance of elem_list permuted by the action
        """
        raise NotImplementedError()


class And(ConditionClause):
    """
    Returns true if all conditions are true.
    """

    def __init__(self, *clauses):
        self.clauses = clauses

    def is_true(self, elem_list):
        for clause in self.clauses:
            if not clause.is_true(elem_list):
                return False
        return True


class Contains(ConditionClause):
    """
    Returns true if all requirements are found in the input
    """

    def __init__(self, *requirements):
        self.requirements = requirements

    def is_true(self, elem_list):
        for requirement in self.requirements:
            if requirement not in elem_list:
                return False
        return True


class Duplicate(ConditionClause):
    """
    Returns true if there is more than one instance of elem in elem_list.
    """

    def __init__(self, elem):
        self.elem = elem

    def is_true(self, elem_list):
        return elem_list.count(self.elem) > 1


class KeepOriginal(object):
    """
    In sequences, this stands for 'keep the original value'
    """

    pass


class Next(ConditionClause):
    """
    Return true if A and B are found next to each other in the elem_list (with zero or more Filler elements
    between them).
    """

    def __init__(self, a_elem, b_elem):
        self.a_elem = a_elem
        self.b_elem = b_elem

    def is_true(self, elem_list):
        a_positions = []
        b_positions = []
        for index, elem in enumerate(elem_list):
            if elem == self.a_elem:
                a_positions.append(index)
            elif elem == self.b_elem:
                b_positions.append(index)

        for a_position in a_positions:
            for b_position in b_positions:
                left = min(a_position, b_position)
                right = max(a_position, b_position)
                between = elem_list[left + 1 : right - 1]
                if len(between) == 0 or all([type(e) is Filler] for e in between):
                    return True
        return False


class Sequence(ConditionClause):
    """
    Returns true if the given sequence is found in elem_list. The sequence consists of date elements
    and wild cards.

    Wild cards:
    . (period): Any single date element (including Filler)
    """

    def __init__(self, *sequence):
        self.sequence = sequence

    def is_true(self, elem_list):
        seq_pos = (
            0
        )  # if we find every element in sequence (pos == length(self.sequence), then a match is found

        for elem in elem_list:
            if self.match(elem, self.sequence[seq_pos]):
                seq_pos += 1
                if seq_pos == len(self.sequence):
                    return True
            else:
                seq_pos = 0  # reset if we exit sequence
        return False

    @staticmethod
    def match(elem, seq_expr):
        """
        Return True if elem (an element of elem_list) matches seq_expr, an element in self.sequence
        """
        if type(seq_expr) is str:  # wild-card
            if seq_expr == ".":  # match any element
                return True
            elif seq_expr == "\d":
                return elem.is_numerical()
            elif seq_expr == "\D":
                return not elem.is_numerical()
            else:  # invalid wild-card specified
                raise LookupError("{0} is not a valid wild-card".format(seq_expr))
        else:  # date element
            return elem == seq_expr

    @staticmethod
    def find(find_seq, elem_list):
        """
        Return the first position in elem_list where find_seq starts
        """
        seq_pos = 0
        for index, elem in enumerate(elem_list):
            if Sequence.match(elem, find_seq[seq_pos]):
                seq_pos += 1
                if seq_pos == len(find_seq):  # found matching sequence
                    return index - seq_pos + 1
            else:  # exited sequence
                seq_pos = 0
        raise LookupError("Failed to find sequence in elem_list")


class Swap(ActionClause):
    """
    Returns elem_list with one element replaced by another
    """

    def __init__(self, remove_me, insert_me):
        self.remove_me = remove_me
        self.insert_me = insert_me

    def act(self, elem_list):
        copy = elem_list[:]
        pos = copy.index(self.remove_me)
        copy[pos] = self.insert_me
        return copy


class SwapDuplicateWhereSequenceNot(ActionClause):
    """
    Replace remove_me with insert_me in the case where remove_me is not part of the sequence.
    """

    def __init__(self, remove_me, insert_me, seq):
        self.remove_me = remove_me
        self.insert_me = insert_me
        self.seq = seq

    def act(self, elem_list):
        copy = elem_list[:]

        start_pos = Sequence.find(self.seq, copy)
        end_pos = start_pos + len(
            self.seq
        )  # do not replace within [start_pos, end_pos)

        for index, elem in enumerate(copy):
            if start_pos <= index < end_pos:  # within sequence
                continue
            else:  # outside of sequence
                if elem == self.remove_me:
                    copy[index] = self.insert_me
                    return copy

        raise LookupError(
            "Failed to find element {0} to replace with {1} in {2} ignoring {3} between [{4},{5})".format(
                self.remove_me, self.insert_me, copy, self.seq, start_pos, end_pos
            )
        )


class SwapSequence(ActionClause):
    """
    Returns elem_list with sequence replaced with another sequence
    """

    def __init__(self, find_seq, swap_seq):
        self.find_seq = find_seq
        self.swap_seq = swap_seq

    def act(self, elem_list):
        copy = elem_list[:]

        start_pos = Sequence.find(self.find_seq, copy)
        for index, replacement in enumerate(self.swap_seq):
            if replacement is not KeepOriginal:
                copy[start_pos + index] = replacement

        # If we intend to delete items, we put None in the swap_seq and then clean up the list here
        while None in copy:
            copy.remove(None)

        return copy


class DateElement:
    """
    Abstract class for a date element, a portion of a valid date/time string
    Inheriting classes should implement a string 'directive' field that provides the relevant
    directive for the datetime.strftime/strptime method.
    """

    directive = None

    def __eq__(self, other):
        if other is None:
            return False
        return self.directive == other.directive

    def __hash__(self):
        return self.directive.__hash__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return self.directive

    def __str__(self):
        return self.directive

    @staticmethod
    def is_numerical():
        """
        Return true if the written representation of the element are digits
        """
        raise NotImplementedError("is_numerical")


class AMPM(DateElement):
    """AM | PM"""

    directive = "%p"

    @staticmethod
    def is_match(token):
        return token in ("AM", "PM", "am", "pm")

    @staticmethod
    def is_numerical():
        return False


class DayOfMonth(DateElement):
    """1 .. 31"""

    directive = "%d"

    @staticmethod
    def is_match(token):
        try:
            day = int(token)
            return 1 <= day <= 31
        except ValueError:
            return False

    @staticmethod
    def is_numerical():
        return True


class Filler(DateElement):
    """
    A special date class, filler matches everything. Filler is usually used for matches of
    whitespace and punctuation.
    """

    def __init__(self, filler):
        self.directive = filler.replace("%", "%%")  # escape %

    @staticmethod
    def is_match(_):
        return True

    @staticmethod
    def is_numerical():
        return False


class Hour12(DateElement):
    """1 .. 12 (zero padding accepted)"""

    directive = "%I"

    @staticmethod
    def is_match(token):
        try:
            hour = int(token)
            return 1 <= hour <= 12
        except ValueError:
            return False

    @staticmethod
    def is_numerical():
        return True


class Hour24(DateElement):
    """00 .. 23"""

    directive = "%H"

    @staticmethod
    def is_match(token):
        try:
            hour = int(token)
            return 0 <= hour <= 23
        except ValueError:
            return False

    @staticmethod
    def is_numerical():
        return True


class Minute(DateElement):
    """00 .. 59"""

    directive = "%M"

    @staticmethod
    def is_match(token):
        try:
            minute = int(token)
            return 0 <= minute <= 59
        except ValueError:
            return False

    @staticmethod
    def is_numerical():
        return True


class MonthNum(DateElement):
    """1 .. 12"""

    directive = "%m"

    @staticmethod
    def is_match(token):
        try:
            month = int(token)
            return 1 <= month <= 12
        except ValueError:
            return False

    @staticmethod
    def is_numerical():
        return True


class MonthTextLong(DateElement):
    """January, February, ..., December
    Uses calendar.month_name to provide localization
    """

    directive = "%B"

    @staticmethod
    def is_match(token):
        return token in calendar.month_name

    @staticmethod
    def is_numerical():
        return False


class MonthTextShort(DateElement):
    """Jan, Feb, ... Dec
    Uses calendar.month_abbr to provide localization
    """

    directive = "%b"

    @staticmethod
    def is_match(token):
        return token in calendar.month_abbr

    @staticmethod
    def is_numerical():
        return False


class Second(DateElement):
    """00 .. 60
    Normally, seconds range from 0 to 59. In the case of a leap second, the second value may be 60.
    """

    directive = "%S"

    @staticmethod
    def is_match(token):
        try:
            second = int(token)
            return 0 <= second <= 60
        except ValueError:
            return False

    @staticmethod
    def is_numerical():
        return True


class Timezone(DateElement):
    """IANA common timezones (e.g. UTC, EST, US/Eastern, ...)"""

    directive = "%Z"

    @staticmethod
    def is_match(token):
        return token in pytz.all_timezones_set

    @staticmethod
    def is_numerical():
        return False


class UTCOffset(DateElement):
    """UTC offset +0400 -1130"""

    directive = "%z"

    @staticmethod
    def is_match(token):
        # technically offset_re should be:
        # ^[-\+]\d\d:?(\d\d)?$
        # but python apparently only uses the +/-hhmm format
        # A rule will catch the preceding + and - and combine the two entries since punctuation and
        # numbers are separated by the tokenizer.
        offset_re = r"^\d\d\d\d$"
        return re.match(offset_re, token)

    @staticmethod
    def is_numerical():
        return False


class WeekdayLong(DateElement):
    """Sunday, Monday, ..., Saturday
    Uses calendar.day_name to provide localization
    """

    directive = "%A"

    @staticmethod
    def is_match(token):
        return token in calendar.day_name


class WeekdayShort(DateElement):
    """Sun, Mon, ... Sat
    Uses calendar.day_abbr to provide localization
    """

    directive = "%a"

    @staticmethod
    def is_match(token):
        return token in calendar.day_abbr

    @staticmethod
    def is_numerical():
        return False


class Year2(DateElement):
    """00 .. 99"""

    directive = "%y"

    @staticmethod
    def is_match(token):
        if len(token) != 2:
            return False
        try:
            year = int(token)
            return 0 <= year <= 99
        except ValueError:
            return False

    @staticmethod
    def is_numerical():
        return True


class Year4(DateElement):
    """0000 .. 9999"""

    directive = "%Y"

    @staticmethod
    def is_match(token):
        if len(token) != 4:
            return False
        try:
            _ = int(token)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_numerical():
        return True

# DATE_ELEMENTS is an ordered sequence of date elements, excluding the filler. It is ordered
# in descending "restrictivity".
# The order is a little loose since date element domains do not necessarily overlap (e.g., the
# range of Jan .. Dec is 12, but the domain is independent of hours 0 .. 23), but overall a lesser
# value should be preferred over a greater value.
# The RULES will be applied after the list is generated following these precedence rules.
DATE_ELEMENTS = (
    AMPM(),
    MonthNum(),
    Hour12(),
    Hour24(),
    DayOfMonth(),
    Minute(),
    Second(),
    Year2(),
    Year4(),
    UTCOffset(),
    MonthTextShort(),
    MonthTextLong(),
    WeekdayShort(),
    WeekdayLong(),
    Timezone(),
)

F = Filler  # short-hand to clarify rules
RULES = [
    If(Sequence(Year4, Year2), SwapSequence([Year4, Year2], [Year4, MonthNum])),
    If(
        Sequence(MonthNum, F("/"), r"\d", F("/"), Year4),
        SwapSequence(
            [MonthNum, F("/"), r"\d", F("/"), Year4],
            [MonthNum, F("/"), DayOfMonth, F("/"), Year4],
        ),
    ),
    If(
        Sequence(MonthNum, F("/"), r"\d", F("/"), Hour24),
        SwapSequence(
            [MonthNum, F("/"), r"\d", F("/"), Hour24],
            [MonthNum, F("/"), DayOfMonth, F("/"), Year2],
        ),
    ),
    If(
        Sequence(MonthNum, F("-"), r"\d", F("-"), Hour24),
        SwapSequence(
            [MonthNum, F("-"), r"\d", F("-"), Hour24],
            [MonthNum, F("-"), DayOfMonth, F("-"), Year2],
        ),
    ),
    If(
        Sequence(MonthNum, F("/"), r"\d", F("/"), MonthNum),
        SwapSequence(
            [MonthNum, F("/"), r"\d", F("/"), MonthNum],
            [MonthNum, F("/"), DayOfMonth, F("/"), Year2],
        ),
    ),
    If(
        Sequence(MonthNum, F("-"), r"\d", F("-"), MonthNum),
        SwapSequence(
            [MonthNum, F("-"), r"\d", F("-"), MonthNum],
            [MonthNum, F("-"), DayOfMonth, F("-"), Year2],
        ),
    ),
    If(
        Sequence(MonthNum, F(":"), r"\d", F(":"), r"\d"),
        SwapSequence(
            [MonthNum, F(":"), r"\d", F(":"), r"\d"],
            [Hour12, F(":"), Minute, F(":"), Second],
        ),
    ),
    If(
        Sequence(Hour24, F(":"), r"\d", F(":"), r"\d"),
        SwapSequence(
            [Hour24, F(":"), r"\d", F(":"), r"\d"],
            [Hour24, F(":"), Minute, F(":"), Second],
        ),
    ),
    If(
        Sequence(MonthNum, F(":"), r"\d", r"\D"),
        SwapSequence([MonthNum, F(":"), "."], [Hour12, F(":"), Minute]),
    ),
    If(
        Sequence(Hour24, F(":"), r"\d", r"\D"),
        SwapSequence([Hour24, F(":"), r"\d"], [Hour24, F(":"), Minute]),
    ),
    If(
        Sequence(MonthNum, F(":"), r"\d"),
        SwapSequence([MonthNum, F(":"), "."], [Hour24, F(":"), Minute]),
    ),
    If(
        And(Sequence(Hour12, F(":"), Minute), Contains(Hour24)),
        Swap(Hour24, DayOfMonth),
    ),
    If(
        And(Sequence(Hour12, F(":"), Minute), Duplicate(Hour12)),
        SwapDuplicateWhereSequenceNot(Hour12, MonthNum, (Hour12, F(":"))),
    ),
    If(
        And(Sequence(Hour24, F(":"), Minute), Duplicate(Hour24)),
        SwapDuplicateWhereSequenceNot(Hour24, DayOfMonth, [Hour24, F(":")]),
    ),
    If(Contains(MonthNum, MonthTextLong), Swap(MonthNum, DayOfMonth)),
    If(Contains(MonthNum, MonthTextShort), Swap(MonthNum, DayOfMonth)),
    If(
        Sequence(MonthNum, ".", Hour12),
        SwapSequence([MonthNum, ".", Hour12], [MonthNum, KeepOriginal, DayOfMonth]),
    ),
    If(
        Sequence(MonthNum, ".", Hour24),
        SwapSequence([MonthNum, ".", Hour24], [MonthNum, KeepOriginal, DayOfMonth]),
    ),
    If(
        Sequence(Hour12, ".", MonthNum),
        SwapSequence([Hour12, ".", MonthNum], [DayOfMonth, KeepOriginal, MonthNum]),
    ),
    If(
        Sequence(Hour24, ".", MonthNum),
        SwapSequence([Hour24, ".", MonthNum], [DayOfMonth, KeepOriginal, MonthNum]),
    ),
    If(Duplicate(MonthNum), Swap(MonthNum, DayOfMonth)),
    If(Sequence(F("+"), Year4), SwapSequence([F("+"), Year4], [UTCOffset, None])),
    If(
        Sequence(Second, F("-"), Year4),
        SwapSequence([Second, F("-"), Year4], [Second, UTCOffset, None]),
    ),
    If(
        Sequence(Minute, F("-"), Year4),
        SwapSequence([Minute, F("-"), Year4], [Minute, UTCOffset, None]),
    ),
    If(
        Sequence(Hour24, ".", r"\D"),
        SwapSequence([Hour24, ".", r"\D"], [DayOfMonth, KeepOriginal, KeepOriginal]),
    ),
    If(
        Sequence(DayOfMonth, ".", MonthNum, ".", DayOfMonth),
        SwapSequence(
            [DayOfMonth, ".", MonthNum, ".", DayOfMonth],
            [DayOfMonth, KeepOriginal, MonthNum, KeepOriginal, Year2],
        ),
    ),
    If(
        And(Duplicate(Minute), Contains(Hour24)),
        SwapDuplicateWhereSequenceNot(Minute, Second, [Minute]),
    ),
    If(And(Duplicate(DayOfMonth), Contains(MonthNum)), Swap(MonthNum, Year2)),
    If(
        Duplicate(DayOfMonth),
        SwapDuplicateWhereSequenceNot(DayOfMonth, MonthNum, [DayOfMonth]),
    ),
]


_alt_directives = {'%z': '%Y',
                   '%Y': '%z'}


def infer(examples, alt_rules=None):
    """
    Returns a datetime.strptime-compliant format string for parsing the *most likely* date format
    used in examples. examples is a list containing example date strings.
    """
    date_classes = _tag_most_likely(examples)

    if alt_rules:
        date_classes = _apply_rewrites(date_classes, alt_rules)
    else:
        date_classes = _apply_rewrites(date_classes, RULES)

    date_string = ""
    directives = []
    for date_class in date_classes:
        directive = date_class.directive
        if '%' in directive:
            if directive in directives:
                directive = _alt_directives.get(directive, directive)
            if directive in directives:
                continue
        directives.append(directive)
        date_string += directive

    return date_string


def _apply_rewrites(date_classes, rules):
    """
    Return a list of date elements by applying rewrites to the initial date element list
    """
    for rule in rules:
        date_classes = rule.execute(date_classes)

    return date_classes


def _mode(elems):
    """
    Find the mode (most common element) in list elems. If there are ties, this function returns the
    least value.
    If elems is an empty list, returns None.
    """
    if not elems:
        return None

    c = collections.Counter()
    c.update(elems)

    most_common = c.most_common(1)
    most_common.sort()
    return most_common[0][
        0
    ]  # most_common[0] is a tuple of key and count; no need for the count


def _most_restrictive(date_elems):
    """
    Return the date_elem that has the most restrictive range from date_elems
    """
    most_index = len(DATE_ELEMENTS)
    for date_elem in date_elems:
        if date_elem in DATE_ELEMENTS and DATE_ELEMENTS.index(date_elem) < most_index:
            most_index = DATE_ELEMENTS.index(date_elem)
    if most_index < len(DATE_ELEMENTS):
        return DATE_ELEMENTS[most_index]

    raise KeyError("No least restrictive date element found")


def _percent_match(date_classes, tokens):
    """
    For each date class, return the percentage of tokens that the class matched (floating point
    [0.0 - 1.0]).
    The returned value is a tuple of length patterns. Tokens should be a list.
    """
    match_count = [0] * len(date_classes)

    for i, date_class in enumerate(date_classes):
        for token in tokens:
            if date_class.is_match(token):
                match_count[i] += 1

    percentages = tuple([float(m) / len(tokens) for m in match_count])
    return percentages


def _tag_most_likely(examples):
    """
    Return a list of date elements by choosing the most likely element for a token within examples
    (context-free).
    """
    tokenized_examples = [_tokenize_by_character_class(example) for example in examples]

    # We currently need the tokenized_examples to all have the same length, so drop instances that
    # have a length that does not equal the mode of lengths within tokenized_examples
    token_lengths = [len(e) for e in tokenized_examples]
    token_lengths_mode = _mode(token_lengths)
    tokenized_examples = [
        example for example in tokenized_examples if len(example) == token_lengths_mode
    ]

    # Now, we iterate through the tokens, assigning date elements based on their likelihood.
    # In cases where the assignments are unlikely for all date elements, assign filler.
    most_likely = []
    for token_index in range(0, token_lengths_mode):
        tokens = [token[token_index] for token in tokenized_examples]
        probabilities = _percent_match(DATE_ELEMENTS, tokens)
        max_prob = max(probabilities)
        if max_prob < 0.5:
            most_likely.append(Filler(_mode(tokens)))
        else:
            if probabilities.count(max_prob) == 1:
                most_likely.append(DATE_ELEMENTS[probabilities.index(max_prob)])
            else:
                choices = []
                for index, prob in enumerate(probabilities):
                    if prob == max_prob:
                        choices.append(DATE_ELEMENTS[index])
                most_likely.append(_most_restrictive(choices))

    return most_likely


def _tokenize_by_character_class(s):
    """
    Return a list of strings by splitting s (tokenizing) by character class.
    For example:
    _tokenize_by_character_class('Sat Jan 11 19:54:52 MST 2014') =>
        ['Sat', ' ', 'Jan', ' ', '11', ' ', '19', ':', '54', ':', '52', ' ', 'MST', ' ', '2014']
    _tokenize_by_character_class('2013-08-14') => ['2013', '-', '08', '-', '14']
    """
    # Callables per character class. Return True/False depending on whether the character is in the
    # respective class.
    character_classes = [
        lambda x: x.isdigit(),
        lambda x: x.isalpha(),
        lambda x: x in string.punctuation,
        lambda x: x.isspace(),
    ]

    result = []
    rest = list(s)
    while rest:
        progress = False
        for part_of_class in character_classes:
            if part_of_class(rest[0]):
                progress = True
                token = ""
                for take_away in itertools.takewhile(part_of_class, rest[:]):
                    token += take_away
                    rest.pop(0)
                result.append(token)
                break
        if (
            not progress
        ):  # none of the character classes matched; unprintable character?
            result.append(rest[0])
            rest = rest[1:]

    return result