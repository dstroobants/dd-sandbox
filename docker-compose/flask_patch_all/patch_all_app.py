#!/usr/bin/env python3
"""
Minimal reproduction of the psycopg.AsyncCursor issubclass TypeError bug

This is the exact reproduction code from the bug report:
https://github.com/DataDog/dd-trace-py/issues/...

Bug: issubclass() TypeError with psycopg.AsyncCursor after ddtrace.patch_all()
"""
import abc
import traceback
from ddtrace import patch_all

# Apply patch_all() first
print("Applying ddtrace.patch_all()...")
patch_all()

# Import psycopg after patching
print("Importing psycopg...")
import psycopg

# Define ABC class
class SomeClass(abc.ABC):
    @abc.abstractmethod
    def some_method(self):
        pass

# Check what type AsyncCursor is after patching
print(f"psycopg.AsyncCursor type: {type(psycopg.AsyncCursor)}")
print(f"psycopg.AsyncCursor repr: {repr(psycopg.AsyncCursor)}")
print(f"psycopg.AsyncCursor __class__: {psycopg.AsyncCursor.__class__}")
print(f"psycopg.AsyncCursor __module__: {getattr(psycopg.AsyncCursor, '__module__', 'N/A')}")
print(f"Is wrapt wrapper: {'wrapt' in str(type(psycopg.AsyncCursor))}")
print(f"Has __wrapped__: {hasattr(psycopg.AsyncCursor, '__wrapped__')}")
if hasattr(psycopg.AsyncCursor, '__wrapped__'):
    print(f"Original class: {psycopg.AsyncCursor.__wrapped__}")
    print(f"Original class type: {type(psycopg.AsyncCursor.__wrapped__)}")

# This should trigger the TypeError
print("Attempting issubclass(psycopg.AsyncCursor, SomeClass)...")
try:
    result = issubclass(psycopg.AsyncCursor, SomeClass)
    print(f"SUCCESS: issubclass returned {result}")
    print("Bug NOT reproduced - this might indicate the issue has been fixed")
except TypeError as e:
    print(f"BUG REPRODUCED: {e}")
    print("This is the expected error from the bug report")
    print("\nFull stack trace:")
    traceback.print_exc()
except Exception as e:
    print(f"UNEXPECTED ERROR: {e}")
    print("\nFull stack trace:")
    traceback.print_exc()
