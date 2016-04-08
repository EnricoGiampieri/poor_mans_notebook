# poor_mans_notebook
simple program to convert python source files to interactive html in a notebook-ish looking way

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

## How this program came to be

On top of these points, the one I care the most is the mindset that different instruments favors.
In my experience, jupyter notebooks bring the scientist to hack it up until it has a results, without caring for a formal method.
I observed the same behavior in most of my students, were the notebooks brought them to write spaghetti code, as a single block due to the difficult of importing code from one notebook to the other.
Never underestimate the path of least resistance.
I got so fedup that I actually stopped teaching them about notebooks, working instead in spyder.
I saw a net improvement in the quality of the code, but the price was losing the ability to merge in a meaningful way information, formulas, images and so on in the code.
I tried to implement different versions of the sandbox-code approach, where the program would execute the code in a sandbox, intercepting the result and pasting it.
It worked, but it was horrible.

