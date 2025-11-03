from .main import getLine, chat, context, PROMPTER, I
from .abscontext import ContextObj

def __getattr__(name):
    global context
    print(f'New function: {name}')
    line, comment = getLine(name)
    def _catchParams(*args, **kwargs):
        pargs = [type(a).__name__ for a in args]
        pkargs = [str(k) + ' of type ' + type(v).__name__ for k, v in kwargs.items()]
        descr = None
        if '_description' in kwargs:
            descr = kwargs['_description']
            del kwargs['_description']
        prompt = PROMPTER.prompt(name, 'f', comment, pargs, pkargs, description=descr)
        response = chat(prompt)
        if I == 'v':
            print(response)
        elif I == 'i':
            print(response)
            critique = input('Comments (type "y" to accept the code): ')
            while not (critique == 'y'):
                prompt += [('assistant', response), ('user', critique)]
                response = chat(prompt)
                print(response)
                critique = input('Comments (type "y" to accept the code): ')
        exec(response, globals = globals())
        
        tmp_context = ContextObj(name, response, descr)
        context.add_definition(tmp_context)
        return globals()[name](*args, **kwargs)
    return _catchParams
