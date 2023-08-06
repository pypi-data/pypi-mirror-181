# Sonotoria

Sonotoria is a library designed to provide features helping with templating and handling yaml files.

# Jinja templating

Sonotoria provides some functions to make the use of jinja2 templating easier.

Note that all the functions presented in this section have the following optional arguments:
 * **context**: A dictionary used as context for the templating
 * **filters**: A dictionary of filters usable during the templating
 * **tests**: A dictionary of tests usable during the templating

Example:
```
// Context
{'key': 'value'} -> {{ test }} -> value

// Filters
{'twotimes': lambda v: v*2} -> {{ test | twotimes }} -> valuevalue

// Tests
{'big': lambda v: len(v) > 10} -> {{ test is big }} -> false
```

## template_string

Shortcut for templating strings:
```py
>>> from sonotoria import jinja
>>> jinja.template_string('Hello {{ hello }}!', context={'hello': 'world'})
Hello world!
```

## template_file

Shortcut for templating files:
```py
>>> from sonotoria import jinja
>>> jinja.template_file('myfile.j2', 'myfile')
```

## template_folder

Shortcut for templating folders:
```py
>>> from sonotoria import jinja
>>> jinja.template_folder('myfolder', 'mytemplatedfolder')
```

Note that the folder can contain an optional template configuration in a `.template` folder. Here you can add config file `config.yaml`.

The config file should like this:
```yaml
---

default: # optional default values for the context
  myvar: myvalue

exclude: # an optional list of file path to ignore
  - .git

template: # use this part to provide information regarding the templating of the folders and files' names
  loop: # The loop section concerns files or folder that should be created using a list, one file/folder will be created for each element of the list
    - folder: myfolder # use file for a file, folder for a folder
      var: folders # the variable from the context that contains the list (required)
      item: folder # the name of the variable in the cotext used to hold the list elements' values
      # If the var name end with an 's', then the item is automatically defined with this name without the s
      # Therefore the 'item' definition here would have been added by default
      transform: my_{{ folder }}_looped # explicit how to transform the folder name, by default it will be named using the item value
      loop: # when looping a folder, you can also loop elements within the folder
        - file: myfile
          loop: # looping is obviously not available for a file, this will result in a configuration error
            ...
      filters: # You can choose filters to apply !on the list! before the templating (filters have the least priority)
        - myfilter
      when: # You can choose test to filter out !element of the list! before the templating
        - mytest
      excluded_values: # You can also exclude values directly (excluded_values have the highest priority)
        - myvalue
  rename: # The rename section is for renaming file or folder without looping (you can create create rename section in looped folder as well)
    - folder: myotherfolder
      var: myvar # When renaming, using var is a shortcut for "transform: {{ myvar }}"
      transform: my_{{ folders[0] | single }} # The transform is used to define how to rename the folder/file if var is also defined a warning will be logged and var will be ignored
      # As we can see in this transform, you can use filters and use typical operations such as the dot and the brackets
      loop: # Once again, when renaming a folder you can use a loop for the elements inside the folder
      rename: # ... or a rename
    - folder: dontchangeme # You can also not change a folder just to perform actions on the element inside
      loop:
        - file: changeme
          var: changes
```

You can also create a `default.yaml` file to hold default values outside of the configuration file. You can use both the default section and the default file. In that case, the default section (in the config file) will have the priority if a variable is defined twice. (And variables passed to the context of the function have obviously the highest priority). You can also create a `vars.yaml` to create variables after the context is loaded and use the context in it (using jinja syntax).

Finally you may also add a `filters.py` and/or a `tests.py` to add filters and tests that will be loading before templating. All they need is to respectively have a `get_filters` and `get_tests` function. Those function must return dictionaries with the filters/tests.


# Loading Yaml

Sonotoria lets you load a yaml with variables using jinja2 syntax:

## Examples

### From a file
Given the file:
```yaml
# test.yml
---

param: value
param2: {{ param }}
```

You can load the data:
```py
>>> from sonotoria import jaml
>>> jaml.load('test.yml')
{'param': 'value', 'param2': 'value'}
```

### From a string
You can also load a string directly:
```py
>>> from sonotoria import jaml
>>> jaml.loads('---\nparam: value\nparam2: {{ param }}')
{'param': 'value', 'param2': 'value'}
```

### Using context
Given the file:
```yaml
# test.yml
---

param2: {{ param }}
```

You can load the data:
```py
>>> from sonotoria import jaml
>>> jaml.load('test.yml', context={'param': 12})
{'param2': 12}
```

### Using filters
Given the file:
```yaml
# test.yml
---

param: value
param2: {{ param | doubled }}
```

You can load the data:
```py
>>> from sonotoria import jaml
>>> jaml.load('test.yml', filters={'doubled': lambda s: s*2})
{'param': 'value', 'param2': 'valuevalue'}
```

### Using tests
Given the file:
```yaml
# test.yml
---

param: value
param2: {{ param is number }}
```

You can load the data:
```py
>>> from sonotoria import jaml
>>> jaml.load('test.yml', tests={'number': lambda s: s.isdigit()})
{'param': 'value', 'param2': False}
```

### Using objects
Given the file:
```yaml
# test.yml
--- !stuff

param: value
param2: {{ param }}
```

You can load the data:
```py
>>> from sonotoria import jaml
>>> class Stuff:
....    pass
>>> my_stuff = jaml.load('test.yml', types={'stuff': Stuff})
>>> my_stuff.param
value
>>> my_stuff.param2
value
```
You can add tests, filters and types:


# Extractor

Sonotoria lets you extract data from a file using a jinja2 template.

## Example

Given this input file:
```
That is a description

:param test: Looks like a test variable, huh
:param lol: This might be a fun variable
:param plop: Plop might just be the next best variable name
:return: Pretty much nothing, sadly
```

And this template file:
```
{{ description }}

{% for param, desc in params.items() %}
:param {{ param }}: {{ desc }}
{% endfor %}{% if return_given %}
:return: {{ return }}{% endif %}{% if rtype_given %}
:rtype: {{ rtype }}{% endif %}
```

You can extract data this way:
```py
>>> import sonotoria
>>> sonotoria.extract('template.file', 'input.file')
{
    'description': 'That is a description',
    'params': {
        'test': 'Looks like a test variable, huh',
        'lol': 'This might be a fun variable',
        'plop': 'Plop might just be the next best variable name'
    },
    'return': 'Pretty much nothing, sadly',
    'rtype': None,
    'return_given': True,
    'rtype_given': False
}
```

# Contributors

 * Emmanuel Pluot (aka. Neomyte)
