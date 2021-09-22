def convert_to_kebab_case(name, join_character='-'):
    """ Transforms incoming name into hyphen-separated lower-cased string."""
    return join_character.join(name.split()).lower()
