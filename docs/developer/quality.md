<h1>Quality</h1>
The project tries to follow some basic guidelines to improve code and documentation quality in order to help future contributors. 
This section defines the general development workflow, code standards, and method of code documentation. 

## Workflow
New features are developed on a separate feature branch.  
This allows you to work independently on a feature and still share code. Push feature branch commits often to communicate what you are working on.  
Read more about this workflow [here](https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow).

## Code standards
The default Python and Django [code style](https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/) is used.  
Write code as simple as possible and focus on readability. Write code for others to understand and read.

*"Always code as if the person who ends up maintaining your code is a violent psychopath who knows where you live. "* - [source](http://c2.com/cgi/wiki?CodeForTheMaintainer)

##### Flake8
Flake8 is a Python tool to check code style. It runs automatically on Travis after each commit.  
You can find the Flake8 output in the [latest Travis build log](https://travis-ci.org/jonge-democraten/website).

## Code documentation
Add comments to code that is not self-explanatory.  
Use [python docstrings](http://en.wikipedia.org/wiki/Docstring#Python) to describe files, classes and functions.  
Add a brief docstring to files and classes. To functions only if necessary. Example,
```python
"""
File description.
"""

class ExampleClass(Example):
    """ Class description. """

    def example_function(self):
        """
        Function description 
        on multiple lines.
        """
``` 
