from fastapi import HTTPException


class CategoryNotFound(HTTPException):
    def __init__(self):
        self.status_code = 404
        self.detail = "Category not found"


class TagNotFound(HTTPException):
    def __init__(self):
        self.status_code = 404
        self.detail = "Tag not found"


class ThreadNotFound(HTTPException):
    def __init__(self):
        self.status_code = 404
        self.detail = "Thread not found"


class ThreadExists(HTTPException):
    def __init__(self):
        self.status_code = 404
        self.detail = "Thread with this title on this category exists"
