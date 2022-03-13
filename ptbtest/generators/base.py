"""
this file contains the main class for generators.
"""

from telegram import Update

class Generator:
    """base class for all generators"""
    def config(self, server):
        pass

    def to_update(self) -> Update:
        pass
