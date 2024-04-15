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


def get_free_to_connect_unit(unit_list: list) -> list:
    free_to_connect_list = []
    for unit in unit_list:
        assert isinstance(unit, PhysicalUnit), "This unit isn't a PhysicalUnit !"
        if len(unit.get_free_input_index()) > 0:
            free_to_connect_list.append(unit)
    return free_to_connect_list


def take_unit_name(unit_list: list):
    return [e.get_name() for e in unit_list]


class Mutate:
    def __init__(self):
        self.mutate_count = 0

    def get_mutate_count(self) -> int:
        return self.mutate_count

    def set_mutate_value(self, value: int):
        self.mutate_count = value

    def increment_mutate_count(self):
        self.mutate_count += 1

    def mutate_structure(self, input_pin_list: list, output_pin_list: list, all_unit_list: list,
                         allowed_logic_unit_creation: list, unit_creation_luck: float, unit_destruction_luck: float,
                         wire_creation_luck: float, wire_destruction_luck: float,
                         make_wire_from_input_pin_luck: float, make_wire_from_output_pin_luck: float) -> tuple:
        """
        Take a list of unit and process some 'mutation' that represent the creation of a unit/wire or the destruction of
        unit/wire
        """
        new_logic_unit_list = []
        new_wire_list = []
        for unit in all_unit_list:
            if isinstance(unit, Wire):
                new_wire_list.append(unit)
            elif not isinstance(unit, Pin):
                new_logic_unit_list.append(unit)

        # Création d'unitée et destruction d'unitée ne s'excluent pas mutuellement
        mutate_creation_unit = random.random()
        mutate_destruction_unit = random.random()
        if mutate_creation_unit < unit_creation_luck:
            # Créer une unitée
            unit_index = random.randint(0, len(allowed_logic_unit_creation) - 1)
            unit_prefab = allowed_logic_unit_creation[unit_index]
            assert isinstance(unit_prefab, PhysicalUnit), "This unit isn't a PHysicalUnit !"
            unit = unit_prefab.copy()
            assert isinstance(unit, PhysicalUnit), "This unit isn't a PhysicalUnit !"
            unit.set_name(f"{unit_prefab.get_name()}_{self.mutate_count}")
            self.increment_mutate_count()

            new_logic_unit_list.append(unit)
        if len(new_logic_unit_list) > 0 and mutate_destruction_unit < unit_destruction_luck:
            # Destruction d'une unitée
            unit_index = random.randint(0, len(new_logic_unit_list) - 1)
            unit = new_logic_unit_list.pop(unit_index)
            assert isinstance(unit, PhysicalUnit), "This unit isn't a PhysicalUnit !"

            disconnected_wire_list = unit.disconnect()
            for wire in disconnected_wire_list:
                new_wire_list.remove(wire)

        # Wire creation et wire destruction ne s'excluent pas mutuellement
        mutate_create_wire = random.random()
        mutate_destroy_wire = random.random()
        if mutate_create_wire < wire_creation_luck:
            # Wire creation

            """
            Revoir la logique des connections de fils
            """
            if len(new_logic_unit_list) == 0:
                mutate_from_input_pin = 1
                mutate_from_output_pin = 1
            else:
                mutate_from_input_pin = random.random()
                mutate_from_output_pin = random.random()

            if mutate_from_input_pin <= make_wire_from_input_pin_luck and mutate_from_output_pin <= make_wire_from_output_pin_luck:
                # Connect an input to an output
                output_pin_free_to_connect_list = get_free_to_connect_unit(output_pin_list)

                if len(output_pin_free_to_connect_list) > 0:
                    input_index = random.randint(0, len(input_pin_list) - 1)
                    input_pin = input_pin_list[input_index]

                    output_index = random.randint(0, len(output_pin_free_to_connect_list) - 1)
                    output_pin = output_pin_free_to_connect_list[output_index]

                    wire = connect_wire(input_pin, 0, output_pin, 0)
                    new_wire_list.append(wire)

            elif len(new_logic_unit_list) > 0 and mutate_from_input_pin <= make_wire_from_input_pin_luck:
                # Connect an input and a logic unit
                logical_unit_free_to_connect_list = get_free_to_connect_unit(new_logic_unit_list)

                if len(logical_unit_free_to_connect_list) > 0:
                    input_index = random.randint(0, len(input_pin_list) - 1)
                    input_pin = input_pin_list[input_index]

                    logic_unit_index = random.randint(0, len(logical_unit_free_to_connect_list) - 1)
                    logic_unit = logical_unit_free_to_connect_list[logic_unit_index]
                    assert isinstance(logic_unit, PhysicalUnit), "This unit isn't a PhysicalUnit !"
                    free_index_list = logic_unit.get_free_input_index()
                    connection_index = random.choice(free_index_list)

                    wire = connect_wire(input_pin, 0, logic_unit, connection_index)
                    new_wire_list.append(wire)

            elif len(new_logic_unit_list) > 0 and mutate_from_output_pin <= make_wire_from_output_pin_luck:
                # Connect a logical unit and an output
                output_pin_free_to_connect_list = get_free_to_connect_unit(output_pin_list)

                if len(output_pin_free_to_connect_list) > 0:
                    # Connect the output pin to a logic unit
                    logic_unit_index = random.randint(0, len(new_logic_unit_list) - 1)
                    logic_unit = new_logic_unit_list[logic_unit_index]
                    assert isinstance(logic_unit, PhysicalUnit), "This unit isn't a PhysicalUnit !"
                    connection_index = random.randint(0, logic_unit.get_output_unit_list_count() - 1)

                    output_pin_index = random.randint(0, len(output_pin_free_to_connect_list) - 1)
                    output_pin = output_pin_free_to_connect_list[output_pin_index]

                    wire = connect_wire(logic_unit, connection_index, output_pin, 0)
                    new_wire_list.append(wire)

            else:
                # Connect two logic unit
                logic_unit_free_to_connect_list = get_free_to_connect_unit(new_logic_unit_list)

                if len(logic_unit_free_to_connect_list) > 1:
                    has_found = False
                    while has_found is False:
                        input_logic_unit_index = random.randint(0, len(logic_unit_free_to_connect_list) - 1)
                        input_logic_unit = logic_unit_free_to_connect_list[input_logic_unit_index]
                        assert isinstance(input_logic_unit, PhysicalUnit), "This unit isn't a PhysicalUnit !"
                        input_connection_index = random.choice(input_logic_unit.get_free_input_index())

                        output_logic_unit = input_logic_unit
                        while output_logic_unit == input_logic_unit:
                            output_logic_unit_index = random.randint(0, len(new_logic_unit_list) - 1)
                            output_logic_unit = new_logic_unit_list[output_logic_unit_index]

                        assert isinstance(output_logic_unit, PhysicalUnit), "This unit isn't a PhysicalUnit !"
                        output_connection_index = random.randint(0, output_logic_unit.get_output_unit_list_count() - 1)

                        try:
                            wire = connect_wire(output_logic_unit, output_connection_index,
                                                input_logic_unit, input_connection_index)
                        except UpdateLoopError as err:
                            print(err.get_message())
                            continue
                        except Exception as exc:
                            raise exc

                        if output_logic_unit not in output_logic_unit.get_all_connected_unit():
                            new_wire_list.append(wire)
                            has_found = True
                        else:
                            wire.disconnect()

        if len(new_wire_list) > 0 and mutate_destroy_wire < wire_destruction_luck:
            # Wire destruction
            wire_index = random.randint(0, len(new_wire_list) - 1)
            wire = new_wire_list[wire_index]
            wire.disconnect()
            new_wire_list.remove(wire)

        return input_pin_list, output_pin_list, input_pin_list + output_pin_list + new_logic_unit_list + new_wire_list


def make_functional_circuit(input_pin_count: int, output_pin_count: int, allowed_unit_data: dict) -> tuple:
    """
    allowed_unit_data: a dictionary of logic gate and the number of these logic gate

    example:
    allowed_unit_data = {and_gate: 5, not_gate: 2, or_gate: 1}
    """
    # Création des pins d'entrée et de sortie
    input_pin_list = []
    output_pin_list = []
    for i in range(input_pin_count):
        new_pin = Pin(f"pin_in_{i}")
        input_pin_list.append(new_pin)
    for i in range(output_pin_count):
        new_pin = Pin(f"pin_out_{i}")
        output_pin_list.append(new_pin)

    # Création des unitées
    unit_list = []
    for unit in allowed_unit_data.keys():
        assert isinstance(unit, PhysicalUnit), "The unit isn't a PhysicalUnit !"
        for j in range(allowed_unit_data[unit]):
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

        # Tant que l'unitée peut être connectée en entrée
        while len(unit.get_free_input_index()) > 0:

            has_found = False  # A trouvé une unitée où se connecter pour ne pas faire de boucle
            while not has_found:

                target = unit
                while unit == target:
                    index = random.randint(0, len(possible_unit_list) - 1)
                    target = possible_unit_list[index]
                assert isinstance(target, PhysicalUnit), "This unit isn't a PhysicalUnit !"

                # Connect the unit and the target
                free_unit_index = unit.get_free_input_index()
                random.shuffle(free_unit_index)
                connection_index = random.randint(0, target.get_output_unit_list_count() - 1)

                try:
                    # Can throw a recursion depth error if the wire make a loop

                    # There will be an error immediately after connection if the unit connected to
                    # update his value according to the wire and this one update his value according to
                    # the unit
                    connect_wire(target, connection_index, unit, free_unit_index[0])
                except UpdateLoopError as err:
                    print(err.args)
                except Exception as exc:
                    raise exc
                if unit in unit.get_all_connected_unit():
                    disconnect_wire(unit, target)
                else:
                    has_found = True

    return input_pin_list, output_pin_list


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

"""
all_combination = make_all_bit_combination(2)
allowed_unit_data = {nand_gate: 3}
result = []
target = ["1", "0", "0", "1"]
i = 0
while result != target:
    i += 1
    if i % 1000 == 0:
        print(f"Essai: {i}")
    try:
        # print("////////////")
        result = []
        input_pin, output_pin = make_functional_circuit(2, 1, allowed_unit_data)
        in_a, in_b = input_pin
        assert isinstance(in_a, Pin), "!"
        assert isinstance(in_b, Pin), "!"
        out = output_pin[0]
        mitsu = Ship("mistu", 2, 1)
        mitsu.make_internal_logic(input_pin, output_pin)
        for cbln in all_combination:
            a, b = cbln
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
        print(exc)
"""

pin_in_a = Pin("in_a")
pin_in_b = Pin("in_b")
pin_out = Pin("out")

input_pin_list_ = [pin_in_a, pin_in_b]
output_pin_list_ = [pin_out]
all_unit_list_ = input_pin_list_ + output_pin_list_

mutate = Mutate()

for i in range(100):
    data = mutate.mutate_structure(input_pin_list_, output_pin_list_, all_unit_list_, [nand_gate],
                                   0.09, 0.05, 0.9, 0.1,
                                   0.2, 0.3)

    input_pin_list_, output_pin_list_, all_unit_list_ = data
    print("/////////////////////////////////////////")
    print([e.get_name() for e in input_pin_list_])
    print([e.get_name() for e in output_pin_list_])
    print([e.get_name() for e in all_unit_list_])
    print()
