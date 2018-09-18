# Welcome to Wonky

This project demonstrates some basic tips for creating numerics projects in physics, but keeping an eye on importing some best practices etc. from software engineering. 
Many software engineering best practices can be relevant (when modified slightly) but may often be overlooked in science-related software projects, which emphaize different things. Topics include patterns, scaffolding projects, data management and "dev ops for physicists" all demonstrated either in the sample project or the notebooks.

### About the sample code
What the actual code does is not so important because this is precisely about all the meta-stuff around the code function. However, the example does illustrate the type of code one may write in complex systems or statistical physics for example. Often, the model itself is relatively simple and most of the code is actually for data collection etc. Often the same boilerplate can be used over and over again in different, changing only the model. The current sample simulates an arbitrary multi-species chemical reaction network on a regular hyperlattice and collects statistics about the number of each space and the trace of each species as a function of time. The data are collated into a consitent file structure for analyis in notebooks.

## 01 Patterns and style
Why? Maintenance. Cleanliness. Dealing with project uncertainty in a non ad-hoc way

How? Appropriate abstractions. Modularity. Reuse. Separation of concerns. Small functions. 

### Some things to Consider...

Understand the difference between objected-orientated and functional orientated programming but don't get caught up in the pointless debate. Partially ignoring my own advice, I find FP far more beautiful and fun (maybe because I learned it second) but there is obvioulsy a time and a place. Google the debate. 

### Links

Example Style guides

[Python] https://www.python.org/dev/peps/pep-0008/

[Julia] https://docs.julialang.org/en/v0.6.2/manual/style-guide/

[Clean code] https://www.investigatii.md/uploads/resurse/Clean_Code.pdf

Example Design patterns 

[Airbrake] https://airbrake.io/blog/design-patterns/software-design-patterns-guide

[The old classic] [Gang of four](https://www.amazon.co.uk/Design-Patterns-Object-Oriented-Addison-Wesley-Professional-ebook/dp/B000SEIBB8 )

On Refactoring 

[Berkeley Inst. Data Science] https://bids.berkeley.edu/news/joy-code-refactoring

[Martin Fowler] https://martinfowler.com/tags/refactoring.html

On Debugging

[Example tips] https://embeddedartistry.com/blog/2017/9/6/debugging-9-indispensable-rules

[Python in VS Code] https://code.visualstudio.com/docs/python/debugging

Discussions

[Speaking against scientific code] https://techblog.bozho.net/the-astonishingly-low-quality-of-scientific-code/

[Repudiation] https://yosefk.com/blog/why-bad-scientific-code-beats-code-following-best-practices.html


## 02 DevOps (or something like it)

## 03 Numerical matters

### links

[Numba](https://numba.pydata.org/)
