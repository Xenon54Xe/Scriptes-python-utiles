"""
Objective: Use algorithm to find the best way to connect logic door
Creator: XenonEGG

using: python 3.6
encoding: utf-8
"""

from unit import *
import random


class ConnectionFinder:
    def __init__(self):
        # Logic list
        self.input_logic_list = []
        self.input_pin_count = -1
        self.output_logic_list = []
        self.output_pin_count = -1

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
        self.input_pin_count = len(self.input_logic_list[0])
        self.output_pin_count = len(self.output_logic_list[0])


def make_functional_structure(input_pin_count: int, output_pin_count: int, allowed_unit: list,
                              max_unit_count_per_type: int):
    # Création des pins d'entrée et de sortie
    input_pin_list = []
    output_pin_list = []
    for i in range(input_pin_count):
        new_pin = Pin(f"pin_in_{i}")
        input_pin_list.append(new_pin)
    for i in range(output_pin_count):
        new_pin = Pin(f"pin_out_{i}")
        output_pin_list.append(new_pin)

    # Définition du nombre d'unitées utilisées par type
    unit_counter = []
    for i in range(len(allowed_unit)):
        count = random.randint(0, max_unit_count_per_type)
        unit_counter.append(count)

    # Création des unitées
    unit_list = []
    for i in range(len(allowed_unit)):
        unit = allowed_unit[i]
        assert isinstance(unit, PhysicalUnit), "The unit isn't a PhysicalUnit !"
        for j in range(unit_counter[i]):
            new_unit = unit.copy()
            new_unit.set_name(f"{unit.get_name()}_{j}")
            unit_list.append(new_unit)
    random.shuffle(unit_list)

    """
    Unit linking:
    - pin output connected in their input pin
    - pin input connected in their output pin
    - other unit connected in both pin
    """
    """# Input pin connections
    for input_pin in input_pin_list:
        # Find a free input pin in unit
        possible_unit_list = unit_list + output_pin_list
        target = PhysicalUnit("NONE", 0, 0)
        free_index_list = []
        while len(free_index_list) == 0 and len(possible_unit_list) > 0:
            index = random.randint(0, len(possible_unit_list) - 1)
            target = possible_unit_list.pop(index)
            free_index_list = target.get_free_input_index()
        assert isinstance(target, PhysicalUnit), "This unit isn't a PhysicalUnit"
        # Connect the input pin and the target
        if len(target.get_free_input_index()) > 0:
            random.shuffle(free_index_list)
            connect_wire(input_pin, 0, target, free_index_list[0])"""

    possible_unit_list = unit_list + input_pin_list
    # Output pin connections
    for output_pin in output_pin_list:
        index = random.randint(0, len(possible_unit_list) - 1)
        target = possible_unit_list[index]
        assert isinstance(target, PhysicalUnit), "This unit isn't a PhysicalUnit !"
        # Connect the output pin and the target
        connection_index = random.randint(0, target.get_output_unit_list_count() - 1)
        connect_wire(target, connection_index, output_pin, 0)

    # Unit connections
    for unit in unit_list:
        assert isinstance(unit, PhysicalUnit), "This unit isn't a PhysicalUnit !"
        while len(unit.get_free_input_index()) > 0:
            target = unit
            while target == unit:
                index = random.randint(0, len(possible_unit_list) - 1)
                target = possible_unit_list[index]
            assert isinstance(target, PhysicalUnit), "This unit isn't a PhysicalUnit !"
            # Connect the unit and the target
            free_unit_index = unit.get_free_input_index()
            random.shuffle(free_unit_index)
            connection_index = random.randint(0, target.get_output_unit_list_count() - 1)
            connect_wire(target, connection_index, unit, free_unit_index[0])

    return input_pin_list, output_pin_list


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
nand_logic = {
    "0 0": "1",
    "0 1": "1",
    "1 0": "1",
    "1 1": "0"
}
or_logic = {
    "0 0": "0",
    "0 1": "1",
    "1 0": "1",
    "1 1": "1"
}
and_gate = LogicGate("AND", and_logic)
not_gate = LogicGate("NOT", not_logic)
nand_gate = LogicGate("NAND", nand_logic)
or_gate = LogicGate("OR", or_logic)
result = []
all_combination = make_all_bit_combination(2)
target = ["1", "0", "0", "1"]
i = 0
while result != target:
    i += 1
    if i % 1000 == 0:
        print(f"Essai: {i}")
    try:
        # print("////////////")
        result = []
        input_pin, output_pin = make_functional_structure(2, 1, [nand_gate, or_gate, and_gate, not_gate], 1)
        in_a, in_b = input_pin
        out = output_pin[0]
        mitsu = Ship("mistu", 2, 1)
        mitsu.make_internal_logic(input_pin, output_pin)
        """print([e.get_name() for e in input_pin])
        print([e.get_name() for e in output_pin])
        print(mitsu.get_connections())"""
        for cbln in all_combination:
            a, b = cbln
            assert isinstance(in_a, Pin), "!"
            assert isinstance(in_b, Pin), "!"
            in_a.set_value(str(a))
            in_b.set_value(str(b))
            in_a.update_all_output_unit()
            in_b.update_all_output_unit()
            x = out.get_current_value()
            result.append(x)
        if result == target:
            print(f"Essai: {i}")
            print(mitsu.get_connections())
        # print(result)
    except Exception as exc:
        if exc.args[0] == "TOO LONG":
            print("TOO LONG")
        else:
            raise exc
