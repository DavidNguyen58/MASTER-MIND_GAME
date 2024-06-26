# The Back-End of the game

# The code is imported from https://cs50.harvard.edu/ai/2024/projects/1/knights/ in the logic file.


class Sentence:
    def evaluate(self, model: dict) -> bool:
        """Evaluates the logical sentence."""
        raise Exception("nothing to evaluate")

    def formula(self) -> str:
        """Returns string formula representing logical sentence."""
        return ""

    def symbols(self) -> set:
        """Returns a set of all symbols in the logical sentence."""
        return set()

    @classmethod
    def validate(cls, sentence) -> None:
        if not isinstance(sentence, Sentence):
            raise TypeError("must be a logical sentence")

    @classmethod
    def parenthesize(cls, s: str) -> str:
        """Parenthesizes an expression if not already parenthesized."""

        def balanced(s) -> bool:
            """Checks if a string has balanced parentheses."""
            count = 0
            for c in s:
                if c == "(":
                    count += 1
                elif c == ")":
                    if count <= 0:
                        return False
                    count -= 1
            return count == 0

        if (
            not len(s)
            or s.isalpha()
            or (s[0] == "(" and s[-1] == ")" and balanced(s[1:-1]))
        ):
            return s
        else:
            return f"({s})"


# Create a symbol for a sentence
class Symbol(Sentence):
    def __init__(self, name: str) -> None:
        self.name = name

    def __eq__(self, other) -> bool:
        return isinstance(other, Symbol) and self.name == other.name

    def __hash__(self) -> int:
        return hash(("symbol", self.name))

    def __repr__(self) -> str:
        return self.name

    def evaluate(self, model: dict) -> bool:
        try:
            return bool(model[self.name])
        except KeyError:
            raise Exception(f"variable {self.name} not in model")

    def formula(self) -> str:
        return self.name

    def symbols(self) -> set:
        return {self.name}


class Not(Sentence):
    def __init__(self, operand: Symbol) -> None:
        Sentence.validate(operand)
        self.operand = operand

    def __eq__(self, other) -> bool:
        return isinstance(other, Not) and self.operand == other.operand

    def __hash__(self) -> int:
        return hash(("not", hash(self.operand)))

    def __repr__(self) -> str:
        return f"Not({self.operand})"

    def evaluate(self, model: dict) -> bool:
        return not self.operand.evaluate(model)

    def formula(self) -> str:
        return "¬" + Sentence.parenthesize(self.operand.formula())

    def symbols(self) -> set:
        return self.operand.symbols()


class And(Sentence):
    def __init__(self, *conjuncts) -> None:
        for conjunct in conjuncts:
            Sentence.validate(conjunct)
        self.conjuncts = list(conjuncts)

    def __eq__(self, other) -> bool:
        return isinstance(other, And) and self.conjuncts == other.conjuncts

    def __hash__(self) -> int:
        return hash(("and", tuple(hash(conjunct) for conjunct in self.conjuncts)))

    def __repr__(self) -> str:
        conjunctions = ", ".join([str(conjunct) for conjunct in self.conjuncts])
        return f"And({conjunctions})"

    def add(self, conjunct) -> None:
        Sentence.validate(conjunct)
        self.conjuncts.append(conjunct)

    def evaluate(self, model) -> bool:
        return all(conjunct.evaluate(model) for conjunct in self.conjuncts)

    def formula(self) -> str:
        if len(self.conjuncts) == 1:
            return self.conjuncts[0].formula()
        return " ∧ ".join(
            [Sentence.parenthesize(conjunct.formula()) for conjunct in self.conjuncts]
        )

    def symbols(self) -> set:
        return set.union(*[conjunct.symbols() for conjunct in self.conjuncts])


class Or(Sentence):
    def __init__(self, *disjuncts) -> None:
        for disjunct in disjuncts:
            Sentence.validate(disjunct)
        self.disjuncts = list(disjuncts)

    def __eq__(self, other) -> bool:
        return isinstance(other, Or) and self.disjuncts == other.disjuncts

    def __hash__(self) -> int:
        return hash(("or", tuple(hash(disjunct) for disjunct in self.disjuncts)))

    def __repr__(self) -> str:
        disjuncts = ", ".join([str(disjunct) for disjunct in self.disjuncts])
        return f"Or({disjuncts})"

    def add(self, disjunct) -> None:
        Sentence.validate(disjunct)
        self.disjuncts.append(disjunct)

    def evaluate(self, model) -> bool:
        return any(disjunct.evaluate(model) for disjunct in self.disjuncts)

    def formula(self) -> str:
        if len(self.disjuncts) == 1:
            return self.disjuncts[0].formula()
        return " ∨  ".join(
            [Sentence.parenthesize(disjunct.formula()) for disjunct in self.disjuncts]
        )

    def symbols(self) -> set:
        return set.union(*[disjunct.symbols() for disjunct in self.disjuncts])


class Implication(Sentence):
    def __init__(self, antecedent, consequent) -> None:
        Sentence.validate(antecedent)
        Sentence.validate(consequent)
        self.antecedent = antecedent
        self.consequent = consequent

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, Implication)
            and self.antecedent == other.antecedent
            and self.consequent == other.consequent
        )

    def __hash__(self) -> int:
        return hash(("implies", hash(self.antecedent), hash(self.consequent)))

    def __repr__(self) -> str:
        return f"Implication({self.antecedent}, {self.consequent})"

    def evaluate(self, model) -> bool:
        return (not self.antecedent.evaluate(model)) or self.consequent.evaluate(model)

    def formula(self) -> str:
        antecedent = Sentence.parenthesize(self.antecedent.formula())
        consequent = Sentence.parenthesize(self.consequent.formula())
        return f"{antecedent} => {consequent}"

    def symbols(self) -> set:
        return set.union(self.antecedent.symbols(), self.consequent.symbols())


class Biconditional(Sentence):
    def __init__(self, left, right) -> None:
        Sentence.validate(left)
        Sentence.validate(right)
        self.left = left
        self.right = right

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, Biconditional)
            and self.left == other.left
            and self.right == other.right
        )

    def __hash__(self) -> int:
        return hash(("biconditional", hash(self.left), hash(self.right)))

    def __repr__(self) -> str:
        return f"Biconditional({self.left}, {self.right})"

    def evaluate(self, model) -> bool:
        return (self.left.evaluate(model) and self.right.evaluate(model)) or (
            not self.left.evaluate(model) and not self.right.evaluate(model)
        )

    def formula(self) -> str:
        left = Sentence.parenthesize(str(self.left))
        right = Sentence.parenthesize(str(self.right))
        return f"{left} <=> {right}"

    def symbols(self) -> set:
        return set.union(self.left.symbols(), self.right.symbols())


def model_check(knowledge, query):
    """Checks if knowledge base entails query."""

    def check_all(knowledge, query, symbols, model):
        """Checks if knowledge base entails query, given a particular model."""

        # If model has an assignment for each symbol
        if not symbols:

            # If knowledge base is true in model, then query must also be true
            if knowledge.evaluate(model):
                return query.evaluate(model)
            return True
        else:

            # Choose one of the remaining unused symbols
            remaining = symbols.copy()
            p = remaining.pop()

            # Create a model where the symbol is true
            model_true = model.copy()
            model_true[p] = True

            # Create a model where the symbol is false
            model_false = model.copy()
            model_false[p] = False

            # Ensure entailment holds in both models
            return check_all(knowledge, query, remaining, model_true) and check_all(
                knowledge, query, remaining, model_false
            )

    # Get all symbols in both knowledge and query
    symbols = set.union(knowledge.symbols(), query.symbols())

    # Check that knowledge entails query
    return check_all(knowledge, query, symbols, dict())
