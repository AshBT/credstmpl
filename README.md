# credstmpl
Command-line tool to instantiate templates from credentials stored in
credstash and Last Pass.

Because your credentials should be treated like a holy temple.

## Installation
Since this is a small-ish project, we don't (yet) have plans to host
this on PyPi. Therefore,
```
pip install git+https://github.com/qadium/credstmpl.git
```

## Templates
We use Jinja2 templates.

Create a file `foo.sh.j2` (for instance) with the contents
```bash
#!/bin/bash

export MY_SECRET={{ credstash('my_secret') }}
export MY_API_KEY={{ credstash('my_api_key') }}
export MY_OTHER_SECRET={{ lastpass('my_other_secret', field='password') }}
```

Running `credstmpl foo.sh.j2` will write a file `foo.sh` containing your
secrets. It will also politely remind you to add the file to your
`.gitignore` file (or equivalent). Finally, it will `chmod 0600
foo.sh`--only you can read the file.

As a consequence, please don't run this tool with `sudo`.

## Why did we build this?
When using Ansible to provision remote machines, we often have to set
passwords, ssh keys, etc. and commit these files to version control to
share with our team. Ansible vault provides one way of encrypting these
files and committing them to version control. However, it requires
sharing a password that developers must remember.

Recently, Ansible added the ability to "lookup" keys and secrets in
credstash. This means a development team simply needs to ensure all
developers have access to AWS in order to access the (shared) keys and
secrets. More importantly, it means config files containing passwords
and secrets can be committed without leaking any information.

While Ansible provides the ability to insert these secrets into a config
file and "template" them out to a remote server, `credstmpl` is intended
to solve the problem of sharing and creating *local* configurations.

## Alternatives
It's possible to implement something similar using Python's
[ConfigParser](https://docs.python.org/2/library/configparser.html),
with a custom interpolator, but there are cases where one might want
more flexibility than an `ini` file. For instance, if you're stashing
credentials but using them in a language that isn't Python.
