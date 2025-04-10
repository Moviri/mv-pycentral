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


class GenericOperationError(PycentralError):
    """
    PYCENTRAL Generic Operation Error Exception.
    """

    base_msg = "GENERIC OPERATION ERROR"

    def __init__(self, *args):
        self.message = None
        self.response_code = None
        self.extra_info = None
        if args:
            self.message = args[0]
            if len(args) >= 2:
                self.response_code = args[1]
            if len(args) > 2:
                self.extra_info = ", ".join(str(a) for a in args[2:])

    def __str__(self):
        msg_parts = [self.base_msg]
        if self.message:
            msg_parts.append(str(self.message))
        if self.response_code:
            msg_parts.append("Code")
            msg_parts.append(str(self.response_code))
        if self.extra_info:
            msg_parts.append("on Module")
            msg_parts.append(str(self.extra_info))
        msg = ": ".join(msg_parts)
        return repr(msg)
