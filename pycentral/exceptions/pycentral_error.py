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

from typing import Any


class PycentralError(Exception):
    """
    Base class for other PYCENTRAL exceptions.
    """

    base_msg = "PYCENTRAL ERROR"

    def __init__(self, *args):
        self.message = ", ".join(
            (
                self.base_msg,
                *(str(a) for a in args),
            )
        )
        self.response = None

    def __setattr__(self, name: str, value: Any) -> None:
        return super().__setattr__(name, value)

    def __str__(self):
        return repr(self.message)

    def set_response(self, response):
        self.response = response
