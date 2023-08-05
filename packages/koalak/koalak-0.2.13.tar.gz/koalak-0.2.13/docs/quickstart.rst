Quickstart
==========

Koalak is mainly built to help you create libraries with plugins architecture.


Wordlistools example
--------------------

Let's say you want to develop an extensible program that will allow you
to perform operations on wordlists (files with one word per line).
The program will have the following features:


- The name of our tool will be "wordlistools"
- The program will have many modifier tools that will modify each line in the file
- The program will have many filter tools that will filter lines following a criteria
- Program easily extensible: users of your library can easily add their own tools


Expected result
---------------

Before starting to develop "wordlistools", we have to know how the final program will be.
Let's take the following wordlist "passwords.txt" which contains 5 potential passwords as example:

::

    Azerty
    TEST
    Test123
    123456789
    something


With our final program we can modify each line in upper case

::

    > ./wordlistools.py upper passwords.txt
    AZERTY
    TEST
    TEST1123
    123456789
    SOMETHING

It will be possible to keep digits only

::

    > ./wordlistools.py isdigit passwords.txt
    123456789

It will be possible to keep only uppercase words

::

    > ./wordlistools.py isupper passwords.txt
    TEST



Basic Koalak Architecture
-------------------------
In order to create a program with Koalak, we have to understand how the basic architecture works:


- Each program can be represented by the object ``framework``

    - A framework must have a unique name over the python projects (preferably the name reserved on Pypi)
    - Framework are created with the function ``koalak.mkframework(framework_name: str)`` (mkframework => make framework)
    - A framework can have zero to many PluginsManager

- PluginsManager are the container object that will have all your plugins

    - A PluginManager must have a unique name inside the Framework
    - PluginManagers are created with the method ``framework.mkpluginmanager(pluginmanager_name: str)``
    - Each PluginManager have one (and only one) base plugin that will be the base class for all plugins.
    - To define the base plugin, use the decorator ``pluginmanager.register(base_class)``


- Plugin
    - To add new plugins, you have to inherit from the BasePlugin class
    - All plugins must have a unique 'name' as a class attribute





Start developing
----------------

For wordlistools we will have only one PluginManager which will represent
all our tools. Each tool will have a type ("modifier" or "filter") and the function
to be executed.

Let's start with the basics, creating our framework and our plugin manager.

::


    import koalak

    wordlistools = koalak.mkframework("wordlistools")
    tools = wordlistools.mkpluginmanager("tools")


Now we can create and register our BasePlugin. We have two constraints that all
plugins must respect. All of our plugins must have the attribute "type" and "func".
It is possible to add constraint on the "type" attribute, it must be a string and
one of the two possibilities "modifiers" or "filters":


::

    @tools.mkbaseplugin
    class BaseTool:
        type = tools.attr(type=str, choices=["modifiers", "filters"])
        func = tools.attr()

We can start develop our first tool, which will modify each word in the
wordlist by making it uppercase.


::

    class UpperTool(BaseTool):
        name = "upper"
        type = "modifiers"
        def func(self, string):
            return string.upper()

Now, we can develop a second tool that will filter digits words only:

::

    class IsdigitTool(BaseTool):
        name = "isdigit"
        type = "filters"
        def func(self, string):
            return string.isdigit()


Now that we have our plugins we can start the core logic of our program.
We will have the main function that will take a filepath (the wordlist) and
a plugin name. We can get the plugin by its name through the brackets syntax
``pluginmanager[<tool_name>]``, then we check the type of the tool.

If the tool is a 'modifier', we will change the content of the word. Otherwise,
if the tool is a 'filter', we will check if the word match the criteria to print
the line or not.

::

    def run_wordlistools(function_name, filepath):
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


Now that our tool is working, we can wrap it in a CLI interface using argparse.
In order to limit the choices of the argument 'tool_name', we can use the
names of all available tools. In order to iterate over plugins, we can
use the ``PluginManager.iter()`` inside a loop or a list comprehension:


::

    if __name__ == "__main__":
        # Get the name of all our tools by iterating the PluginManager
        tool_names = [tool.tool_name for tool in tools]

        parser = argparse.ArgumentParser()
        parser.add_argument("tool", help="Tool to use", choices=tool_names)
        parser.add_argument("filepath", help="Wordlist path")
        args = parser.parse_args()

        run_wordlistools(args.tool_name, args.filepath)


Final code
----------

.. literalinclude:: wordlistools_example.py

Summary
-------
In summary Koalak helps in the writing of plugins architecture programs, Koalak will
do for you:

- Adding constraints to your plugins easily
- Query your plugins (list of plugins, get plugin by name, ...)
- The possibility to extend your program easily (inherit the base class)
- Possibility to add plugins by writing python file on your home path "~/.koalak/<framework>/plugins/myplugins.py"
