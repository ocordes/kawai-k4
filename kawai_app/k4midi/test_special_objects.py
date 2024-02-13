

#func = getattr(K4MultiInstrument, funcname)
#if type(func) == property:
#    func.fset(self._multi, val)
#else:
#    func(self._multi, val)



class Section(object):
    def __init__(self, data, start):
        self._data = data
        self._start = start

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

    #value3 = property(get_val_template(1234), set_val_template(1234))
    value4 = property(*func_template(2345))

    def get_val(self, funcname):
        def f():
            print('>internal2<')
            return 42

        setattr(self, funcname, property(f))
        self.value2 = property(f)

    def set_val(self, funcname):
        def f(val):
            print('>internal<', val)

        setattr(self, funcname, f)

    def read_val(self, val):
        pass

    def test(self, val1, val2):
        self.set_val('set_value1')
        self.set_value1(val1)

        self.get_val('value1')
        self.value3 = val2
        print(self.value3)

        #self.value4 = 1234

class Test(object):
    sections = [Section(1,2), Section(3,4), Section(5,6), Section(7,8)]
    def __init__(self):
        #self.sections = [Section(1,2), Section(3,4), Section(5,6), Section(7,8)]
        pass

# main

t = Test()

t.sections[0].test(-1, -2)

funcname = 'sections[0]'
#func = getattr(Test, funcname)
func = t.__getattribute__(funcname)

print(type(func))