#!/usr/bin/env python
# encoding: utf-8

class Unbuffered:
    '''
    Class for unbuffering stdout
    '''
    def __init__(self, stream):
        self.stream = stream
    def write(self, data):
        self.stream.write(data)
        self.stream.flush()
    def __getattr__(self, attr):
        return getattr(self.stream, attr)
