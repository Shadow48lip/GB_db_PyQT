# правильно
i = i + 1
submitted += 1
x = x * 2 - 1
hypot2 = x * x + y * y
c = (a + b) * (a - b)

# неправильно
i=i+1
submitted +=1
x = x*2 - 1
hypot2 = x*x + y*y
c = (a+b) * (a-b)


# правильно
def complex(real, imag=0.0):
    return magic(r=real, i=imag)


# неправильно
def complex(real, imag = 0.0):
    return magic(r = real, i = imag)

# правильно
if foo == 'blah':
    do_blah_thing()
do_one()
do_two()
do_three()

# неправильно
if foo == 'blah': do_blah_thing()
do_one(); do_two(); do_three()
