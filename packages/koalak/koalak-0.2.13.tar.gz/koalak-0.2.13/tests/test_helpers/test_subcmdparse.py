import pytest
from koalak import SubcommandParser


def test_run_cmd(capsys):
    main_command = SubcommandParser()

    def run_mycmd(args):
        print(1)

    mycmd_command = main_command.add_subcommand("mycmd")
    mycmd_command.function = run_mycmd

    # assert that "mycmd" parse
    main_command.parse_args(["mycmd"])

    capsys.readouterr()  # ignore the first prints
    main_command.run(["mycmd"])
    captured = capsys.readouterr()
    assert captured.out == "1\n"


def test_run_with_args(capsys):
    main_command = SubcommandParser()

    def run_mycmd(args):
        print(args.printme)

    mycmd_command = main_command.add_subcommand("mycmd")
    mycmd_command.add_argument("printme")
    mycmd_command.function = run_mycmd

    # assert that "mycmd" parse
    main_command.parse_args(["mycmd", "1"])

    with pytest.raises(SystemExit):
        main_command.parse_args(["mycmd"])

    capsys.readouterr()  # ignore the first prints

    main_command.run(["mycmd", "test"])
    captured = capsys.readouterr()
    assert captured.out == "test\n"

    main_command.run(["mycmd", "22"])
    captured = capsys.readouterr()
    assert captured.out == "22\n"


def test_run_with_many_args(capsys):
    main_command = SubcommandParser()

    def run_mycmd(args):
        print(args.printme * args.n)

    mycmd_command = main_command.add_subcommand("mycmd")
    mycmd_command.add_argument("printme")
    mycmd_command.add_argument("-n", type=int, default=1)
    mycmd_command.function = run_mycmd

    # assert that "mycmd" parse
    main_command.parse_args(["mycmd", "1"])

    # assert that "mycmd" parse
    main_command.parse_args(["mycmd", "1", "-n", "2"])

    with pytest.raises(SystemExit):
        main_command.parse_args(["mycmd"])

    capsys.readouterr()  # ignore the first prints

    main_command.run(["mycmd", "test"])
    captured = capsys.readouterr()
    assert captured.out == "test\n"

    main_command.run(["mycmd", "hey", "-n", "3"])
    captured = capsys.readouterr()
    assert captured.out == "heyheyhey\n"


def test_nested_commands(capsys):
    main_command = SubcommandParser()

    """
    main
        - version
        - var
            - ls
            - add
    """
    version_command = main_command.add_subcommand("version")
    version_command.function = lambda args: print("version")

    var_command = main_command.add_subcommand("var")

    ls_command = var_command.add_subcommand("ls")
    ls_command.function = lambda args: print("ls")

    add_command = var_command.add_subcommand("add")
    add_command.function = lambda args: print("add")

    capsys.readouterr()  # ignore the first prints
    main_command.run(["version"])
    captured = capsys.readouterr()
    assert captured.out == "version\n"

    main_command.run(["var", "ls"])
    captured = capsys.readouterr()
    assert captured.out == "ls\n"

    main_command.run(["var", "add"])
    captured = capsys.readouterr()
    assert captured.out == "add\n"


def test_nested_commands_depth_2(capsys):
    main_command = SubcommandParser("main")

    main_command.add_subcommand("a").function = lambda args: print("d1.a")
    main_command.add_subcommand("b").function = lambda args: print("d1.b")

    depth_command = main_command.add_subcommand("depth")
    depth_command.add_subcommand("a").function = lambda args: print("d2.a")
    depth_command.add_subcommand("b").function = lambda args: print("d2.b")

    depth3_command = depth_command.add_subcommand("depth")
    depth3_command.add_subcommand("a").function = lambda args: print("d3.a")
    depth3_command.add_subcommand("b").function = lambda args: print("d3.b")

    capsys.readouterr()  # ignore the first prints
    main_command.run(["a"])
    captured = capsys.readouterr()
    assert captured.out == "d1.a\n"

    capsys.readouterr()  # ignore the first prints
    main_command.run(["b"])
    captured = capsys.readouterr()
    assert captured.out == "d1.b\n"

    with pytest.raises(SystemExit):
        main_command.run([])

    # depth2
    capsys.readouterr()  # ignore the first prints
    main_command.run(["depth", "a"])
    captured = capsys.readouterr()
    assert captured.out == "d2.a\n"

    capsys.readouterr()  # ignore the first prints
    main_command.run(["depth", "b"])
    captured = capsys.readouterr()
    assert captured.out == "d2.b\n"

    with pytest.raises(SystemExit):
        main_command.run(["depth"])

    # depth3
    capsys.readouterr()  # ignore the first prints
    main_command.run(["depth", "depth", "a"])
    captured = capsys.readouterr()
    assert captured.out == "d3.a\n"

    capsys.readouterr()  # ignore the first prints
    main_command.run(["depth", "depth", "b"])
    captured = capsys.readouterr()
    assert captured.out == "d3.b\n"

    with pytest.raises(SystemExit):
        main_command.run(["depth", "depth"])

    # None existing commands/args
    with pytest.raises(SystemExit):
        main_command.run(["a", "dontexist"])

    with pytest.raises(SystemExit):
        main_command.run(["depth", "dontexist"])

    with pytest.raises(SystemExit):
        main_command.run(["depth", "depth", "dontexist"])

    with pytest.raises(SystemExit):
        main_command.run(["a", "-x"])


def test_nested_commands_fullname(capsys):
    main_command = SubcommandParser("main")
    assert main_command.name == "main"
    assert main_command.fullname == "main"

    a_main_command = main_command.add_subcommand("a")
    assert a_main_command.name == "a"
    assert a_main_command.fullname == "main.a"

    b_main_command = main_command.add_subcommand("b")
    assert b_main_command.name == "b"
    assert b_main_command.fullname == "main.b"

    # check that main name didn't change
    assert main_command.name == "main"
    assert main_command.fullname == "main"

    depth_command = main_command.add_subcommand("depth")
    assert depth_command.name == "depth"
    assert depth_command.fullname == "main.depth"

    main_depth_a_cmd = depth_command.add_subcommand("a")
    assert main_depth_a_cmd.name == "a"
    assert main_depth_a_cmd.fullname == "main.depth.a"

    main_depth_b_cmd = depth_command.add_subcommand("b")
    assert main_depth_b_cmd.name == "b"
    assert main_depth_b_cmd.fullname == "main.depth.b"

    main_depth_depth_cmd = depth_command.add_subcommand("depth")
    assert main_depth_depth_cmd.name == "depth"
    assert main_depth_depth_cmd.fullname == "main.depth.depth"

    main_depth_depth_a_cmd = main_depth_depth_cmd.add_subcommand("a")
    assert main_depth_depth_a_cmd.name == "a"
    assert main_depth_depth_a_cmd.fullname == "main.depth.depth.a"

    main_depth_depth_b_cmd = main_depth_depth_cmd.add_subcommand("b")
    assert main_depth_depth_b_cmd.name == "b"
    assert main_depth_depth_b_cmd.fullname == "main.depth.depth.b"


# TODO: test without function linked

# Test errors
def test_subcmdparser_without_subcommands(capsys):
    # Without subcommands should have a function or error
    main_command = SubcommandParser(description="catchme")

    with pytest.raises(ValueError):
        main_command.parse_args([])

    # if main_command have function no error is raised
    main_command.function = lambda args: print("hello")
    main_command.parse_args([])


def test_subcmdparser_subcmd_without_function():
    main_command = SubcommandParser()
    subcmd_command = main_command.add_subcommand("subcmd")

    with pytest.raises(ValueError):
        main_command.run([])


def test_run_non_existing_cmd(capsys):
    # run non-existing command print help and exit
    main_command = SubcommandParser()
    main_command.add_subcommand("mycmd").function = lambda args: print("hello")

    with pytest.raises(SystemExit):
        capsys.readouterr()  # ignore last entries
        main_command.run(["dontexist"])

    # help was printed
    assert "invalid choice" in capsys.readouterr().err.lower()


def test_run_attribute_not_callable():
    main_command = SubcommandParser()

    main_command.add_subcommand("x").function = "String and not callable"

    with pytest.raises(TypeError):
        main_command.parse_args([])


def test_subcmd_already_exists():
    main_command = SubcommandParser()

    main_command.add_subcommand("x")

    with pytest.raises(KeyError):
        main_command.add_subcommand("x")


def test_help_basic(capsys):
    main_command = SubcommandParser("main")
    a_cmd = main_command.add_subcommand("a", description="do nothing")
    capsys.readouterr()

    main_command.print_help()
    expected_help = """Usage: main [-h] <subcommand>

Commands:

    a    do nothing"""
    # print()
    # print(expected_help)
    assert capsys.readouterr().out.strip() == expected_help


def test_help_3_subcmd(capsys):
    main_command = SubcommandParser("main")
    a_cmd = main_command.add_subcommand("a", description="do nothing")
    a_cmd = main_command.add_subcommand("b", description="yes")
    a_cmd = main_command.add_subcommand("cc", description="no")
    capsys.readouterr()

    main_command.print_help()
    # add more spaces because cc have length of 2
    expected_help = """Usage: main [-h] <subcommand>

Commands:

    a     do nothing
    b     yes
    cc    no"""
    # print()
    # print(expected_help)
    assert capsys.readouterr().out.strip() == expected_help


def test_help_hide(capsys):
    main_command = SubcommandParser("main")
    a_cmd = main_command.add_subcommand("a", description="do nothing")
    a_cmd = main_command.add_subcommand("b", description="yes", hide=True)
    a_cmd = main_command.add_subcommand("cc", description="no")
    capsys.readouterr()

    main_command.print_help()
    # add more spaces because cc have length of 2
    expected_help = """Usage: main [-h] <subcommand>

Commands:

    a     do nothing
    cc    no"""
    # print()
    # print(expected_help)
    assert capsys.readouterr().out.strip() == expected_help


def test_help_adding_groups(capsys):
    main_command = SubcommandParser("main")

    main_command.add_group(
        "first", title="First commands", description="important commands"
    )
    main_command.add_group(
        "second", title="Second commands", description="useless commands"
    )

    main_command.add_subcommand("a", description="do nothing", group="first")
    main_command.add_subcommand("bbb", description="yes", hide=True)
    main_command.add_subcommand("cc", description="no", group="second")
    main_command.add_subcommand("d", description="yesno", group="first")

    capsys.readouterr()

    main_command.print_help()
    # add more spaces because cc have length of 2
    expected_help = """Usage: main [-h] <subcommand>

First commands: important commands

    a     do nothing
    d     yesno

Second commands: useless commands

    cc    no
"""
    # print()
    # print(expected_help)
    assert capsys.readouterr().out.strip() == expected_help.strip()
