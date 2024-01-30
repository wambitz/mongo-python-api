#!/usr/bin/env python3

class CRUDStrategy:
    def create(self, data):
        pass

    def read(self, identifier):
        pass

    def update(self, identifier, data):
        pass

    def delete(self, identifier):
        pass


class CRUDContext:
    def __init__(self, strategy: CRUDStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: CRUDStrategy):
        self.strategy = strategy

    def create(self, data):
        return self.strategy.create(data)

    def read(self, identifier):
        return self.strategy.read(identifier)

    def update(self, identifier, data):
        return self.strategy.update(identifier, data)

    def delete(self, identifier):
        return self.strategy.delete(identifier)