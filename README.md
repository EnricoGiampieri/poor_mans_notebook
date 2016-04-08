# PMN (The Poor Man's Notebook)
simple program to convert python source files to interactive html in a notebook-ish looking way

WARNING - this script is extremely in the alpha stage! it shouldn't do any damage in any way to your work, but it is lacking all the testing and infrastructure necessary to be called a real program!

## Usage

1. copy the script in the directory where you plan to use it.
2. run your program as usual (it should save figures and other material on disk)
3. sun the script on your file. It will generate the rst, compile in html and open it with your default browser.
4. enjoy!

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

## Why ReStructuredText Nnd Not MarkDown?
I love markdown, but I think that for this kind of projects the rst is the way to go for the following reasons:

* scientific python (and python in general) already use rst for the documentation, and they are doing great with it. When possible, it's better to not deviate from the standards
* Markdown is a very variable format, and there are 2'000 flavours of it. Rst is more standardized and will less variants, and this mean one less detail to take care about
* RST comes with a lot of batteries included, like the possibility of code formatting, ordered and named references in the text and so on. Using it smartly could be easily used to write a full scientific paper.



