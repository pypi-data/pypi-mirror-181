VALID_ALGORITHMS = {'HS256', 'ECDSA', 'NONE'}

def check_is_valid_algorithm(name: str):
   if not name in VALID_ALGORITHMS:
    raise ValueError(
        f'Algorithm {name} is not a valid signature or mac algorithm. Valid algorithms are {VALID_ALGORITHMS}.'
    )