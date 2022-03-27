def handle_storage(instance, filename):
    file_extension = filename.split('.')[-1]
    if hasattr(instance, 'name'):
        name_value = instance.name
    else:
        name_value = instance.uuid.hex
    return f'{instance.__class__.__name__}/{name_value}.{file_extension}'
