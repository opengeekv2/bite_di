from bite_di import container, inject, Contents

contents = Contents()
contents.from_var_dict({
    'a': 'hola'
})
container(contents)
