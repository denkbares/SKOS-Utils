import uuid


class IDGenerator:
    _instance = None
    _generated_ids = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(IDGenerator, cls).__new__(cls)
            cls._generated_ids = []
        return cls._instance

    def generate_uuid(cls, len=6):
        myid = str(uuid.uuid4())[:len]
        while uuid in cls._generated_ids:
            myid = str(uuid.uuid4())[:len]
        return myid

