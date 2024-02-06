#coding:utf-8
import maya.cmds as cmds
from functools import wraps
import functools

#undoをまとめるデコレータ
'''
def undo_chunk(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        cmds.undoInfo(openChunk=True)
        try:
            result = func(*args, **kwargs)
        finally:
            cmds.undoInfo(closeChunk=True)
        return result
    return wrapper
'''

def undo_chunk(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        cmds.undoInfo(openChunk=True)
        try:
            result = func(*args, **kwargs)
        finally:
            cmds.undoInfo(closeChunk=True)
        return result
    return wrapper

def apply_decorator_to_all_functions(module, decorator):
    for name, obj in vars(module).items():
        if callable(obj) and not name.startswith('_'):
            setattr(module, name, decorator(obj))
