import uuid

def is_valid_uuid(id, ignore_none=False):
    if id is None and ignore_none:
        return
    try:
        uuid.UUID(str(id))
    except:
        raise ValueError(f'{id} is not a valid UUID.')
