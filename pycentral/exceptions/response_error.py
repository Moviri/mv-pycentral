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

from .pycentral_error import PycentralError


class ResponseError(PycentralError):
    """
    Exception class for a PYCENTRAL Response Error.
    """

    base_msg = "RESPONSE ERROR"

    def __init__(self, *args):
        self.message = None
        self.response = None
        if args:
            self.response = args[0]
            if len(args) > 1:
                self.message = ", ".join(str(a) for a in args[1:])
        else:
            self.message = None

    def __str__(self):
        msg_parts = [self.base_msg]
        if self.message:
            msg_parts.append(str(self.message))
        if self.response:
            msg_parts.append("Response")
            msg_parts.append(str(self.response))
        msg = ": ".join(msg_parts)
        return repr(msg)
