# function generator

class Test(object):
    def __init__(self):
        self._data = 9876

    def read_val(self, val):
        pass

    def set_val(self, funcname):
        def f(val):
            print('>internal<', val)

        setattr(self, funcname, f)


    def get_val(self, funcname):
        
        def f():
            print('>internal2<')
            return 42

        setattr(self, funcname, property(f))
        self.value2 = property(f)

    def get_val_template(val):
        def f(self):
            print('>internal3<', self._data)
            return val

        return f

    def set_val_template(val):
        def f(self, newval):
            print('>internal4<', newval)

        return f


    def func_template(val):
        def set_f(self, newval):
            print(f'set value @{val}: {newval}')

        def get_f(self):
            print(f'get value @{val}')

        return get_f, set_f

    value3 = property(get_val_template(1234), set_val_template(1234))   
    value4 = property(*func_template(2345))

# main
t = Test()
t.set_val('set_value1')
t.set_value1(10)

t.get_val('value1')
t.value3 = 4
print(t.value3)

t.value4 = 1234
print(t.value4)

