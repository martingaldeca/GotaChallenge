def handle_storage(instance, filename):
    file_extension = filename.split('.')[-1]
    name_value = instance.name if hasattr(instance, 'name') else instance.uuid.hex
    return f'{instance.__class__.__name__}/{name_value}.{file_extension}'
