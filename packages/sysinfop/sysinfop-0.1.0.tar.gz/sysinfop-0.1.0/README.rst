sysinfop
========

Lightweight system info utility

   Sysinfop is my own attempt at a *Neofetch* / *Screenfetch* style cli
   app. Sysinfop Is built using Python3 and requires both a working
   Python3 install as well as the Poetry build tool available on your
   system if you are building the project from source. Pre-built
   ``wheel``, ``sdist``, ``.exe`` (Windows), and ``.app`` (MacOS) assets
   will be available soon...

What does it look like?
-----------------------

On a 2022 Macbook Air for example, it will output the following.

.. code:: shell

     hostname.local
     * IP: 127.0.0.1
     * OS: Darwin
     * CPU: arm
     * RAM: 8 GB

How to use it
-------------

Simply call ``sysinfop`` from your shell configuration.

bash
~~~~

.. code:: shell

   $ echo "sysinfop" >> ~/.bashrc

zsh
~~~

.. code:: shell

   $ echo "sysinfop" >> ~/.zshrc

How to install it
-----------------

Install from pip
~~~~~~~~~~~~~~~~

.. code:: shell

   pip install sysinfop

Contributing
------------

The project is a simple Python 3 app that is built using the Poetry
tool, this is all you need to contribute. PR's, issues, etc. all
directed to this github repo.

LICENSE
-------

MIT License

Copyright (c) 2022 Josh Burns josh@joshhburns.xyz

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
