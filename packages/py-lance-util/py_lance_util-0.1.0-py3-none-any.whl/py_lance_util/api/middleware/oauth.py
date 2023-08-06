from fastapi import Header


def token_is_true(authorization=Header(None)):
    return True
   


