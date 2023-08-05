This solution could be no more than a 'collection of scripts.'
However, we prefer to try and maintain some design throughout the code base.

> Generally, in this document, design refers to 'software organization conventions'.

Specifically, we will discusses each of the following in some depth:

* [Design Objectives](#design-objectives)
* [General Conventions](#general-conventions)
* [CLI Tool Naming Convention](#cli-tool-naming-convention)
* [Module & Package Conventions](#module--package-conventions)
* [API Integration Conventions](#api-integrationwrapper-conventions)
* [TextFSM Conventions](#textfsm-conventions)
* [Argument Parsing](#argument-parsing)


# CLI Tool Naming Convention

CLI Tools use the following naming convention:

* `routeviews-` prefix
    * Automation tools that help with some automated workflow.
* `rvm-` prefix
    * Monitoring tools that give some info about our infrastructure.
    * **⚠ Important:** These tools MUST **not** make changes.
    * Ideally, all these tools support "--influxdb" option to produce InfluxDB Line Protocol. 
        > InfluxDB Line Protocol enables easy integration with our Telegraf/InfluxDB/Grafana monitoring solution!

# Argument Parsing

We use the [ConfigArgParse package](https://pypi.org/project/ConfigArgParse/) for processing command line arguments.

> **ℹ Tip:** 'Pipeline' solutions are great at handling Environment Variables.
> ConfigArgParse introduces the `env_var` option for any argument to auto  (e.g., Jenkins, GitHub Actions).



# TextFSM Conventions

We use [TextFSM](https://github.com/google/textfsm#textfsm) templates when we need to collect data from some CLI command's output.

> **ℹ Tip:** If there is any method for extracting structured data (ex. JSON, NetCONF, XML), **prefer structured data over using TextFSM**. 

> ℹ What is TextFSM?
> Best to provide the definition directly from [project page](https://github.com/google/textfsm):
>
> > Python module which implements a template based state machine for parsing semi-formatted text. 
> > Originally developed to allow programmatic access to information returned from the command line interface (CLI) of networking devices.

## Usage

We have wired up the `routeviews.parse.template_parse` function to use the "src/routeviews/templates/" folder.
Any template added to the "src/routeviews/templates/" folder can subsequently be invoked using `template_parse()`.

As an example, assume we've just added the template, "src/routeviews/templates/**bgp_neighbors**.tmpl".
This template can be run by calling `template_parse(..., 'bgp_neighbors')`

A full example (leveraging `routeviews.exec`) is provided below:

    import routeviews.exec
    import routeviews.parse

    console_output = routeviews.exec.run('sudo', 'vtysh', '-c', 'show bgp neighbors')

    parsed_output = routeviews.parse.template_parse(console_output, template='bgp_neighbors')


# General Conventions

Many conventions are generic, and can apply to *all* Python code.

## Modules as Singletons

The common 'singleton pattern' is trivial to implement in Python.
All we do is consider the module itself to be the 'singleton object.'

*Convention*: 

* use a single module (e.g. "my_singleton.py").
* define all 'methods' directly as module functions.
* define all 'properties' directly as module variables.
* retrieve the singleton object via "import my_singleton"

You may be asking, "is this really a proper Singleton?"
There are two important characteristics we care about Singleton objects, which this scheme fulfills:

* Only ONE of the Singleton object will ever exist.
    * ✅ Yes: thanks to Python's import logic, any subsequent imports of the 'my_singleton' module will ALWAYS return the same 'my_singleton object.'
* Can we retrieve the same Singleton object from anywhere?
    * ✅ Yes: *everything* is an object in Python.*

> *: Even an imported module is an object! 
> So, "import my_singleton" results in importing the one-and-only 'my_singleton object.'

## Provide Type Hints

Type hints make any object-oriented package or module much more 'discoverable' by its users.
So, try to provide type hints wherever possible!

### Reference a Type before it is defined

If some type hint is impossible due to circular dependencies, [that definition may be expressed as a string literal, to be resolved later ("forward references")](https://peps.python.org/pep-0484/#forward-references).

Without forward references, the following code does not work.

    class Tree:
        def __init__(self, left: Tree, right: Tree):
            self.left = left
            self.right = right
    
Using the string literal `'Tree'` (instead of `Tree`) results in a forward reference which will be resolved later.

    class Tree:
        def __init__(self, left: 'Tree', right: 'Tree'):
            self.left = left
            self.right = right

## Use Data Classes

> Data Classes Require Python >= 3.7

We love [Python Data Classes (PEP 557)](https://peps.python.org/pep-0557/).

What are Data Classes?
Conceptually, any class that will store data is a Data Class.
In Python, this is manifest as the `dataclasses` package.
This package provides the simple `dataclass` decorator/function, which will reduce a lot of 'boilerplate code' from your Data Class.

**Key Point**: The `dataclasses` module reduces a lot of 'boilerplate code.'

As an example, I consider the `__init__()` method to be boilerplate in general.
Using `dataclass` decorator, that method is auto-defined!

    from dataclasses import dataclass

    @dataclass
    class Foo:
        foo: str

With this super-readable 'Data Class' definition for `Foo`, we can instantiate Foo using key-value arguments.

    # We didn't have to write __init__(foo)..., but it works!
    Foo(foo='hello')

### Prefer Immutable Objects (`frozen=True`)

We prefer immutable dataclasses!

> ℹ Why prefer `frozen=True`? 
>
> 'Frozen objects' can be used in Python Sets and as Dictionary Keys!
> In addition, 'preferring immutable objects' often results in code that is *much* **easier to test!**

To make a dataclass immutable, use the dataclass decorator with the keyword argument: "`frozen=True`"

An example of an immutable Point data class.

    @dataclass(frozen=True)
    class Point:
        x: int
        y: int

    point = Point(1,2)
    point.x = 3  # Will raise an exception!

### *Warning: mutable default values*

When setting default values, mind that default values are not mutable!
Specifically, this can result in multiple class instances sharing the same copy of that default value!

Let's consider a specific example: if two instances of class `D` do not specify a value for `x` when creating a class instance will share the same copy of `x`.

    from dataclasses import dataclass
    @dataclass
    class D:
        x: list = []  # ❌ BAD, never do this!

To fix this, we can simply use the provided `field` function from the dataclasses module.
    
    from dataclasses import dataclass, field
    @dataclass
    class D:
        x: list = field(default_factory=list)

> See more in ["Mutable default values" in Python docs](https://docs.python.org/3/library/dataclasses.html#mutable-default-values)

# Module & Package Conventions

Overall, we use package and module names that follow PEP 8 and 'make sense.'
Given that, these are some of the patterns that have emerged in this code base.

* `routeviews.scripts` package holds CLI tools.
* `routeviews.templates` package holds template resources.

## Defining `__all__`

We maintain `__all__` in our packages' `__init__.py` to help simplify the 'public API' of the package.
This concept is well discussed in the following quote, from [a stack overflow answer](https://stackoverflow.com/a/35710527):

> *What does `__all__` do?*
>
> It declares the semantically "public" names from a module. 
> If there is a name in __all__, users are expected to use it, and they can have the expectation that it will not change.


# API Integration/Wrapper Conventions

We integrate with many external platforms and services via API.
Keeping these integrations organized is useful.

We use the following conventions to manage our API integrations, each discussed further below:

* One package per API integration
* Manage `__all__`
* `dataclasses` sub-package

## One Package per Integration

Recall one of our high level design goals is 'package cohesion.'
For API Integrations, we consider primary dimension of cohesion for these to be, "what product's API am I integrating?"

*Convention*:

* Develop ONE single package for each external application that we integrate with.

> This convention is intuitive and aligns with [many platform/services](https://github.com/realpython/list-of-python-api-wrappers).

## Repository, Client, and Unit of Work

TODO

| Layer | Abstractness  | Title         | Description | 
|-------|---------------|---------------|-------------|
| 3     | More          | Unit of Work  | Plan some work to be done. |
| 2     | Some          | Repository    | Work with well-typed 'Domain Data Classes'. |
| 1     | None          | Client        | Work directly with bytes and return primitive dictionaries. |

These are software layers, which implies dependencies between layers.

Specifically: 

* Repository: depends on Client.
* Unit of Work: depends on Repository (and transitively depends on the Client as well). 


## Domain Data Classes

In general, every different platform that we integrate will have its own *types* of data.
To make working with these different data joyful, we define a *domain Data Class* per data type.

> Relevant Design goal: "* Type hints for everything."

### `dataclasses` package

We use the name "dataclasses" for the package that contains [Python dataclasses](https://docs.python.org/3/library/dataclasses.html).
Further, all dataclasses are then exposed in the API package.

*Convention*:

* "dataclasses" package contains all dataclasses.
* One dataclass per module/file.

## Maintain `__all__`

We have already discussed the convention that [we 'Define `__all__`' for packages](#defining-all).

*Convention*:

* Expose all dataclasses 

Specifically, for API wrappers, we want to ensure the following:

- [ ] All dataclasses are available via `routeviews.<API>.<dataclass_name>`
- [ ] Repository & Client classes are available via `routeviews.<API>.<repository_classname>`


# Design Objectives

We have the following objectives in our design.

> These are roughly order-ranked: the top of the list is highest priority.

* Type hints for everything.
* Packages, Modules, and Classes are cohesive*.
* Packages, Modules, and Classes are loosely coupled**.

*: TODO Discuss 'cohesion.'
**: TODO Discuss 'loosely coupled.'

