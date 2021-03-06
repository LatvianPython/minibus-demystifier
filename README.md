# minibus-demystifier

Demystifies the arrival of minibuses for a desired route and stop in Riga/Latvia, so you never miss one ever again! 

# example of `slack_app.py`

![Screenshot](doc/sample.png)

# installing

You would need to clone or download the whole repository.

Right now only really supporting *Python 3.7*

Requirements can be installed via:

`pip install -r requirements.txt`

Due to optimizations now need to compile a Cython file

You will need a C compiler

You can compile using

`cythonize.exe -a -i -3 .\geolocation\calculations.pyx`

# how to use

Basic usage is covered in `examples/basic.py`

For some advanced usage examples refer to implementation within `slack_app.py`
