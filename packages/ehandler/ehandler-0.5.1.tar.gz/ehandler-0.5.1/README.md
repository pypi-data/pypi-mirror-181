<img src="./assets/images/logo.png" alt="Trii Logo" title="Trii" align="right" height="32">

# Exception Handler [ FastAPI Utility ]

This project works together with FastAPI and allows you to create error handlers
in a very simple and standard way. Basically it allows you to add (or use the default
a function that will be executed when an exception occurs on the server.

This is possible using the FastAPI Exception Handler (actually Starlette) and
using a function as a template that receives data such as the request object
that was invoked on the route, the exception, the status code that handles that
exception, and some _'static'_ arguments.

## Table of Contents

- [How to use it](#how-to-use-it)
  - [Basic](#basic)
  - [Explanation](#explanation)
- [Examples](#examples)
  - [Content callback](#content-callback)
  - [Add additional data](#add-additional-data)
  - [Change default status code](#change-default-statuscode)
- [Contribute](#how-to-contribute)
  - [Prerequisites](#prerequisites)
  - [Install Poetry](#install-poetry)
  - [Install Pre-Commit](#install-pre-commit)
    - [Install hooks](#install-hooks)
  - [Install dependencies](#install-dependencies)
  - [Add dependencies](#add-dependency)
  - [Add dev dependencies](#add-dev-dependency)
  - [Run test](#run-test)
    - [Static test](#static-test)
      - [Single test](#single-test)
      - [All test](#all-test)
      - [All files](#all-files)
    - [Static test](#unittest)

## How to use it

### Basic

There are several ways to use it, the simplest is to use it with the templates
(Callbacks) that come by default. And simply create a list with the pairs of
exceptions and status codes.

<details>

```python
from fastapi import FastAPI
from ehandler import ExceptionHandlerSetter

app = FastAPI()

handlers = [(ZeroDivisionError, 500), (ValueError, 400)]
ExceptionHandlerSetter(
    content_callback_kwargs={"show_error": True, "show_data": True}
).add_handlers(app, handlers)


@app.get("/value_error")
def raise_value_error():
    raise ValueError("Invalid value")


@app.get("/division")
def call_external():
    return some_func()


@app.get("/uncaught")
def uncaught():
    raise Exception("This error is not handled")


def some_func():
    print("Trying to do something unless that thing get fails")
    return 1 / 0  # This raise a `ZeroDivisionError`
```

`/value_error` - **_HTTP 400 Bad Request_**

```json
{
    "detail": "Bad Request",
    "error": "ValueError",
    "message": "Invalid value"
}
```

`/division` - **_HTTP 500 Internal Server Error_**

```json
{
    "detail": "Internal Server Error",
    "error": "ZeroDivisionError",
    "message": "division by zero"
}
```

`/uncaught` - **_HTTP 500 Internal Server Error_**

```json
Internal Server Error
```

#### **Explanation**

When an error occurs within our server that is not handled (with a `try-except`)
the server will respond with a _500 - Internal Server Error_

`ExceptionHandlerSetter().add_handlers(app, handlers)` Basically create this to
be able to handle specific exceptions (or general if `Exception` is handled)
( [original example](https://fastapi.tiangolo.com/tutorial/handling-errors/?h=#install-custom-exception-handlers) ) :

```python
@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )
```

But with a dynamic/configurable exception and status code and using a function
(callback) as a template, in fact 2 functions/callbacks are used:

- One that parses the content, can take the exception, the request, etc, and
create some content with it.
- The other is the function that returns the response, usually just put it
inside a `JSONResponse`.

```python
@app.exception_handler(<ExceptionClass>)
async def <ResponseCallback>(request: Request, content: Any = <content_callback>, status_code: int = <status_code>)
    return <ContentCallback>,
```

</details>

___

## Examples

### Content callback

<details>

Use your own callback to parse the content of the response

```python
import traceback

from fastapi import FastAPI
from ehandler import ExceptionHandlerSetter

app = FastAPI()

def parse_exception(
    request: Request,
    exception: Exception,
    status_code: int,
    debug: bool = False,
) -> dict:
    content = {"message": "Something went wrong"}
    if debug:
        content["traceback"] = traceback.format_exc()
    return content

handlers = [(Exception, 500)]
ExceptionHandlerSetter(
    content_callback=parse_exception
    content_callback_kwargs={"debug": True}
).add_handlers(app, handlers)
```

</details>

___

### Add additional data

<details>

> ⚠️ This uses the default implementation from `ehandler.parsers.parse_exception`

```python
from fastapi import FastAPI
from ehandler import ExceptionHandlerSetter
from ehandler.utils import add_data

app = FastAPI()

handlers = [(Exception, 500)]
ExceptionHandlerSetter(
    content_callback_kwargs={"show_data": True}  # If `show_data` is False it won't work
).add_handlers(app, handlers)


@app.get("/exception")
def raise_value_error():
    raise add_data(ValueError("Invalid value"), {"user": "user_info"})
```

`/exception` - **_HTTP 500 Internal Server Error_**

```json
{
    "data": {
        "user": "user_info"
    },
    "detail": "Internal Server Error",
    "message": "Invalid value"
}
```

</details>

___

### Change default _status_code_

<details>

```python
from fastapi import FastAPI
from ehandler import ExceptionHandlerSetter
from ehandler.utils import add_code

app = FastAPI()

handlers = [(Exception, 500)]
ExceptionHandlerSetter(force_status_code=False).add_handlers(app, handlers)


@app.get("/exception")
def raise_value_error():
    raise add_code(ValueError("Invalid value"), 400)
```

`/exception` - **_HTTP 400 Bad Request_**

```json
{
    "detail": "Bad Request",
    "message": "Invalid value"
}
```

</details>

## How to contribute

### Prerequisites

> Python ^3.9
>
> poetry ^1.1.14
>
> pre-commit ^2.20.0

<details>
<summary> Install requirements </summary>

### **Install Poetry**

Poetry is a tool for dependency management and packaging in Python. It allows
you to declare the libraries your project depends on and it will manage
(install/update) them for you.

To install poetry you can follow the official documentation on the page according
to your operating system. [Poetry Installation](https://python-poetry.org/docs/#installation)

### **Install Pre-Commit**

It is a multi-language package manager for pre-commit hooks. You specify a list
of hooks you want and pre-commit manages the installation and execution of any
hook written in any language before every commit.

To install poetry you can follow the official documentation on the page according
to your operating system. [Pre-Commit Installation](https://pre-commit.com/#install)

#### **Install hooks**

```bash
pre-commit install
```

</details>

<details>
<summary> Dependencies </summary>

### **Install dependencies**

```bash
poetry install
```

You can also follow the documentation of poetry for a better use of this or any
questions. [Poetry Basic Usage](https://python-poetry.org/docs/basic-usage/)

### **Add dependency**

They are the dependencies that the package needs to work.

```bash
poetry add <package>
```

```bash
poetry add fastapi
```

### **Add dev dependency**

These are the dependencies that you need only for development,
for example those that are needed to test the package.

```bash
poetry add -D <package>
```

```bash
poetry add -D requests
```

</details>

<details>
<summary> Tests </summary>

### **Run test**

#### **Static test**

The analysis or static test is run using pre-commit, you can run a specific
analysis using the id, or run all tests

##### **Single test**

```bash
pre-commit run pylint
```

> ⚠️ Pre-commit by default only runs on files modified in stage.
> If you want to run on all files you can add the `--all-files` flag.

##### **All test**

```bash
pre-commit run
```

##### **All files**

```bash
pre-commit run --all-files
pre-commit run black --all-files
```

#### **Unittest**

```bash
poetry run pytest -v
```

</details>
