"""
Objective: Use algorithm to find the best way to connect logic door
Creator: XenonEGG

using: python 3.6
encoding: utf-8

In this script:
uml = unit_make_luck
ukl = unit_kill_luck
wml = wire_make_luck
wkl = wire_kill_luck
wfi = wire_from_input_luck
wfo = wire_from_output_luck
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


class Mutate:
    def __init__(self, allowed_unit_list: list,
                 max_add_unit_count: float,
                 max_add_wire_count: float,
                 uml: float, ukl: float,
                 wml: float, wkl: float,
                 wfi: float, wfo: float):
        self.uml = uml
        self.ukl = ukl
        self.wml = wml
        self.wkl = wkl
        self.wfi = wfi
        self.wfo = wfo

        # Allow to control the maximum of unit and wire created for every ship
        self.max_add_unit_count = max_add_unit_count
        self.max_add_wire_count = max_add_wire_count

        # A list of logic unit (LogicGate or Ship)
        self.allowed_unit_list = allowed_unit_list

        # A counter that count the number of modification done (remove and add)
        self.mutation_count = 0

    def get_mutation_count(self) -> int:
        return self.mutation_count

    def set_mutation_count(self, value: int):
        self.mutation_count = value

    def increment_mutation_count(self):
        self.mutation_count += 1

    def add_logic_unit(self, unit_list: list, allowed_logic_unit_list: list, add_count: int):
        for unit in allowed_logic_unit_list:
            if isinstance(unit, Ship) or isinstance(unit, LogicGate):
                continue
            else:
                raise Exception(f"The unit {unit.get_name()} isn't a logic unit !")

        allowed_list_size = len(allowed_logic_unit_list)
        for i in range(add_count):
            new_unit_index = random.randint(0, allowed_list_size - 1)
            unit_prefab = allowed_logic_unit_list[new_unit_index]
            new_unit = unit_prefab.copy()
            new_unit.set_name(f"{unit_prefab.get_name()}_{self.mutation_count}")

            unit_list.append(new_unit)
            self.increment_mutation_count()

    def remove_unit(self, unit_list: list, wire_list: list, remove_count: int):
        for i in range(remove_count):
            if len(unit_list) > 0:
                unit_index = random.randint(0, len(unit_list) - 1)
                removed_unit = unit_list.pop(unit_index)
                self.increment_mutation_count()

                assert isinstance(removed_unit, PhysicalUnit), "This unit isn't a PhysicalUnit !"
                disconnected_wire_list = removed_unit.disconnect()
                for wire in disconnected_wire_list:
                    wire_list.remove(wire)
                    self.increment_mutation_count()

    def add_wire(self, input_pin_list: list, output_pin_list: list,
                 logic_unit_list: list, wire_list: list,
                 in_to_out_count: int, in_to_logic_count: int, logic_to_out_count: int, logic_to_logic_count: int):

        for i in range(in_to_out_count):
            # Connect an input to an output
            out_free_list = get_free_to_connect_unit(output_pin_list)

            if len(out_free_list) > 0:
                input_index = random.randint(0, len(input_pin_list) - 1)
                input_pin = input_pin_list[input_index]

                output_index = random.randint(0, len(out_free_list) - 1)
                output_pin = out_free_list[output_index]

                wire = connect_wire(input_pin, 0, output_pin, 0)
                wire_list.append(wire)
                self.increment_mutation_count()

        if len(logic_unit_list) > 0:
            for i in range(in_to_logic_count):
                # Connect an input and a logic unit
                logic_free_list = get_free_to_connect_unit(logic_unit_list)

                if len(logic_free_list) > 0:
                    input_index = random.randint(0, len(input_pin_list) - 1)
                    input_pin = input_pin_list[input_index]

                    logic_unit_index = random.randint(0, len(logic_free_list) - 1)
                    logic_unit = logic_free_list[logic_unit_index]
                    assert isinstance(logic_unit, PhysicalUnit), "This unit isn't a PhysicalUnit !"
                    free_index_list = logic_unit.get_free_input_index()
                    connection_index = random.choice(free_index_list)

                    wire = connect_wire(input_pin, 0, logic_unit, connection_index)
                    wire_list.append(wire)
                    self.increment_mutation_count()

        if len(logic_unit_list) > 0:
            for i in range(logic_to_out_count):
                # Connect a logical unit and an output
                out_free_list = get_free_to_connect_unit(output_pin_list)

                if len(out_free_list) > 0:
                    # Connect the output pin to a logic unit
                    logic_unit_index = random.randint(0, len(logic_unit_list) - 1)
                    logic_unit = logic_unit_list[logic_unit_index]
                    assert isinstance(logic_unit, PhysicalUnit), "This unit isn't a PhysicalUnit !"
                    connection_index = random.randint(0, logic_unit.get_output_unit_list_count() - 1)

                    output_pin_index = random.randint(0, len(out_free_list) - 1)
                    output_pin = out_free_list[output_pin_index]

                    wire = connect_wire(logic_unit, connection_index, output_pin, 0)
                    wire_list.append(wire)
                    self.increment_mutation_count()

        if len(logic_unit_list) > 1:
            for i in range(logic_to_logic_count):
                # Connect two logic unit
                logic_free_list = get_free_to_connect_unit(logic_unit_list)

                if len(logic_free_list) > 0:
                    has_found = False
                    try_count = 0
                    while has_found is False:
                        if try_count > len(logic_unit_list) * 2:
                            has_found = True
                            continue
                        try_count += 1

                        input_logic_unit_index = random.randint(0, len(logic_free_list) - 1)
                        input_logic_unit = logic_free_list[input_logic_unit_index]
                        assert isinstance(input_logic_unit, PhysicalUnit), "This unit isn't a PhysicalUnit !"
                        input_connection_index = random.choice(input_logic_unit.get_free_input_index())

                        output_logic_unit = input_logic_unit
                        while output_logic_unit == input_logic_unit:
                            output_logic_unit_index = random.randint(0, len(logic_unit_list) - 1)
                            output_logic_unit = logic_unit_list[output_logic_unit_index]

                        assert isinstance(output_logic_unit, PhysicalUnit), "This unit isn't a PhysicalUnit !"
                        output_connection_index = random.randint(0, output_logic_unit.get_output_unit_list_count() - 1)

                        try:
                            wire = connect_wire(output_logic_unit, output_connection_index,
                                                input_logic_unit, input_connection_index)
                        except RecursionError as err:
                            print(err.args)
                            continue
                        except Exception as exc:
                            raise exc

                        if output_logic_unit not in output_logic_unit.get_all_connected_unit():
                            wire_list.append(wire)
                            self.increment_mutation_count()
                            has_found = True
                        else:
                            wire.disconnect()

    def remove_wire(self, wire_list: list, remove_count: int):
        for i in range(remove_count):
            if len(wire_list) > 0:
                wire_index = random.randint(0, len(wire_list) - 1)
                wire = wire_list[wire_index]
                wire.disconnect()
                wire_list.remove(wire)
                self.increment_mutation_count()

    def mutate_structure(self, input_pin_list: list, output_pin_list: list, all_unit_list: list) -> tuple:
        """
        Take a list of unit and process some 'mutation' that represent the creation of a logic unit/wire
        or the destruction of logic unit/wire

        Return a tuple composed of:
        - input_pin_list
        - output_pin_list
        - all_unit_list (including input_pin_list and output_pin_list)
        """

        logic_unit_list = []
        wire_list = []
        for unit in all_unit_list:
            if isinstance(unit, Wire):
                wire_list.append(unit)
            elif not isinstance(unit, Pin):
                logic_unit_list.append(unit)

        # Variables utiles
        logic_unit_count = len(logic_unit_list)
        max_add_unit_count = self.max_add_unit_count
        wire_count = len(wire_list)
        max_add_wire_count = self.max_add_wire_count

        # Définition du nombre d'unitées logiques détruites
        remove_unit_count = 0
        remove_unit_chance = random.random()
        while remove_unit_count < logic_unit_count and remove_unit_chance < self.ukl:
            remove_unit_count += 1
            remove_unit_chance = random.random()
        # Destruction des unitées logiques
        self.remove_unit(logic_unit_list, wire_list, remove_unit_count)

        # Définition du nombre d'unitées logiques ajoutées
        add_unit_count = 0
        add_unit_chance = random.random()
        while add_unit_count < max_add_unit_count and add_unit_chance < self.uml:
            add_unit_count += 1
            add_unit_chance = random.random()
        # Ajout des unitées logiques
        self.add_logic_unit(logic_unit_list, self.allowed_unit_list, add_unit_count)

        # Définition du nombre de fils détruits
        remove_wire_count = 0
        remove_wire_chance = random.random()
        while remove_wire_count < wire_count and remove_wire_chance < self.wkl:
            remove_wire_count += 1
            remove_wire_chance = random.random()
        # Destruction des fils
        self.remove_wire(wire_list, remove_wire_count)

        # Définition du nombre de fils créés
        add_wire_count = 0
        add_wire_chance = random.random()
        while add_wire_count < max_add_wire_count and add_wire_chance < self.wml:
            add_wire_count += 1
            add_wire_chance = random.random()
        # Définition des connexions crées
        in_to_out_count = 0
        in_to_logic_count = 0
        logic_to_out_count = 0
        logic_to_logic_count = 0
        while add_wire_count > 0:
            from_in_chance = random.random()
            from_out_chance = random.random()
            if from_in_chance < self.wfi and from_out_chance < self.wfo:
                in_to_out_count += 1
            elif from_in_chance < self.wfi:
                in_to_logic_count += 1
            elif from_out_chance < self.wfo:
                logic_to_out_count += 1
            else:
                logic_to_logic_count += 1
            add_wire_count -= 1
        # Ajout des fils
        self.add_wire(input_pin_list, output_pin_list, logic_unit_list, wire_list, in_to_out_count,
                      in_to_logic_count, logic_to_out_count, logic_to_logic_count)

        return input_pin_list, output_pin_list, input_pin_list + output_pin_list + logic_unit_list + wire_list

    def mutate_ship(self, target_ship: Ship) -> Ship:
        """
        Take a ship, copy it, process some 'mutation' on the copy and return a mutated ship
        """
        ship_copy = target_ship.copy()

        ship_copy_internal_input_pin = ship_copy.get_internal_input_pin_list()
        ship_copy_internal_output_pin = ship_copy.get_internal_output_pin_list()
        ship_copy_internal_unit = ship_copy.get_every_internal_unit()

        mutated_tuple = self.mutate_structure(ship_copy_internal_input_pin, ship_copy_internal_output_pin,
                                              ship_copy_internal_unit)

        input_pin_list, output_pin_list, all_unit_list = mutated_tuple
        new_ship = Ship(f"{target_ship.get_name()}_{self.get_mutation_count()}",
                        target_ship.get_input_unit_count(), target_ship.get_output_unit_list_count())
        new_ship.make_internal_logic(input_pin_list, output_pin_list)

        return new_ship


class GeneratePopulation(Mutate):
    def __init__(self, allowed_unit_list: list,
                 max_add_unit_count: float,
                 max_add_wire_count: float,
                 uml: float, ukl: float,
                 wml: float, wkl: float,
                 wfi: float, wfo: float):
        super().__init__(allowed_unit_list, max_add_unit_count, max_add_wire_count, uml, ukl, wml, wkl, wfi, wfo)

        self.ship_prefab = None

    def set_ship_prefab(self, new_ship: Ship):
        self.ship_prefab = new_ship

    def generate_population(self, count: int) -> list:
        """
        Return a list of ship with mutation representing the population created from ship_prefab
        """
        assert isinstance(self.ship_prefab, Ship), ("You need te set the unit_prefab "
                                                    "before generate a population from it!")
        new_ship_list = []

        name = self.ship_prefab.get_name()
        for i in range(count):
            new_ship = self.mutate_ship(self.ship_prefab)
            new_ship_list.append(new_ship)
            new_ship.set_name(f"{name}_{i}")

        return new_ship_list


def evaluate(ship: Ship, target_logic: dict):
    """
    given_points:
    Possible keys       -       logic                               ->      params
    clc                 -       x * common_logic_count              ->      (x)
    clsc                -       x * common_logic_shape_count        ->      (x)
    """

    # Points
    points = 0
    clc_pts = 20
    clsc_pts = 40

    # Ship logic
    ship_logic = convert_ship_to_logic_gate(ship).get_logic()
    if ship_logic == target_logic:
        points += 1000

    """
    Evaluation
    """
    keys = list(target_logic.keys())
    for i in range(len(keys)):
        key = keys[i]

        # clc
        target_result = target_logic[key]
        result = ship_logic[key]
        if result == target_result:
            points += clc_pts

        # clsc
        if i < len(keys) - 1:
            key_a = keys[i+1]
            target_result_a, result_a = target_logic[key_a], ship_logic[key_a]
            if (result, result_a) == (target_result, target_result_a):
                points += clsc_pts

    return points


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
                except RecursionError as err:
                    print(err.args)
                except Exception as exc:
                    raise exc
                if unit in unit.get_all_connected_unit():
                    disconnect_wire(unit, target)
                else:
                    has_found = True

    return input_pin_list, output_pin_list


def get_all_unit_name(unit_list: list) -> list:
    name_list = []
    for unit in unit_list:
        name_list.append(unit.get_name())
    return name_list


def get_free_to_connect_unit(unit_list: list) -> list:
    free_to_connect_list = []
    for unit in unit_list:
        assert isinstance(unit, PhysicalUnit), "This unit isn't a PhysicalUnit !"
        if len(unit.get_free_input_index()) > 0:
            free_to_connect_list.append(unit)
    return free_to_connect_list


# Définition du problème:
# Créer un circuit qui fait la même logique qu'un NAND
xor_logic = {
    "0 0": "0",
    "1 0": "1",
    "0 1": "1",
    "1 1": "0"
}
target_logic = xor_logic

# Logiques utilisables:

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

and_gate = LogicGate("AND", and_logic)
not_gate = LogicGate("NOT", not_logic)
nand_gate = LogicGate("NAND", nand_logic)
in_pin_a, in_pin_b, out_pin = Pin("INA"), Pin("INB"), Pin("OUT")

# Création du ship a faire muter
ship_prefab = Ship("ShipPrefab", 2, 1)
ship_prefab.make_internal_logic([in_pin_a, in_pin_b], [out_pin])

# Proposition de valeurs de probabilités
# 0.5, 0.1, 1, 0.5, 0.2, 0.3
pop_gen = GeneratePopulation([nand_gate], 1, 20, 0.5, 0.1, 1, 0.9,
                             0.2, 0.3)

# Processing
generation_count = 100
greater_number = 0
best_ship_list = [ship_prefab]

time = 0
target_logic_number = 1
best_logic = {}
while best_logic != target_logic:
    if time % 3 == 0:
        target_logic_number += 1
    time += 1
    given_points = {
        "clc": 100,
        "clsc": 300,
        "luc": (30, target_logic_number)
    }
    print(target_logic_number)
    children_per_ship = generation_count // len(best_ship_list)

    current_generation = []
    for best_ship in best_ship_list:
        pop_gen.set_ship_prefab(best_ship)
        current_generation += [best_ship] + pop_gen.generate_population(children_per_ship)
    print(current_generation)
    print(get_all_unit_name(current_generation))

    points_dict = {}
    points_list = []
    for ship in current_generation:
        assert isinstance(ship, Ship), "This isn't a ship !"
        print("//////////")
        print(ship.get_name())
        print(ship.get_internal_connections())
        pts = evaluate(ship, target_logic, given_points)
        if pts not in points_list:
            points_dict[pts] = [ship]
            points_list.append(pts)
        else:
            points_dict[pts] += [ship]
        print(pts)

    points_list = sorted(points_list)
    greater_number = points_list[-1]
    best_ship_list = points_dict[greater_number]

    print(get_all_unit_name(best_ship_list))
    best_logic = convert_ship_to_logic_gate(best_ship_list[-1])

print("######################")
best_ship = best_ship_list[-1]
print(best_ship.get_name())
print(best_ship.get_internal_connections())
print(greater_number)
