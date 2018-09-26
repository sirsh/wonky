# Welcome to Wonky

This project demonstrates some basic tips for creating numerics projects in physics, but keeping an eye on and importing some best practices etc. from software engineering. 
Many software engineering best practices can be relevant (when modified slightly) but may often be overlooked in science-related software projects, which emphasize different things. Topics include patterns, scaffolding projects, data management and "dev ops for physicists" all demonstrated either in the sample project or the notebooks.
This project was created for the __Workshop On Numerical methods in KomplexitY__ organised by the Nonequilibrium physics group at Imperial College London.

![](https://github.com/sirsh/wonky/blob/master/images/ScyOps.png)

### About the sample code
What the actual code does is not so important because this is precisely about all the meta-stuff around the code function. However, the example does illustrate the type of code one may write in complex systems or statistical physics for example. Often, the model itself is relatively simple and most of the code is actually for data collection etc. Often the same boilerplate can be used over and over again in different research projects, changing only the model. The current sample simulates an arbitrary multi-species chemical reaction network on a regular hyperlattice and collects statistics about the number of each species and the trace of each species as a function of time. The data are collated into a consistent file structure for analysis in notebooks. See the [guide](https://github.com/sirsh/wonky/blob/master/guide.ipynb).

## 01 Patterns, paradigms and style
Patterns, why? Maintenance. Cleanliness. Dealing with project uncertainty in a non ad-hoc way

Patterns, How? Appropriate abstractions. Modularity. Reuse. Separation of concerns. Small functions. 

### Some things to consider about mixing paradigms...

Scientific code should properly mix paradigms such as OOP, FOP and VOP. See the Wiki post on [mixing paradigms](https://github.com/sirsh/wonky/wiki/Mixing-Paradigms)

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

Discussions

[Speaking against scientific code] https://techblog.bozho.net/the-astonishingly-low-quality-of-scientific-code/

[Repudiation] https://yosefk.com/blog/why-bad-scientific-code-beats-code-following-best-practices.html


## 02 DevOps (or something like it)
[DevOps](https://en.wikipedia.org/wiki/DevOps) in software engineering is interesting because it represents the evolution of software engineering culture towards automated management of the software lifecycle. Often times, this is about "operations" i.e ensuring software is up and running 24/7. Therefore in science, where often we don't care if our software is "live" or even if it has a "life-time" beyond the current project, Dev-Ops may seem redundant. What can scientists learn from the Dev Ops movement? In a nutshell, perhaps things like automating repetitive tasks,  [unit testing](https://en.wikipedia.org/wiki/Test-driven_development) for rigour and source control ([git](https://en.wikipedia.org/wiki/Git)) and other practices for sharing and [reproducibility](https://en.wikipedia.org/wiki/Reproducibility). Sometimes sharing/reproducibility just means sharing with your future self! Interestingly, it is far, far easier to "excuse" one's self for not adopting certain practices in science compared to software engineering. The mistake may be in believing that the demands of each domain are really so different.

### Links

Lessons from the 'middle ground'...

[DevOps in data science](https://redmonk.com/dberkholz/2012/11/06/what-can-data-scientists-learn-from-devops/)


## 03 Numerical matters

### links

[Numba](https://numba.pydata.org/)

[Numpy (basics)](https://realpython.com/numpy-array-programming/)

[100 Numpy excercises](http://www.labri.fr/perso/nrougier/teaching/numpy.100/index.html)

[Einsum](http://ajcr.net/Basic-guide-to-einsum)

## 04 Other things

On Debugging

[Example tips] https://embeddedartistry.com/blog/2017/9/6/debugging-9-indispensable-rules

[Python in VS Code] https://code.visualstudio.com/docs/python/debugging
