import argparse

import koalak

# Creating framework and pluginmanager
wordlistools = koalak.mkframework("wordlistools")
tools = wordlistools.mkpluginmanager("tools")


# Creating ou BasePlugin with constraints on the attribute
@tools.mkbaseplugin
class BaseTool:
    type = tools.attr(type=str, choices=["filters", "modifiers"])
    func = tools.attr()


# Adding Modifiers Plugin tools
class LowerTool(BaseTool):
    type = "modifiers"
    name = "lower"

    def func(self, string):
        return string.lower()


class UpperTool(BaseTool):
    type = "modifiers"
    name = "upper"

    def func(self, string):
        return string.upper()


class InvertTool(BaseTool):
    type = "modifiers"
    name = "invert"

    def func(self, string):
        return string[::-1]


# Adding Filters Plugin tools
class IsdigitTool(BaseTool):
    type = "filters"
    name = "isdigit"

    def func(self, string):
        return string.isdigit()


class IsupperTool(BaseTool):
    type = "filters"
    name = "isupper"

    def func(self, string):
        return string.isupper()


# Main program logic
def run_wordlistools(function_name, filepath):
    # Get the plugin class with its name
    Tool = tools[function_name]
    tool = Tool()

    if tool.type == "filters":
        with open(filepath) as f:
            for line in f:
                line = line[:-1]
                if tool.func(line):
                    print(line)
    elif tool.type == "modifiers":
        with open(filepath) as f:
            for line in f:
                line = line[:-1]
                print(tool.func(line))


if __name__ == "__main__":
    # Get the name of all our tools by iterating the PluginManager
    tool_names = [tool.tool_name for tool in tools]

    parser = argparse.ArgumentParser()
    parser.add_argument("tool", help="Tool to use", choices=tool_names)
    parser.add_argument("filepath", help="Wordlist path")
    args = parser.parse_args()

    run_wordlistools(args.tool_name, args.filepath)
