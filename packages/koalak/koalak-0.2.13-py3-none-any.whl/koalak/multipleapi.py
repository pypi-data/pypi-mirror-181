from inspect import _ParameterKind
from typing import Dict

import attr
import docstring_parser
from koalak import SubcommandParser
from koalak.decorators import optionalargs


@attr.s
class APIMethod:
    name = attr.ib()
    description = attr.ib()
    method = attr.ib()
    args = attr.ib()
    kwargs = attr.ib()


@attr.s
class APIParameter:
    name = attr.ib()
    description = attr.ib()
    default = attr.ib()
    annotation = attr.ib()


class BudgetManager:
    def __init__(self, money=1000):
        self.transactions = []
        self.money = money

    # API rest:  /api/v1/outcom/
    def outcom(self, cost: int, description: str = ""):
        """
        Args:
            cost(cost): lol
            description(str): haha
        """
        self.transactions.append(cost)
        self.money -= cost

    def show(self):
        for t in self.transactions:
            print(t)


import inspect

s = inspect.signature(BudgetManager.outcom)


class MultiAPI:
    def __init__(self, name):
        self.name = name
        self.methods: Dict[str, APIMethod] = {}
        self.maincli = None

    def build(self):
        self.build_cli()

    @optionalargs
    def add(
        self, method, *, name=None, description=None, http_method=None, help_group=None
    ):
        if name is None:
            name = method.__name__

        if name in self.methods:
            raise ValueError(f"Method {name} already exists")

        parsed_docstring = docstring_parser.parse(method.__doc__)
        if description is None:
            description = parsed_docstring.short_description

        args = []
        kwargs = {}
        signature = inspect.signature(method)
        for i, param in enumerate(signature.parameters.values()):
            if i == 0 and param.name == "self":
                continue
            api_param = APIParameter(
                param.name,
                description="",
                default=param.default,
                annotation=param.annotation,
            )
            if param.kind in [
                _ParameterKind.POSITIONAL_OR_KEYWORD,
                _ParameterKind.POSITIONAL_ONLY,
            ]:
                args.append(api_param)
            else:
                kwargs[param.name] = api_param

        method_api = APIMethod(
            name, method=method, description=description, args=args, kwargs=kwargs
        )
        self.methods[name] = method_api
        print(method_api)
        return method

    def build_cli(self):
        self.maincli = SubcommandParser(self.name)
        for method in self.methods.values():
            subcmd = self.maincli.add_subcommand(
                method.name, description=method.description
            )
            subcmd.function = method.method
            for param in method.args:
                subcmd.add_argument(param.name, type=param.annotation)
            for param in method.kwargs.values():
                subcmd.add_argument(f"--{param.name}", type=param.annotation)


multiapi = MultiAPI("budgetm")


class BudgetManager:
    def __init__(self, money=1000):
        self.transactions = []
        self.money = money

    @multiapi.add(http_method="POST", help_group="basics")
    def outcom(self, cost: int, description: str = ""):
        """
        Add a new outcom to the current profil

        Args:
            cost(int): cost to add
            description(str): description of the transaction
        """
        self.transactions.append(-cost)
        self.money -= cost

    @multiapi.add
    def show(self):
        for t in self.transactions:
            print(t)

    @multiapi.add(http_method="POST", help_group="basics")
    def incom(self, cost: int, description: str = ""):
        """
        Add a new outcom to the current profil

        Args:
            cost(int): cost to add
            description(str): description of the transaction
        """
        self.transactions.append(cost)
        self.money += cost


# FIXME: how to add groups!?
# FIXME: how to chose which instance to use
# FIXME: how to add description of prog
def manual_build():
    budgetm_cmd = SubcommandParser("budgetm", description="TODO")
    outcom_cmd = budgetm_cmd.add_subcommand("outcom")
    outcom_cmd.add_argument("cost", type=int, description="Adding things")

    show_cmd = budgetm_cmd.add_subcommand("show")


if __name__ == "__main__":
    multiapi.build()
    multiapi.maincli.run()
