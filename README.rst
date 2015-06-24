==================
1 Impaf experiment
==================
Impaf is an experiment in which we trying to create web framework which uses
inheritance as much as it can. It is not a complete framework, because to run
we use Pyramid framework. But it serves its purpose.

1.1 Ideology
============
First of all, we wanted to use inheritance as much as we can, to see is is worth
it. Python inheritance (with MRO) is one of a kind, and we think it is very
powerfull.

Also we wanted to achive is pluginable design. So if you want to use
sqlalchemy plugin but you do not want to use a small part of it, you should be
abel to very quickly change it by inheritance of the part.

Another point we want to achive is very descriable code. We will not use any
"Convention Over Configuration" or something like that, because it make code
very blurry for new people. We are trying to not make "magic" here, just code.
(Magic is when you now it is working, but you can not tell why.)

=================
2 Impaf workspace
=================
This repository is not a core repository. Impaf is distributed into many plugins.
This is a workspace repository.

2.1 core
========
Repository for the core of the impaf

2.2 jinja2
==========
Repository for jinja2 support.

2.3 haml
========
Repository for the jinja2 hamlish support.

2.3 sqlalchemy
==============
Repository for sqlalchemy support.

2.4 alembic
===========
Repository for the alembic support.

2.5 example
===========
Repository for example web application made on top of the Impaf.

============
3 How to run
============
First you should use makefile and just run:

    make

It should download all dependencies, create virtualenv and make ready to go
example application. Now you can just go to "example" dir and run this:

    pserve frontend.ini --reload
