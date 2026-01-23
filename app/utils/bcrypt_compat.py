"""
Bcrypt compatibility fix for passlib.

This module MUST be imported before any passlib imports to fix the
AttributeError: module 'bcrypt' has no attribute '__about__'

passlib tries to access bcrypt.__about__.__version__ which doesn't exist in bcrypt 4.x
"""

import bcrypt

# Create fake __about__ module if it doesn't exist
if not hasattr(bcrypt, '__about__'):
    class FakeBcryptAbout:
        __version__ = bcrypt.__version__ if hasattr(bcrypt, '__version__') else '4.0.0'
    
    bcrypt.__about__ = FakeBcryptAbout()
    print(f"✓ Applied bcrypt compatibility patch (version: {bcrypt.__about__.__version__})")
