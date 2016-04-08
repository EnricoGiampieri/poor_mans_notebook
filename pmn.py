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
<link rel="stylesheet" type="text/css" href="style.css">
<link rel="stylesheet" type="text/css" href="user.css">
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
Creating the CSS file
~~~~~~~~~~~~~~~~~~~~~

to reduce the number of files necessary to be around, I will create the css style sheet from here.
It doesn't look good, but the alternative is that losing the main one everything looks horrible.
Also this means that the whole thing would become a one file script, that is always better!
"""

CSS_autohide_code = """
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

"""

CSS_general_look = """
/*
:Authors: Ian Bicking, Michael Foord
:Contact: fuzzyman@voidspace.org.uk
:Date: 2005/08/26
:Version: 0.1.0
:Copyright: This stylesheet has been placed in the public domain.

Stylesheet for Docutils.
Based on ``blue_box.css`` by Ian Bicking
and ``html4css1.css`` revision 1.46.
*/

@import url(html4css1.css);

body { font-family: Arial, sans-serif; }
em, i { font-family: Times New Roman, Times, serif; }
a.target { color: blue; }
a.target { color: blue; }
a.toc-backref { text-decoration: none; color: black; }
a.toc-backref:hover { background-color: inherit;}
a:hover { background-color: #cccccc; }

div.attention, div.caution, div.danger, div.error, div.hint,
div.important, div.note, div.tip, div.warning {
  background-color: #cccccc;
  padding: 3px;
  width: 80%;
}

div.admonition p.admonition-title, div.hint p.admonition-title,
div.important p.admonition-title, div.note p.admonition-title,
div.tip p.admonition-title  {
  text-align: center;
  background-color: #999999;
  display: block;
  margin: 0;
}

div.attention p.admonition-title, div.caution p.admonition-title,
div.danger p.admonition-title, div.error p.admonition-title,
div.warning p.admonition-title {
  color: #cc0000;
  font-family: sans-serif;
  text-align: center;
  background-color: #999999;
  display: block;
  margin: 0;
}

h1, h2, h3, h4, h5, h6 {
  font-family: Helvetica, Arial, sans-serif;
  border: thin solid black;
  /* This makes the borders rounded on Mozilla, which pleases me */
  -moz-border-radius: 8px;
  padding: 4px;
}

h1 {
  background-color: #444499;
  color: #ffffff;
  border: medium solid black;
}

h1 a.toc-backref, h2 a.toc-backref { color: #ffffff; }
h2 {
  background-color: #666666;
  color: #ffffff;
  border: medium solid black;
}

h3, h4, h5, h6 { background-color: #cccccc; color: #000000; }

h3 a.toc-backref, h4 a.toc-backref, h5 a.toc-backref,
h6 a.toc-backref { color: #000000; }

h1.title {
  text-align: center;
  background-color: #444499;
  color: #eeeeee;
  border: thick solid black;
  -moz-border-radius: 20px;
}

table.footnote {  padding-left: 0.5ex;}
table.citation { padding-left: 0.5ex }
pre.literal-block, pre.doctest-block {border: thin black solid; padding: 5px;}
.image img {border-style : solid; border-width : 2px;}
h1 tt, h2 tt, h3 tt, h4 tt, h5 tt, h6 tt {font-size: 100%;}

"""

CSS_code_highlight = """
/* example stylesheet for Docutils */

/* :Author:    Günter Milde */
/* :Copyright: © 2012 G. Milde */
/* :License:   This stylesheet is placed in the public domain. */

/* Syntax highlight rules for HTML documents generated with Docutils */
/* using the ``--syntax-highlight=long`` option (new in v. 0.9). */

/* This stylesheet implements Pygment's "default" style with less rules than */
/* pygments-default using class hierarchies.                                 */
/* Use it as example for "handcrafted" styles with only few rules.      */

.code                              { background: #f8f8f8; }
.code .comment                     { color: #008800; font-style: italic }
.code .error                       { border: 1px solid #FF0000 }
.code .generic.deleted             { color: #A00000 }
.code .generic.emph                { font-style: italic }
.code .generic.error               { color: #FF0000 }
.code .generic.heading             { color: #000080; font-weight: bold }
.code .generic.inserted            { color: #00A000 }
.code .generic.output              { color: #808080 }
.code .generic.prompt              { color: #000080; font-weight: bold }
.code .generic.strong              { font-weight: bold }
.code .generic.subheading          { color: #800080; font-weight: bold }
.code .generic.traceback           { color: #0040D0 }
.code .keyword                     { color: #AA22FF; font-weight: bold }
.code .keyword.pseudo              { font-weight: normal }
.code .literal.number              { color: #666666 }
.code .literal.string              { color: #BB4444 }
.code .literal.string.doc          { color: #BB4444; font-style: italic }
.code .literal.string.escape       { color: #BB6622; font-weight: bold }
.code .literal.string.interpol     { color: #BB6688; font-weight: bold }
.code .literal.string.other        { color: #008000 }
.code .literal.string.regex        { color: #BB6688 }
.code .literal.string.symbol       { color: #B8860B }
.code .name.attribute              { color: #BB4444 }
.code .name.builtin                { color: #AA22FF }
.code .name.class                  { color: #0000FF }
.code .name.constant               { color: #880000 }
.code .name.decorator              { color: #AA22FF }
.code .name.entity                 { color: #999999; font-weight: bold }
.code .name.exception              { color: #D2413A; font-weight: bold }
.code .name.function               { color: #00A000 }
.code .name.label                  { color: #A0A000 }
.code .name.namespace              { color: #0000FF; font-weight: bold }
.code .name.tag                    { color: #008000; font-weight: bold }
.code .name.variable               { color: #B8860B }
.code .operator                    { color: #666666 }
.code .operator.word               { color: #AA22FF; font-weight: bold }

"""

CSS_data = CSS_autohide_code + CSS_general_look + CSS_code_highlight

with open("./style.css", "w") as css_file:
    print(CSS_data, file=css_file)

"""
Opening In The Browser
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Why press two buttons when you can get around with a single one?
"""

webbrowser.open_new_tab(html_file)
