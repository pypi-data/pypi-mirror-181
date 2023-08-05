import argparse
import inspect
import sys
import typing
import warnings

import argcomplete
import coloring

"""
Group structure:
    name(str)
    title(str)
    description(str)
    commands(dict)
        description(str)
"""


class SubcommandParser:
    def __init__(
        self,
        prog=None,
        *,
        parent=None,
        parser=None,
        autocomplete: bool = None,
        # Help
        colors=None,
        prolog=None,
        description=None,
        epilog=None,
    ):
        """

        Args:
            prog: name of the program
            parent: parent parser
            parser: argparse.ArgParser to use
            description: description of the program
            autocomplete: E,able autocomplete
            colors:

        Advantages over argparse:
            - use add_subcommand instead of using add_parsers then add_subparser
            - run command that will run directly the program
            - better help with groups/colors
            - ease of use autocomplete
        """

        if prog is None:
            prog = sys.argv[0]

        if colors is None:
            colors = False

        if autocomplete is None:
            autocomplete = False

        self.parent = parent
        self.name = prog or sys.argv[0]
        self.subcommands = {}
        self.function = None
        self._argparse_subparsers = None

        # Help
        self.colors = colors
        self.groups = {}
        self.add_group("_ungrouped", title="Other commands")
        self.description = description
        self.prolog = prolog
        self.epilog = epilog
        self.hide = False
        self.autocomplete = autocomplete
        self._group_namespace = (
            set()
        )  # track groupnamespace for subcommands and help_subcommands

        if self.parent is None:
            self.fullname = self.name
        else:
            self.fullname = f"{self.parent.fullname}.{self.name}"

        if parser is None:
            parser = argparse.ArgumentParser(
                prog=prog, description=description, epilog=epilog
            )

        self._argparse_parser = parser
        self._subcommand_depth = 1

        self._print_help = self._argparse_parser.print_help

    def add_argument(self, *args, **kwargs):
        self._argparse_parser.add_argument(*args, **kwargs)

    def add_group(self, name, *, title: str = None, description: str = None):
        if name in self.groups:
            raise KeyError(f"Group {name} already exists")

        if title is None:
            title = name

        if description is None:
            description = ""

        self.groups[name] = {"title": title, "description": description, "commands": {}}

    def add_subcommand(self, command_name, description=None, group=None, hide=False):
        if command_name in self.subcommands:
            raise KeyError(f"command {command_name!r} already exists")

        # TODO: check that help_command is not existing in the same grp
        #  refactor this! we should check all namespace not only the one for grp
        # TODO: test me
        if group and hide:
            raise ValueError(f"Canno't have both group and hide is True")
        if not hide:
            if command_name in self._group_namespace:
                raise KeyError(
                    f"command {command_name!r} already exists as help_subcommand"
                )

            if group is None:
                group = "_ungrouped"

            self.groups[group]["commands"][command_name] = {"description": description}
            self._group_namespace.add(command_name)

        if self._argparse_subparsers is None:
            self._argparse_subparsers = self._argparse_parser.add_subparsers(
                dest=self._get_subcommand_dest_name()
            )

        subcommand_parser = self._argparse_subparsers.add_parser(command_name)

        subcommand_command = SubcommandParser(
            command_name,
            parser=subcommand_parser,
            parent=self,
            description=description,
        )
        subcommand_command._subcommand_depth += self._subcommand_depth
        subcommand_command.hide = hide
        self.subcommands[command_name] = subcommand_command
        return subcommand_command

    def add_help_subcommand(self, command_name, description=None, group=None):
        """Only add this command in the help

        Explanation:
            this could be usefull if you have a lot of commands that are hidden
            and you want to add one help description to group all these commands
        """
        if group is None:
            group = "_ungrouped"

        if command_name in self.subcommands:
            raise KeyError(f"command {command_name!r} already exists")

        if command_name in self._group_namespace:
            raise KeyError(
                f"command {command_name!r} already exists in help_subcommands"
            )

        self.groups[group]["commands"][command_name] = {"description": description}
        self._group_namespace.add(command_name)

    def __getitem__(self, item: str):
        return self.subcommands[item]

    def __str__(self):
        return f"SubcommandParser(<{self.fullname}>)"

    def __repr__(self):
        return self.__str__()

    def print_help(self):
        self._init_help()
        self._print_help()

    def _get_subcommand_dest_name(self, depth: int = None):
        if depth is None:
            depth = self._subcommand_depth
        if depth == 1:
            return "subcommand"
        else:
            return f"subcommand_{depth}"

    def _get_subcommand_name(self, parsed_args, depth: int = None):
        argparse_cmd_name = self._get_subcommand_dest_name(depth)
        return getattr(parsed_args, argparse_cmd_name)

    def parse_args(self, args=None, namespace=None):
        self.check_errors()
        self._init_help()

        if self.autocomplete:
            argcomplete.autocomplete(self._argparse_parser)

        return self._argparse_parser.parse_args(args, namespace=namespace)

    def run(self, args=None):
        """Run the main program"""

        # Parse arguments
        parsed_args = self.parse_args(args)
        # TODO: hook main: self._run_main(parsed_args)  # hook to _run_main

        # Check if there is any subcommand
        if not self.subcommands:
            self.print_help()
            sys.exit(1)

        # get called subcommand
        depth = 1
        subcommand = self
        while True:
            try:

                cmd_name = self._get_subcommand_name(parsed_args, depth=depth)

                if cmd_name is None:
                    self.print_help()
                    sys.exit(1)
                subcommand = subcommand[cmd_name]
                depth += 1
            except AttributeError:
                break

        # If function is None, automatically it (doesn't have subparsers
        #  because we already checked errors on parse_args
        if subcommand.function is None:
            self.print_help()
            sys.exit(0)

        subcommand.function(parsed_args)

    def _init_help(self):
        """If groups exist change the current help"""
        """
        - prolog
        - usage
        - prog description
        - list subcommands
        - epilog
        """
        SPACES = "    "
        LINE_SEP = "\n\n"

        # FIXME: test/me
        # Handle groups
        # =============
        # Groups are already handled in add_subcommand
        if len(self.groups) == 1:
            # If len groups == 1, title = "Commands" else title = "Other commands"
            self.groups["_ungrouped"]["title"] = "Commands"

        # make ungrouped in last position
        _ungrouped = self.groups.pop("_ungrouped")
        self.groups["_ungrouped"] = _ungrouped
        # get the longest command name for pretty print with tabulations
        # flatten all commands names in self.groups()
        commands_names = [
            cmd for group in self.groups.values() for cmd in group["commands"]
        ]

        if len(commands_names):
            max_command_length = len(max(commands_names, key=len))
        else:
            max_command_length = 0

        # header prog name and description
        prog = self.name
        help = ""

        # add prolog
        if self.prolog:
            help += self.prolog + LINE_SEP

        # add usage
        help += f"Usage: {prog} [-h] <subcommand>{LINE_SEP}"

        # add description
        if self.description:
            help += f"{self.description}{LINE_SEP}"

        for group_name, group in self.groups.items():
            if not group["commands"]:
                continue
            group_title = group["title"] + ":"
            if self.colors:
                group_title = coloring.colorize(group_title, c="slate_blue3", s="b")

            group_description = group.get("description", "")

            help += group_title
            if group_description:
                help += " " + group_description
            help += LINE_SEP
            for cmd_name, command_info in group["commands"].items():
                description_command = command_info.get("description", "") or ""
                cmd_txt = cmd_name.ljust(max_command_length)
                if self.colors:
                    cmd_txt = coloring.colorize(cmd_txt, c="medium_purple")
                help += f"{SPACES}{cmd_txt}{SPACES}{description_command}\n"
            help += "\n"

        help += self.epilog or ""
        # change the help function
        self._argparse_parser.print_help = lambda file=None: print(help, file=file)
        # self.main_parser.print_usage = self.main_parser.print_help
        # print(help)
        self._print_help = self._argparse_parser.print_help

    def _print_and_exist(self, msg, status=1):
        print(msg)
        sys.exit(status)

    def iter_allcommands(self):
        """Iter all commands, self included"""
        yield self
        for parser in self.subcommands.values():
            yield from parser.iter_allcommands()

    def check_errors(self):
        """Check if subcommands are correctly built
        This method is called before parse_args/run
        """
        for command in self.iter_allcommands():
            # If function exists it must be callable
            if command.function is not None and not callable(command.function):
                raise TypeError(f"{command.fullname}.function must be callable")

            # Todo: check that function has only one argument

            # If the command don't have any subcommand, it must have a function
            if not command.subcommands and command.function is None:
                raise ValueError(
                    f"Subcommand {command} don't have linked function or should have subpcommands"
                )


class ArgparseSubcmdHelper:
    """argparse class Helper for making subcommands easily
    To add a subcommand x implement the following methods/attributes
        def parser_x(self, parser): add arguments to the subcommand parser
        def run_x(self, args):  run the subcommand
        description_x: description of the subcommand


    cls attributes
        prog:
        _parser_main: add to the main parser
        _run_main(self, args): hook after parsing args, handling main variable before dispatch to subcmd

    Custom help
        groups

    Nested subcommand
        command_x: of Type[ArgparseSubcmdHelper]


    """

    prog = None
    description = None
    groups = None  # FIXME: not yet correctly implemented/tested
    autocomplete = False

    # TODO: add a way to have an optional subcm (dont thtrow and error when called withotu subcmd)
    # TODO: improve the custom help! and test it
    def _parser_main(self, parser):
        """Hook to add arguments to the main parser (general arguments)"""
        pass

    def _run_main(self, args):
        """Hook to execute code before executing the subcommand"""
        pass

    def _init_help(self):
        """If groups exist change the current help"""
        # FIXME: imlement/test me
        if not self.groups:
            return
        SPACES = "    "
        color_help = getattr(self, "color_help", False)
        # header prog name and description
        prog = self.prog or sys.argv[0]
        help = getattr(self, "prolog", "")
        help += f"usage: {prog} [-h] <subcommand>\n\n"

        if self.description:
            help += f"{self.description}\n\n"

        # get the longest command name for pretty print with tabulations
        # flatten all commands names in self.groups()
        grouped_commands_name = [
            cmd for e in self.groups.values() for cmd in e.get("commands", [])
        ]
        all_commands_name = [e[4:] for e in dir(self) if e.startswith("run_")]
        # TODO: add nested commands
        ungrouped_printed_commands = [
            e for e in all_commands_name if e not in grouped_commands_name
        ]
        # max command length for pretty print (aligned)
        max_command_length = len(max(grouped_commands_name, key=len))
        # FIXME: check that ungrouped do not exist
        # add ungrouped commands
        if ungrouped_printed_commands:
            self.groups["ungrouped"] = {
                "commands": ungrouped_printed_commands,
                "title": "Other commands",
                # "description": "commands that do not belong to any group",
            }

        for group_name, group in self.groups.items():
            group_title = group.get("title", group_name) + ":"
            if color_help:
                group_title = coloring.colorize(group_title, c="slate_blue3", s="b")
            commands = group["commands"]
            group_description = group.get("description", "")

            help += group_title
            if group_description:
                help += " " + group_description
            help += "\n\n"
            for cmd in commands:
                # check if the command exist!
                if not hasattr(self, f"run_{cmd}"):
                    raise TypeError(
                        f"Command {cmd!r} can't be in a group because it don't exist (consider implementing 'run_{cmd}')"
                    )
                description_command = getattr(self, f"description_{cmd}", "")
                cmd_txt = cmd.ljust(max_command_length)
                if color_help:
                    cmd_txt = coloring.colorize(cmd_txt, c="medium_purple")
                help += f"{SPACES}{cmd_txt}{SPACES}{description_command}\n"
            help += "\n"

        # change the help function
        self.parser.print_help = lambda file=None: print(help, file=file)
        # self.main_parser.print_usage = self.main_parser.print_help

    def __init__(self, parser=None, subcommand_depth=1):
        # subcommand_depth to allow different level of subcommands and have
        #   the correct dest for subcommands "subcommand" "subcommand_2" "subcommand_3" ...
        self.subcommand_depth = subcommand_depth

        # create main parser
        if parser is None:
            parser = argparse.ArgumentParser(
                prog=self.prog, description=self.description
            )
        self.parser = parser

        # hook to add arguments for the main program
        self._parser_main(self.parser)
        self._build_command()

    def _build_command(self):
        # init the subcommande
        if self.subcommand_depth == 1:
            dest = "subcommand"
        else:
            dest = f"subcommand_{self.subcommand_depth}"

        self.subparsers = self.parser.add_subparsers(dest=dest)
        # Handle all the run_<x> commands
        for subcommand_name in [
            e[len("run_") :] for e in dir(self) if e.startswith("run_")
        ]:
            # Check that the subcommand is callable
            if not callable(getattr(self, "run_" + subcommand_name)):
                raise TypeError(f"Attrbute {'run_'+subcommand_name} must be callable")

            # check that command_<x> and run_<x> dont exist
            if hasattr(self, f"command_{subcommand_name}"):
                raise RuntimeError(
                    f"Both command_{subcommand_name} and run_{subcommand_name} are present"
                )

            # get help if exist
            description = getattr(self, "description_" + subcommand_name, None)
            subparser = self.subparsers.add_parser(
                subcommand_name, help=description, description=description
            )
            parser_name = f"parser_{subcommand_name}"

            # add parser_<cmd> if exist (the parser_<cmd> is not required only run_<cmd> is)
            if hasattr(self, parser_name):
                parser_func = getattr(self, parser_name)
                parser_func(subparser)

        # If parser_x exist but run_x don't raise an exception
        for parser_name in [
            e[len("parser_") :] for e in dir(self) if e.startswith("parser_")
        ]:
            if not hasattr(self, "run_" + parser_name):
                raise RuntimeError(
                    f"parser_{parser_name} method present but run_{parser_name} missing"
                )

        # change help if groups attribute is present
        self._init_help()

        # handle all the command_<x> subcommands
        for subcommand_name in [
            e[len("command_") :] for e in dir(self) if e.startswith("command_")
        ]:
            subcommand_cls: typing.Type[ArgparseSubcmdHelper] = getattr(
                self, "command_" + subcommand_name
            )
            if (not inspect.isclass(subcommand_cls)) or not (
                issubclass(subcommand_cls, ArgparseSubcmdHelper)
            ):
                raise TypeError(
                    f"command_{subcommand_name} attribute must be a class that inherit from {ArgparseSubcmdHelper.__name__!r} not '{type(subcommand_name).__name__}'"
                )

            subcmd_description = getattr(self, f"description_{subcommand_name}", None)
            # TODO: add help_ and description_
            subcmd_parser = self.subparsers.add_parser(
                subcommand_name, description=subcmd_description, help=subcmd_description
            )
            subcommand = subcommand_cls(
                parser=subcmd_parser, subcommand_depth=self.subcommand_depth + 1
            )
            setattr(self, f"_instance_command_{subcommand_name}", subcommand)

    def parse_args(self, args=None):
        if self.autocomplete:
            argcomplete.autocomplete(self.parser)

        return self.parser.parse_args(args)

    def run(self, args=None):
        """Run the main program"""
        if self.autocomplete:
            argcomplete.autocomplete(self.parser)
        parsed_args = self.parser.parse_args(args)
        self._run_main(parsed_args)  # hook to _run_main
        self._run(self, parsed_args)

    def _run(self, command, parsed_args, depth=1):
        """Search the subfunction to run recursivly"""
        if depth == 1:
            subcommand_name_attribute = "subcommand"
        else:
            subcommand_name_attribute = f"subcommand_{depth}"

        subcommand_name = getattr(parsed_args, subcommand_name_attribute)
        if subcommand_name is None:
            command.parser.print_help()
            sys.exit(1)

        if hasattr(command, f"run_{subcommand_name}"):
            subcommand = getattr(command, f"run_{subcommand_name}")
            subcommand(parsed_args)
        elif hasattr(command, f"command_{subcommand_name}"):
            subcommand_instance = getattr(
                command, f"_instance_command_{subcommand_name}"
            )
            self._run(subcommand_instance, parsed_args, depth + 1)

    def main(self, *args, **kwargs):
        """Deprecated run method"""
        warnings.warn(
            "main will be deprecated in future version, use run instead",
            PendingDeprecationWarning,
        )
        self.run(*args, **kwargs)


# TODO: deprecate old argparse
# TODO: add help feature
# TODO: groups with help
