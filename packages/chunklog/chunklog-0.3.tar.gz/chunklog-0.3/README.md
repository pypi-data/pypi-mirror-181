<div align="center">
<img src="./assets/images/chunklog.png" alt="chunklog" width="200" />

# chunklog

</div>

Chunklog is a tool to find a specific section of code in a git repository and show that section's history. It was developed to search for a specific requirement in a project and see how it has changed over time. As a user you specify an identifier of the section of text that is to be found and the git repository to be searched.

The example below shows how changes of a specific section, i.e. in this case a requirement, can be tracked. The output is the history of a section with a unique ID. It shows a list of instances of the section since the creation of the git repository. Each instance represent a change since the last instance. Changes in spaces, newlines and tabs will not be presented.

<div align="center">
<img src="./assets/images/exampleOutput.png" alt="An example output" width="450" />
</div>

## Installation

To install this project run the following command in your virtual environment
```
pip install chunklog
```
The link to the project on PyPi: TBD

## Configuration

A configuration file named config.ini is required to be in the folder .sectionHistory in the root of the target repository, if the program is used as a command line application. Otherwise, it can be solely specified as a string. See example for the usage as a Python library below.

Content of config.ini:

```
[regex_section]
regex_val = my_regex
```

Where my_regex is the regex to match a desired section in the history of the repository. Example configuration files are provided in the folder config-files-examples.

## Cache

The history of different sections will be stored in a cache, which can be local or global. Thus, before retrieving the history of a specific section a cache has to be created.

The folder storing the cache will be called .sectionHistory and we advise to include it in the .gitignore. More specifically the cache will be stored in the subfolder called cache within the folder .sectionHistory. The ID of each section found will be represented as directories within the folder. Inside each directory are json files named after the commit hashes where changes to the sections were made. The json files will contain the entry associated with this section in this commit, i.e. if it was changed. An entry contains information on the file, repo, text and id relevant to the section as well as the commit hash, author, date and message of the commit.

## Usage

### Usage as a command line application

**Retrieve the history of a section**

The history of a specific section can be retrieved by running the following commmand in the repository of your project:

```
python -m chunklog [Identifier]
```
The identifier is the unique ID of the section. If a cache has not been generated in the repository of the current working directory, a prompt will be displayed in the terminal giving the user the possibility to create it or not.

If the cache is stored in for example a global cache, i.e. not in the repo of the current working directory, the following command must be run:
```
python -m chunklog [Identifier] --cache-path [Path]
```
Where Path indicates where the cache is stored. Same as above, if the cache has not been created at the location of the given cache-path, a prompt will be displayed to give the option to do so. Retrieving from multiple caches is also possible, i.e. by including the flag along with a path for each of the caches to retrieve from. It should be noted that by providing more than one cache-path you forgo the possibility of creating one in the provided cache paths, if they are empty.

The specified path to the cache should not include the folder .sectionHistory or .sectionHistory/cache as their existance will be searched in the given path location of the cache and if not found, created at the specified location.

**Update the cache**

To update the cache after the cache has been created the following command can be run:
```
python -m chunklog --update-cache
```

As with retrieving the history, in order to specify where the cache should be stored, it must be added to the command as the following shows:
```
python -m chunklog --update-cache --cache-path [Path]
```
Where Path specifies again where the cache should be stored, if not in the repository in the current working directory. As opposed to retrieving the history from the cache, adding to the cache is only possible for a single cache path at a time.

To force update the cache, i.e. remove the content of the cache and add entries to it again, the following flag can be added:
```
python -m chunklog --update-cache --force
```
The shorthand -f is also applicable.

**Highlighted output**

By default the output will highlight differences between entries of a specific requirement. There's an optional flag available to get the entries without diff highlighting.
```
--no-diff
```

### Usage as a Python library

This is an example of how the project can be used as a Python library.

**Create/Update the cache**

First a cache has to be created. The add_to_cache method expects four arguments, a Repo object pointing to the target repository, a path specifying from where in the repository the history analysis of the sections of code should take place, a Cache object specifying the cache and a regex, i.e. a string of a regular expression which matches the sections of which history will be added to the cache.

```
from chunklog import Cache, add_to_cache
from git.repo import Repo
from pathlib import Path

# The path can be the root of the repo or a subdirectory within it
path = 'path/to/target/repo'

# If the path is a subdirectory we need to also search the parent directories
repo = Repo(path, search_parent_directories=True)

# See examples for regex examples in the folder config-file-examples
regex = 'my-regex'

# Cache should be created in the root of the repository (or in a global cache)
root_path = repo.working_tree_dir
cache = Cache(root_path)

add_to_cache(repo, path, cache, regex)
```

To see the generated cache you can navigate to the target repository and find the .sectionHistory/cache folder which has been generated. You can also make use of the function associated with the Cache dataclass, i.e. check_cache_empty, or call the get_history function below and see the new entries in the output for a specific section.

**Retrieve the history of a section**

To retrieve the history of a section we use the function get_history. It expects two arguments, i.e. firstly a string containing the identifier of a section and secondly a Cache object.

```
from chunklog import Cache, get_history

# Initiate the cache with a global cache path (as an example)
cache = Cache(path_to_global_cache)

# Unique identifier of a specific section
id = 'my-id'

section_history = get_history(id, cache)
```

Now you have retrieved the history of a specified section and can print it in the output on the terminal or feed it into some other functions. If you choose to print it in the terminal you can highlight the output by including the code below to your above code snippet.

**Highlighted output**

To highlight the output in terminal the function parse_entry_output can be used. It takes in two arguments, i.e. a list of entries indicating the history of a section and a boolean value specifying whether the highlight should also include diff formatting of the text in each entry. An example of the diff formatting can be seen in the first figure of this document.

```
from chunklog import Cache, get_history, parse_entry_output

...

parse_entry_output(section_history, True)

```

## Testing

Testing the Section history is made easy with hatch. First follow the steps below to install the project:

1. Clone the git repo
2. Hatch is used as a project manager. To install hatch with pip run the following command in a terminal

    ```
    pip install hatch
    ```
3. To activate the virtual environment, run the following command in the root directory of the repository, i.e. SectionHistory

    ```
    hatch shell
    ```

After initiating the virtual environment in the root of the git repository run

    pytest

or to also get a report for the test coverage

    hatch run cov

All tests from within the tests folder will be run.
