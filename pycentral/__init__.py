# MIT License
#
# Copyright (c) 2025 HPE Aruba Networking
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# n the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from .base import NewCentralBase

# Manually import each module in the legacy Central folder
import importlib
import sys

CLASSIC_MODULES = [
    "audit_logs",
    "base",
    "base_utils",
    "configuration",
    "constants",
    "device_inventory",
    "firmware_management",
    "licensing",
    "monitoring",
    "msp",
    "rapids",
    "refresh_api_token",
    "topology",
    "url_utils",
    "user_management",
    "visualrf",
    "workflows",
]

for module in CLASSIC_MODULES:
    full_module_name = f"pycentral.classic.{module}"
    imported_module = importlib.import_module(full_module_name)

    sys.modules[f"pycentral.{module}"] = imported_module

# Delete importlib and sys to clean up the namespace after their use
del importlib, sys
