# PMN (The Poor Man's Notebook)
simple program to convert python source files to interactive html in a notebook-ish looking way

WARNING - this script is extremely in the alpha stage! it shouldn't do any damage in any way to your work, but it is lacking all the testing and infrastructure necessary to be called a real program!

## Usage

1. copy the script in the directory where you plan to use it.
2. run your program as usual (it should save figures and other material on disk)
3. sun the script on your file. It will generate the rst, compile in html and open it with your default browser.
4. enjoy!

if you want to personalize the css style and keep it stable between runs of the program, do not modify the style.css (it gets rewritten everytime)
but rather edit (create if there is none) a css file called `user.css`. This file is imported by default and it is after the base one, overwriting any configuration you want.

##Examples

PMN applied to itself. The html contains all the info and effect, and rst, while not enabled to autofold the code, it's still quite usable. 

* html version: https://rawgit.com/EnricoGiampieri/poor_mans_notebook/master/examples/pmn_itself/pmn.html
* rst version: https://github.com/EnricoGiampieri/poor_mans_notebook/blob/master/examples/pmn_itself/pmn.rst

A toy example of including files and image, bot png, svg and dynamic (using bokeh).
Due to limitation in the GitHub preview system, the svg and html are not rendered in the rst version, so check the html one

* html version: https://rawgit.com/EnricoGiampieri/poor_mans_notebook/master/examples/display_random_objects/test_figures.html
* 
The html is generated using http://rawgit.com/

## Rationale

This package is thought as an aid to literate programming in the scientific programming world.
Many solutions exists for this and each one has its own distinctive pros and cons.
One of the main solution that is gaining traction is by far the Jupyter notebook, with the weaving techniques that come second.
Personally I found myself uncomfortable with both, so I went and created my own solution.

the Poor Man's Notebook take a standard python source code, with no special syntaxis added.
It will process all the string at the main level (not the docstrings) as rst blocks and insert some html and css styling for good reason, then compile everything to an html file.

This html file contains the documentation and the source code (collapsed by default, to give the best view experience of the documentation).
Beware: It will not execute the code in any way!
If you want to include the results of your simulation, you have to save them to file and include them explicitly.
That's all.

there are several advantages to this naive approach:

* secure by default: no code get executed, not complicated sandboxes are necessary
* recompiling the documentation does not require running the code again: if the simulations last hours, you definitely don't want to have to run them everytime
* compatible with Version Control: have you ever tried keeping a notebook in git? then you know the pain
* simple as it can be: just run the program with the target file as argument, no need to complicated pipelines of parameters mangling
* pythonic: explicit is better than implicit
* non-local references: the code and its results are not linked together forcibly, but they can be moved areound without problems. I don't even need the code to a certain figure to be in the same text, without weirded out.
* full information without visibility price: the html format allow to have the code hidden by default, but visible at will, so the focus is on the narative unless checking the source code becomes relevant

## How This Program Came To Be

On top of these points, the one I care the most is the mindset that different instruments favors.
In my experience, jupyter notebooks bring the scientist to hack it up until it has a results, without caring for a formal method.
I observed the same behavior in most of my students, were the notebooks brought them to write spaghetti code, as a single block due to the difficult of importing code from one notebook to the other.
Never underestimate the path of least resistance.
I got so fed up that I actually stopped teaching them about notebooks, working instead in spyder.
I saw a net improvement in the quality of the code, but the price was losing the ability to merge in a meaningful way information, formulas, images and so on in the code.
I tried to implement different versions of the sandbox-code approach, where the program would execute the code in a sandbox, intercepting the result and pasting it.
It worked, but it was horrible.
A lot of hacks were necessary to keep things in line, import hacking, monkey patching, special cases and syntax.

In the end I tried to keep things to the minimum, just converting the rst and including the text, and slowly realized that it meant actually more freedom and power rather than less.
Ok, including and image meant writing 3 more lines (one of python and two in rst), but allow way more freedom to put things where and how I wanted it, without worries about presentation during the code and experimentation phase, and vice versa.
So I dedided to stick with that road, keeping it simple and light.

This mean also that the documentation necessary is borderline nil.
You just need to write you python code, and put some docstrings in the code.
The program have almost no moving parts, so basically no configuration is necessary.
Working with standard instruments like rst, html and CSS meant that I could leverage all that power without trying to reinvent the wheel, and that is always a good thing.
If you want to reconfigure how things look, you can just edit the css file and you're done, with as much detail of control as you want.

## Related Libraries

Due to its static way of working, PMN works very well with some other library for data analysis.
Combining them together could lead to excellent results, so I strongly suggest to take a look at them!

### [Sumatra](http://pythonhosted.org/Sumatra/)
[Sumatra](http://pythonhosted.org/Sumatra/) works on top of a version control system, and keeps automatically tracks of all the results (stored as file) as a function of the input and code of your program.
It is foundamental to keep a virtual notebook with the results of all your simulations, so it will not be a mistery anymore how those results were obtained two years ago.

### [Ruffus](http://www.ruffus.org.uk/) & [Luigi](http://luigi.readthedocs.org/en/stable/)

Both these libraries manage the workflow pipeline, connecting one piece of code to the other by the creation and update of intermediate files, with a principle similar to the old time `make`.
They both manage pipeline interruption quite easily, but they work on different scales: [Ruffus](http://www.ruffus.org.uk/) is quite quick and easy to set up, while [Luigi](http://luigi.readthedocs.org/en/stable/) requires more boilercode, but it does offer a very comfortable web interface to manage the progression of the pipeline, both locally and remotely, making big batch job like bioinformatic processing as easy as possible.

### [Bokeh](http://bokeh.pydata.org/en/latest/)

This plotting library works very well, and is easy to make play nicely with the old-timey matplotlib.
The interesting advantage is that it is able to save the plot as an html file, that contains the whole visualized dataset and the code to interact with it, allowing to export good looking and interactive visualization with your poor man's notebook.

## Question Time

### Why ReStructuredText and not MarkDown?
I love markdown, but I think that for this kind of projects the rst is the way to go for the following reasons:

* scientific python (and python in general) already use rst for the documentation, and they are doing great with it. When possible, it's better to not deviate from the standards
* Markdown is a very variable format, and there are 2'000 flavours of it. Rst is more standardized and will less variants, and this mean one less detail to take care about
* RST comes with a lot of batteries included, like the possibility of code formatting, ordered and named references in the text and so on. Using it smartly could be easily used to write a full scientific paper.

### Why you don't parse higher level docstring, such as for functions and classes?
Several reasons:

1. doing that woud require to either replicate the documentation, having it both in the code and the text
2. would force the docstring to appear in the text. The two could have no relation, so it's better to separate them
3. would force the docstring to be written in rst. As much as I think it should be a standard, I don't want to enforce that.
4. It might render the code wrong if copied and pasted. I like the possibility of doing that.
5. Would require much more hacking: the more the code, the more the moving parts, the greater the chances of something going wrong

### How come I get Syntax Errors from my file even if I'm not running it?
To process the source code the program uses the AST module, that means that it also performs a syntax check of your code.
If PMN does not parse it python would not run it, so there is some problem there!

### The CSS is hardcoded in the source code, that's bad practice!
We agree, but this bad practice allow the program to be fuly self contained. This means that you can just drag and drop it in your folder and not worry about anything else. 
You can add your own css in there and put all the configurations you want.

I think that this is worth the price of a little bit of hard coding.

### Your code is looks like shit and it's badly written!
We agree.
The first worry was to put out there a working prototype, style can come later.
Any PR is welcome, if you feel like it.

### Why using strings and not comments?
First, strings are used commonly for documentation in python, and are often.
Second, the string format is quite similar among different languages, so it would be easier to generalize it, while the comments can vary wildly.
Third, comment are commonly used to describe the code rather than to document the high level concepts; forcing a meaning in that would make it harder to port old code and write anew
Fourth, comments already have a meaning in certain packages, like cython and python 3 (for type hinting); using comments as meaningful syntax will collide with those uses.

## Known Issues

### Version specificity
I would like the code to be able to process older versions of python and maybe cython or ipython scripts.
This would require moving away from AST and tokenizer to a regex approach, at least to my knowledge.

### Document title
In some cases implementing interactive figures like those generated by bokeh will modify the header of the document.
Those HTML files should be sanitized before importing, but I'm not sure on which the best approach would be

### Interaction of code folding
some HTML code injection can lead to misbehavior of the code folding CSS in an unpredictable way, still trying to understand what's going on.

