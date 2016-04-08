"""
=======================
THE POOR MAN'S NOTEBOOK
=======================

:Author: Enrico Giampieri
:Contact: enrico.giampieri@unibo.it
:Version: 0.1
:Date: 2016/04/07
:Copyright: Python Software Foundation License (PSFL)

Introduction
---------------

This software create an html version of a piece of code.
It will note execute it, but only convert floating strings as rst.

If you want to actually show something, save it to disk and include it!

from the python zen::

    >>> import this
    ...
    explicit is better than implicit
    ...


.. DANGER::

   .. image:: https://openclipart.org/image/300px/svg_to_png/1157/ryanlerch-Other-Dangers-Sign.png
      :align: left
      :width: 20%

   This software is **EXTREMELY** in alpha state.
   Should not be able to do any damage, but BEWARE!

The Code
---------------

Imports
~~~~~~~~

`tokenize` and `ast` are used to correctly parse the python file.

`docutils` is used to convert the rst code to html.
"""

import tokenize
import itertools as it
import ast
import sys
import webbrowser

from docutils.core import publish_parts

"""
Filename and Parameters Detection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

if len(sys.argv) > 1:
    myname = sys.argv[1]
else:
    myname = sys.argv[0]

"""
First Crunching
~~~~~~~~~~~~~~~~~

`is_info_string` test if a given token produced by the tokenizer is a good
text string. To be, it must be not only a string, but also start at the
beginning of the line.
"""

def is_info_string(token):
    return token.type == tokenize.STRING and token.start[1] == 0


with open(myname, 'rb') as myfile:
    tokens = list(tokenize.tokenize(myfile.readline))
    comment_tokens = [token for token in tokens if is_info_string(token)]
    comment_position = [(t.start[0]-1, t.end[0]) for t in comment_tokens]

"""
Second Crunching
~~~~~~~~~~~~~~~~~

`inside_comment_line` check that the given lineindex is inside the range
of the found comment by the `is_info_string` function.
"""

def inside_comment_line(line_info):
    line_idx, line = line_info
    for bottom, top in comment_position:
        if bottom <= line_idx < top:
            return True
    return False

with open(myname, 'r') as myfile:
    divide_file = it.groupby(enumerate(myfile.readlines()),
                             inside_comment_line)
    divide_file = [(truth, [l[1] for l in lines])
                   for truth, lines in divide_file]

"""
Transformation to RST
~~~~~~~~~~~~~~~~~~~~~
"""

link_head = """

.. raw:: html

    <embed>
    <input type="checkbox" id="cb{0}"/><label for="cb{0}">Show Code</label>
    </embed>

"""

result_lines = []

for block_num, (truth, lines) in enumerate(divide_file):
    if not truth:
        lines = str.join("\n", ('   '+line.rstrip() for line in lines))
        # this is necessary to avoid problems with white lines
        # at the end of the file or in the middle of nothign
        lines_test = lines.rstrip().strip()
        if lines_test:
            lines = link_head.format(block_num)+".. code:: python\n\n"+lines
        else:
            lines = '\n\n'

    else:
        lines = str.join("", lines)
        tree = tree = ast.parse(lines)
        nodes_str = [node.s for node in ast.walk(tree) if isinstance(node, ast.Str)]
        lines = str.join("", nodes_str)
    result_lines.append(lines)


"""
Creation of The RST and HTML Files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

rst = str.join("\n", result_lines)
html_doc = publish_parts(rst.encode('utf8'),
                         writer_name='html',
                         settings_overrides={'input_encoding': 'utf8'})

css_head = """
<head>
<link rel="stylesheet" type="text/css" href="voidspace.css">

<style type="text/css">

label{
	background-color: #AAAFAB;
	border-radius: 5px;
	padding: 3px;
	padding-left: 25px;
	color: white;
}

input[type=checkbox] { display: none; }
input[type=checkbox] ~ .code {
	max-height: 0;
	max-width: 0;
	opacity: 0;
   -webkit-transition:all 1s ease;
   -moz-transition:all 1s ease;
   -o-transition:all 1s ease;
   transition:all 1s ease;

}
input[type=checkbox]:checked ~ .code {
	max-height: 100%;
	max-width: 100%;
	opacity: 1;
}
input[type=checkbox] + label:before{
	transform-origin:25% 50%;
  border: 8px solid transparent;
  border-width: 8px 12px;
  border-left-color: white;
  margin-left: -20px;
	width: 0;
	height: 0;
	display: inline-block;
	text-align: center;
	content: '';
	color: #AAAFAB;
   -webkit-transition:all .5s ease;
   -moz-transition:all .5s ease;
   -o-transition:all .5s ease;
   transition:all .5s ease;
	position: absolute;
	margin-top: 1px;
}
input[type=checkbox]:checked + label:before {
	transform: rotate(90deg);
	/*margin-top: 6px;
  margin-left: -25px;*/
}
</style>

</head>
"""

html = html_doc['meta'] + css_head + html_doc['html_body']

"""
Printing Them Out
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
html_file = myname.replace('.py', '.html')

with open(myname.replace('.py', '.rst'), 'w') as outfile:
    outfile.write(rst)

with open(html_file, 'w') as outfile:
    outfile.write(html)

"""
Opening In The Browser
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Why press two buttons when you can get around with a single one?
"""

webbrowser.open_new_tab(html_file)
