q_step = 0
answers = []
query_params = []
cmd = ''
user_level = 0

########## Functions #############

def RunCode(code, globals = {}, locals = {}):
    with open('__tmp__.py', 'w') as file:
        file.write(code)
    execfile('__tmp__.py', globals, locals)
    if 'message' in locals.keys():
        return locals
    else:
        return {'message' : '', 'chatid_list' : []}
    
def execfile(filepath, globals=None, locals=None):
    if globals is None:
        globals = {}
    globals.update({
        "__file__": filepath,
        "__name__": "__main__",
    })
    with open(filepath, 'rb') as file:
        exec(compile(file.read(), filepath, 'exec'), globals, locals)