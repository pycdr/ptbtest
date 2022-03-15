"""
this file contains the main class for generators.
"""

from telegram import Update

class Generator:
    """base class for all generators"""
    def config(self, server):
        """Get and Set :class:`telegram.Update` data"""
        pass

    def to_update(self) -> Update:
        """Convert generator to `telegram.Update` and return"""
        pass
