"""
Objective: Use algorithm to find the best way to connect logic door
Creator: XenonEGG

using: python 3.6
encoding: utf-8
"""

from unit_class import *
import random


class ConnectionFinder:
    def __init__(self):
        # Logic list
        self.input_logic_list = []
        self.output_logic_list = []

        # Allowed gates data
        self.allowed_unit = []
        self.allowed_unit_counter = []
        self.current_max_unit = 1

    def find_best_connections(self, logic_dictionary: dict, allowed_logic_gates: list):
        # Création des list d'input et d'output
        self.input_logic_list.clear()
        self.output_logic_list.clear()
        keys = logic_dictionary.keys()
        values = logic_dictionary.values()
        for key in keys:
            text = key.split(" ")
            self.input_logic_list.append(text)
        for value in values:
            text = value.split(" ")
            self.output_logic_list.append(text)

        self.allowed_unit = allowed_logic_gates

    def make_a_functional_structure(self):
        # Définition du nombre d'unitées utilisées
        allowed_unit_counter = []
        current_max_unit = self.current_max_unit
        for i in range(len(self.allowed_unit)):
            count = random.randint(0, current_max_unit)
            allowed_unit_counter.append(count)

        # Création des unitées




"""
and_logic = {
    "0 0": "0",
    "1 0": "0",
    "0 1": "0",
    "1 1": "1"
}
not_logic = {
    "0": "1",
    "1": "0"
}

# OR gate
and_gate = LogicGate("AND", and_logic)
not_gate_a = LogicGate("NOT_a", not_logic)
not_gate_b = LogicGate("NOT_b", not_logic)
not_gate_c = LogicGate("NOT_c", not_logic)
pin_in_a = Pin("in_a", "0")
pin_in_b = Pin("in_b", "0")
pin_out_a = Pin("out_a", "0")
pin_out_b = Pin("out_b", "0")

connect_wire(pin_in_a, 0, not_gate_a, 0)
connect_wire(pin_in_b, 0, not_gate_b, 0)
connect_wire(not_gate_a, 0, and_gate, 0)
connect_wire(not_gate_b, 0, and_gate, 1)
connect_wire(and_gate, 0, not_gate_c, 0)
connect_wire(not_gate_c, 0, pin_out_a, 0)

or_gate = Ship("OR", 2, 1)
or_gate.make_internal_logic([pin_in_a, pin_in_b], [pin_out_a])

# NAND gate
and_gate = and_gate.copy()
not_gate_a = not_gate_a.copy()
pin_in_a = pin_in_a.copy()
pin_in_b = pin_in_b.copy()
pin_out_a = pin_out_a.copy()

connect_wire(pin_in_a, 0, and_gate, 0)
connect_wire(pin_in_b, 0, and_gate, 1)
connect_wire(and_gate, 0, not_gate_a, 0)
connect_wire(not_gate_a, 0, pin_out_a, 0)

nand_gate = Ship("NAND", 2, 1)
nand_gate.make_internal_logic([pin_in_a, pin_in_b], [pin_out_a])

pin_in_a = pin_in_a.copy()
pin_in_b = pin_in_b.copy()
pin_out_a = pin_out_a.copy()
pin_out_b = pin_out_b.copy()

connect_wire(pin_in_a, 0, nand_gate, 0)
connect_wire(pin_in_b, 0, nand_gate, 1)
connect_wire(nand_gate, 0, pin_out_a, 0)

connect_wire(pin_in_a, 0, or_gate, 0)
connect_wire(pin_in_b, 0, or_gate, 1)
connect_wire(or_gate, 0, pin_out_b, 0)

mitsubichi = Ship("MITSUBICHI", 2, 2)
mitsubichi.make_internal_logic([pin_in_a, pin_in_b], [pin_out_a, pin_out_b])

pin_in_a = pin_in_a.copy()
pin_in_b = pin_in_b.copy()
pin_out_a = pin_out_a.copy()
pin_out_b = pin_out_b.copy()

connect_wire(pin_in_a, 0, mitsubichi, 0)
connect_wire(pin_in_b, 0, mitsubichi, 1)
connect_wire(mitsubichi, 0, pin_out_a, 0)
connect_wire(mitsubichi, 1, pin_out_b, 0)

connections = mitsubichi.get_connections()
print(connections)

for cbln in make_all_bit_combination(2):
    a, b = cbln
    pin_in_a.set_value(a)
    pin_in_b.set_value(b)
    x = pin_out_a.get_value()
    y = pin_out_b.get_value()
    print(cbln)
    print(x)
    print(y)
"""
test = ConnectionFinder()
logic = {
    "0 0": "0",
    "1 0": "0",
    "0 1": "0",
    "1 1": "1"
}
test.find_best_connections(logic)
