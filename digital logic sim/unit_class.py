"""
Objective: Make classes representing the logic unites of a computer
Creator: XenonEGG

using: python 3.6
encoding: utf-8
"""


class DigitalUnit:
    def __init__(self, name, value):
        """
        Represent the abstract part of a logic unit
        """
        self.name = name
        self.value = value

    def copy(self):
        return DigitalUnit(self.name, self.value)

    def get_name(self):
        return self.name

    def get_value(self, ask_unit=None) -> str:
        return self.value

    def set_value(self, value: str):
        self.value = value


class PhysicalUnit(DigitalUnit):
    def __init__(self, name: str, value: str, input_pin_count: int, output_pin_count: int):
        """
        Represent the physical part of a logic unit
        """
        super().__init__(name, value)

        self.input_unit_count = input_pin_count
        self.input_unit_list = [DigitalUnit("NONE", -1)] * input_pin_count
        self.output_unit_count = output_pin_count
        self.output_unit_list = []
        for i in range(output_pin_count):
            self.output_unit_list.append([])

    def copy(self):
        return PhysicalUnit(self.name, self.value, self.input_unit_count, self.output_unit_count)

    def get_input_unit_count(self) -> int:
        return self.input_unit_count

    def get_input_unit(self, index: int) -> DigitalUnit:
        return self.input_unit_list[index]

    def get_input_unit_list(self) -> list:
        return self.input_unit_list

    def get_output_pin_count(self) -> int:
        return self.output_unit_count

    def get_output_pin_unit_list(self, index: int) -> list:
        return self.output_unit_list[index]

    def get_all_output_pin_list(self) -> list:
        return self.output_unit_list

    def set_input_unit(self, index: int, unit: DigitalUnit):
        current_unit = self.input_unit_list[index]
        if current_unit.get_name() != "NONE":
            raise Exception(f"{self.get_name()}: You need to disconnect the unit at index {index} "
                            f"before connecting '{unit.get_name()}'")
        self.input_unit_list[index] = unit

    def remove_input_unit(self, index: int):
        self.input_unit_list[index] = DigitalUnit("NONE", "-1")

    def set_input_unit_list(self, unit_list: list):
        for unit in self.input_unit_list:
            if unit.get_name() != "NONE":
                raise Exception(f"{self.get_name()}: You need to disconnect all unit before connecting others")

        if len(unit_list) != self.input_unit_count:
            raise Exception("Le nombre d'unitées dans la liste n'est pas le bon")
        self.input_unit_list = unit_list

    def add_output_unit(self, index: int, unit: DigitalUnit):
        if unit not in self.output_unit_list[index]:
            self.output_unit_list[index].append(unit)
        else:
            raise Exception(f"This unit is already in pin index {index}")

    def pop_output_unit(self, index: int):
        self.output_unit_list[index].pop(index)

    def clear_output_unit(self, index: int):
        self.output_unit_list[index].clear()

    def remove_output_unit(self, index: int, unit: DigitalUnit):
        self.output_unit_list[index].remove(unit)


class Pin(PhysicalUnit):
    def __init__(self, name: str, value: str):
        """
        Represent a pin used by ship to represent their internal inputs and outputs
        """
        super().__init__(name, value, 1, 1)

        self.owner_ship = Ship("NONE", 0, 0)

    def copy(self):
        return Pin(self.name, self.value)

    def get_value(self, ask_unit: PhysicalUnit = None) -> str:
        input_unit = self.get_input_unit(0)
        if input_unit.get_name() == "NONE":
            if self.owner_ship.get_name() == "NONE":
                return self.value
            else:
                self.owner_ship.get_value()
                return self.value
        else:
            value = input_unit.get_value()
            self.set_value(value)
            return value

    def get_owner_ship(self):
        return self.owner_ship

    def set_owner_ship(self, ship):
        self.owner_ship = ship


class Wire(PhysicalUnit):
    def __init__(self, name: str):
        """
        Represent a wire that will be connected to other unit

        When you connect a wire with the connection type "INPUT" the wire is connected to the input pin of a unit
        """
        super().__init__(name, "0", 1, 1)

        self.unit_datas = []

    def copy(self):
        return Wire(self.name)

    def get_connected_unit(self) -> tuple:
        return self.unit_datas[0]["unit"], self.unit_datas[1]["unit"]

    def get_connection_types(self) -> tuple:
        return self.unit_datas[0]["connection_type"], self.unit_datas[1]["connection_type"]

    def get_connection_index(self) -> tuple:
        return self.unit_datas[0]["connection_index"], self.unit_datas[1]["connection_index"]

    def get_value(self, ask_unit: PhysicalUnit = None) -> str:
        unit_a, unit_b = self.get_connected_unit()
        connection_type_a, connection_type_b = self.get_connection_types()
        value = "-1"
        if connection_type_a == "OUTPUT":
            value = unit_a.get_value(self)
        elif connection_type_b == "OUTPUT":
            value = unit_b.get_value(self)

        if value == "-1":
            raise Exception(f"The wire '{self.name}' isn't linked properly, input missing")
        self.set_value(value)
        return value

    def link_wire_to_unites(self, entity_data_a: dict, entity_data_b: dict):
        """
        entity_data: a dict with keys 'entity', 'pin_type', 'pin_index'
        representing the connection type between the wire and the entity

        Example: entity_data = {"entity": nand_ship, "pin_type": "INPUT", "pin_index": 0}

        pin_type can be 'INPUT' or 'OUTPUT'
        """
        entity_a, pin_type_a, pin_index_a = (entity_data_a["unit"], entity_data_a["connection_type"],
                                             entity_data_a["connection_index"])
        entity_b, pin_type_b, pin_index_b = (entity_data_b["unit"], entity_data_b["connection_type"],
                                             entity_data_b["connection_index"])
        allowed_type = ["INPUT", "OUTPUT"]
        assert pin_type_a != pin_type_b, "The wire need to go from an output pin to an input pin"
        assert pin_type_a in allowed_type, "The pin_a need to have a type of: INPUT or OUTPUT"
        assert pin_type_b in allowed_type, "The pin_a need to have a type of: INPUT or OUTPUT"

        allowed_keys = ["unit", "connection_type", "connection_index"]
        for key in entity_data_a.keys():
            assert key in allowed_keys, "The key referred is not allowed"
        for key in entity_data_b.keys():
            assert key in allowed_keys, "The key referred is not allowed"

        self.unit_datas = [entity_data_a, entity_data_b]

        for unit_data in self.unit_datas:
            unit, connection_type, connection_index = (unit_data["unit"], unit_data["connection_type"],
                                                       unit_data["connection_index"])
            if isinstance(unit, PhysicalUnit):
                if connection_type == "INPUT":
                    unit.set_input_unit(connection_index, self)
                    self.add_output_unit(0, unit)
                elif connection_type == "OUTPUT":
                    unit.add_output_unit(connection_index, self)
                    self.set_input_unit(0, unit)
            else:
                raise Exception("The unit isn't a PhysicalUnit")

    def disconnect(self):
        for unit_data in self.unit_datas:
            unit, connection_type, connection_index = (unit_data["unit"], unit_data["connection_type"],
                                                       unit_data["connection_index"])
            if isinstance(unit, PhysicalUnit):
                if connection_type == "INPUT":
                    unit.remove_input_unit(connection_index)
                elif connection_type == "OUTPUT":
                    unit.remove_output_unit(connection_index, self)
            else:
                raise Exception("The unit isn't a physical unit !")
        self.unit_datas = []


class LogicGate(PhysicalUnit):
    def __init__(self, name: str, logic: dict):
        """
        Represent a logic unit used by other ship to proceed logic

        logic: a dictionary where a string represent the input and a string represent the output
        AND gate example -> logic = {'0 0': '0', '1 0': '0', '0 1': '0', '1 1': '1'}
        """

        # logic: dict[str:str]
        self.logic = logic

        self.logic_count = -1
        self.input_unit_count = -1
        self.output_unit_count = -1
        self.verify_input()  # set: input/output pin count, logic count

        super().__init__(name, "0", self.input_unit_count, self.output_unit_count)

    def copy(self):
        return LogicGate(self.name, self.logic)

    def verify_input(self):
        # Input pin count
        first_input_unit_count = -1
        last_logic_input = None
        # Output pin count
        first_output_unit_count = -1
        last_logic_output = None

        for current_logic_input in self.logic.keys():
            input_pin_count = len(current_logic_input.split(" "))
            current_logic_output = self.logic[current_logic_input]
            output_pin_count = len(current_logic_output.split(" "))

            if first_input_unit_count == -1:
                first_input_unit_count = input_pin_count
            elif first_input_unit_count != input_pin_count:
                raise Exception(f"The logic input need to have same amount of input pin for every case:\n"
                                f"{last_logic_input} != {current_logic_input}")

            if first_output_unit_count == -1:
                first_output_unit_count = output_pin_count
            elif first_output_unit_count != output_pin_count:
                raise Exception(f"The logic output need to have same amount of output pin for every case:\n"
                                f"{last_logic_output} != {current_logic_output}")

            last_logic_input = current_logic_input
            last_logic_output = current_logic_output

        self.input_unit_count = first_input_unit_count
        self.output_unit_count = first_output_unit_count

        self.logic_count = 2 ** first_input_unit_count
        if len(self.logic.keys()) != self.logic_count:
            raise Exception(f"A door with {first_input_unit_count} pin need to have a rule composed of "
                            f"{self.logic_count} logic...")

    def get_value(self, ask_unit: PhysicalUnit = None) -> str:
        input_string = ""
        for input_pin in self.input_unit_list:
            if input_pin is None:
                raise Exception(f"Il reste au moins un fil à connecter à la porte logique {self.name}")
            else:
                value = input_pin.get_value()
                input_string += f"{value} "
        input_string = input_string[:-1]

        try:
            output = self.logic[input_string]
        except:
            raise Exception(f"{self.get_name()}: The logic input doesn't match logic dictionary (get:{input_string})")

        self.set_value(output)
        if ask_unit is not None:
            index = -1
            for i in range(self.get_output_pin_count()):
                output_unit_list = self.get_output_pin_unit_list(i)
                if ask_unit in output_unit_list:
                    index = i
            output = output.split(" ")
            return output[index]
        return output

    def get_logic(self):
        return self.logic

    def get_logic_count(self):
        return self.logic_count


class Ship(PhysicalUnit):
    def __init__(self, name, input_unit_count: int, output_unit_count: int):
        """
        Represent a more complex unit composed of other unit

        The list output_unit_list can contain only a number of list of one pin equal to output_unit_count
        """
        super().__init__(name, "0", input_unit_count, output_unit_count)

        self.has_updated_unite_values = False

        # Unités internes au ship
        self.internal_input_unit_list = []
        self.internal_output_unit_list = []

        # Création des pins d'interface, et stockage comme pin input et output, ces pins ne doivent jamais être modifiés
        # car ils permettent de créer les liens nécéssaires au fonctionnement du ship avec d'autres unitées branchées
        # à lui
        for i in range(input_unit_count):
            new_pin = Pin(f"input_pin_{i}", "-1")
            new_pin.set_owner_ship(self)
            self.input_unit_list[i] = new_pin
        for i in range(output_unit_count):
            new_pin = Pin(f"output_pin_{i}", "-1")
            new_pin.set_owner_ship(self)
            current_list = self.output_unit_list[i]
            current_list.append(new_pin)

    def copy(self):
        # Internal entity list: Pin, Wire, LogicalGate
        internal_unit_list = self.get_every_unit()
        # Création de la liste contenant la copie de chaque entitée
        internal_unit_list_copy = []

        # Internal ship list
        internal_ship_list = []
        # Création de la liste contenant les ship internes à celui-ci
        internal_ship_list_copy = []

        # Création de la liste contenant les pins reliés a un ship déjà vue
        internal_pin_owned_by_ship_list = []

        # Création de la liste contenant les liens entre les entitées
        internal_link_list = []
        for i in range(len(internal_unit_list)):
            unit = internal_unit_list[i]
            assert isinstance(unit, PhysicalUnit), "The unit need to be a physical unit !"

            internal_unit_list_copy.append(unit.copy())

            # Récupération des informations des fils et rangement dans link_list
            if isinstance(unit, Wire):
                unit_a, unit_b = unit.get_connected_unit()
                connection_type_a, connection_type_b = unit.get_connection_types()
                connection_index_a, connection_index_b = unit.get_connection_index()
                unit_a_position = find_index_in_list(internal_unit_list, unit_a)
                unit_b_position = find_index_in_list(internal_unit_list, unit_b)
                assert unit_a_position != -1, f"The unit ({unit_a.get_name()}) was not found on the list !"
                assert unit_b_position != -1, f"The unit ({unit_b.get_name()}) was not found on the list !"
                wire_data = {
                    "unit_a_position": unit_a_position,
                    "unit_b_position": unit_b_position,
                    "connection_type_a": connection_type_a,
                    "connection_type_b": connection_type_b,
                    "connection_index_a": connection_index_a,
                    "connection_index_b": connection_index_b
                }
                internal_link_list.append(wire_data)

            elif isinstance(unit, Pin):
                # Récupération des informations des pins sur leurs owner_ship
                owner_ship = unit.get_owner_ship()
                if owner_ship.get_name() != "NONE":
                    if unit not in internal_pin_owned_by_ship_list and owner_ship not in internal_ship_list:
                        linked_pins = owner_ship.get_input_unit_list() + owner_ship.get_all_output_pin_list()
                        internal_ship_list.append(owner_ship)
                        internal_ship_list_copy.append(owner_ship.copy())
                        internal_pin_owned_by_ship_list += linked_pins
                internal_link_list.append(None)

            else:
                internal_link_list.append(None)

        # Branchement des fils aux portes logiques et aux pins
        for i in range(len(internal_unit_list_copy)):
            current_unit = internal_unit_list_copy[i]

            if isinstance(current_unit, Wire):
                wire_data = internal_link_list[i]
                unit_a, unit_b = (internal_unit_list_copy[wire_data["unit_a_position"]],
                                  internal_unit_list_copy[wire_data["unit_b_position"]])
                connection_type_a, connection_type_b = wire_data["connection_type_a"], wire_data["connection_type_b"]
                connection_index_a, connection_index_b = wire_data["connection_index_a"], wire_data["connection_index_b"]

                unit_data_a = {
                    "unit": unit_a,
                    "connection_type": connection_type_a,
                    "connection_index": connection_index_a
                }
                unit_data_b = {
                    "unit": unit_b,
                    "connection_type": connection_type_b,
                    "connection_index": connection_index_b
                }
                current_unit.link_wire_to_unites(unit_data_a, unit_data_b)

            # Liaison des ship a leurs pins
            for ship_index in range(len(internal_ship_list)):
                internal_ship = internal_ship_list[ship_index]
                internal_ship_copy = internal_ship_list_copy[ship_index]
                ship_input_pins = internal_ship.get_input_unit_list()
                ship_output_pins = internal_ship.get_all_output_pin_list()

                ship_input_pins_copy = []
                ship_output_pins_copy = []
                for pin in ship_input_pins:
                    pin_index = find_index_in_list(internal_unit_list, pin)
                    pin_copy = internal_unit_list_copy[pin_index]
                    if isinstance(pin_copy, Pin):
                        pin_copy.set_owner_ship(internal_ship_copy)
                    else:
                        raise Exception("The unit isn't a pin !")
                    ship_input_pins_copy.append(pin_copy)

                for pin in ship_output_pins:
                    pin_index = find_index_in_list(internal_unit_list, pin)
                    pin_copy = internal_unit_list_copy[pin_index]
                    if isinstance(pin_copy, Pin):
                        pin_copy.set_owner_ship(internal_ship_copy)
                    else:
                        raise Exception("The unit isn't a pin !")
                    ship_output_pins_copy.append(pin_copy)

                if isinstance(internal_ship_copy, Ship):
                    internal_ship_copy.make_internal_logic(ship_input_pins_copy, ship_output_pins_copy)
                else:
                    raise Exception("The unit isn't a ship !")

        # Création du nouveau ship
        new_ship = Ship(self.name, self.input_unit_count, self.output_unit_count)

        internal_input_pin_list_copy = []
        internal_output_pin_list_copy = []
        for pin in self.internal_input_unit_list:
            pin_index = find_index_in_list(internal_unit_list, pin)
            internal_input_pin_list_copy.append(internal_unit_list_copy[pin_index])
        for pin in self.internal_output_unit_list:
            pin_index = find_index_in_list(internal_unit_list, pin)
            internal_output_pin_list_copy.append(internal_unit_list_copy[pin_index])

        new_ship.make_internal_logic(internal_input_pin_list_copy, internal_output_pin_list_copy)
        return new_ship

    def get_every_unit(self):
        internal_unit_list = []
        for pin in self.internal_output_unit_list:
            if isinstance(pin, PhysicalUnit):
                store_every_unit(internal_unit_list, pin)
                internal_unit_list.append(pin)
            else:
                raise Exception(f"The unit ({pin.get_name()}) isn't a pin !")
        return internal_unit_list

    def get_logic_unit(self):
        devices = self.get_every_unit()

        i = 0
        while i < len(devices):
            entity = devices[i]
            if isinstance(entity, Wire) or isinstance(entity, Pin):
                devices.pop(i)
                i -= 1
            i += 1
        return devices

    def get_wires(self):
        devices = self.get_every_unit()

        i = 0
        while i < len(devices):
            entity = devices[i]
            if not isinstance(entity, Wire):
                devices.pop(i)
                i -= 1
            i += 1
        return devices

    def get_connections(self) -> str:
        wires = self.get_wires()
        result = ""
        for wire in wires:
            assert isinstance(wire, Wire), "The unit isn't a wire !"
            unit_a, unit_b = wire.get_connected_unit()
            connection_type_a, connection_type_b = wire.get_connection_types()
            if connection_type_a == "INPUT":
                result += f"{unit_b.get_name()} connected to {unit_a.get_name()}\n"
            if connection_type_b == "INPUT":
                result += f"{unit_a.get_name()} connected to {unit_b.get_name()}\n"
        return result[:-1]

    def get_value(self, ask_unit: PhysicalUnit = None):
        for i in range(self.input_unit_count):
            input_pin = self.get_input_unit(i)
            value = input_pin.get_value()
            internal_input_pin = self.internal_input_unit_list[i]
            internal_input_pin.set_value(value)

        output = ""
        for i in range(self.output_unit_count):
            internal_output_pin = self.internal_output_unit_list[i]
            value = internal_output_pin.get_value()
            interface_output_pin = self.get_output_pin_unit_list(i)[0]
            interface_output_pin.set_value(value)
            output += f"{value} "
        output = output[:-1]

        if ask_unit is not None:
            index = -1
            for i in range(self.get_output_pin_count()):
                output_pin = self.get_output_pin_unit_list(i)[0]
                assert isinstance(output_pin, Pin), "This unit isn't a pin !"
                output_pin_output_list = output_pin.get_output_pin_unit_list(0)
                if ask_unit in output_pin_output_list:
                    index = i
            output = output.split(" ")
            return output[index]
        return output

    def get_has_updated_unit_values(self):
        return self.has_updated_unite_values

    def set_has_updated_unit_values(self, state: bool):
        self.has_updated_unite_values = state

    def set_input_unit(self, index: int, unit: DigitalUnit):
        target_pin = self.get_input_unit(index)
        if isinstance(target_pin, Pin):
            target_pin.set_input_unit(0, unit)
        else:
            raise Exception("The target_pin isn't a pin !")

    def add_output_unit(self, index: int, unit: DigitalUnit):
        target_pin = self.get_output_pin_unit_list(index)[0]
        if isinstance(target_pin, Pin):
            target_pin.add_output_unit(0, unit)
        else:
            raise Exception("The target_pin isn't a pin !")

    def remove_input_unit(self, index: int):
        target_pin = self.get_input_unit(index)
        if isinstance(target_pin, Pin):
            target_pin.remove_input_unit(0)
        else:
            raise Exception("The target_pin isn't a pin !")

    def remove_output_unit(self, index: int, unit: PhysicalUnit):
        target_pin = self.get_output_pin_unit_list(index)[0]
        if isinstance(target_pin, Pin):
            target_pin.remove_output_unit(0, unit)
        else:
            raise Exception("The target_pin isn't a pin !")

    def set_input_unit_list(self, unit_list: list):
        for i in range(self.input_unit_count):
            target_pin = self.get_input_unit(i)
            target_unit = unit_list[i]
            if isinstance(target_pin, Pin):
                target_pin.set_input_unit(0, target_unit)
            else:
                raise Exception(f"The target_pin ({i}) isn't a pin !")

    def make_internal_logic(self, internal_input_unit_list: list, internal_output_unit_list: list):
        # Destruction des liens avec l'extérieur pour les pins internes
        for interface_pin in internal_input_unit_list:
            assert isinstance(interface_pin, Pin), "This unit isn't a pin !"
            interface_pin.remove_input_unit(0)
        for interface_pin in internal_output_unit_list:
            assert isinstance(interface_pin, Pin), "This unit isn't a pin !"
            interface_pin.clear_output_unit(0)

        assert len(internal_input_unit_list) == self.get_input_unit_count(), "Wrong wount !"
        assert len(internal_output_unit_list) == self.get_output_pin_count(), "Wrong wount !"

        self.internal_input_unit_list = internal_input_unit_list
        self.internal_output_unit_list = internal_output_unit_list


def store_every_unit(unit_list: list, start_unit: PhysicalUnit):
    new_unit_list = []
    for unit in start_unit.get_input_unit_list():
        if unit.get_name() == "NONE":
            continue
        elif unit not in new_unit_list and unit not in unit_list:
            store_every_unit(unit_list, unit)
            new_unit_list.append(unit)
    unit_list += new_unit_list


def find_index_in_list(unit_list: list, unit: DigitalUnit):
    for i in range(len(unit_list)):
        current_entity = unit_list[i]
        if current_entity == unit:
            return i
    return -1


def connect_wire(unit_a: PhysicalUnit, output_index: int,
                 unit_b: PhysicalUnit, input_index: int) -> Wire:
    wire_data_output = {
        "unit": unit_a, "connection_type": "OUTPUT", "connection_index": output_index
    }
    wire_data_input = {
        "unit": unit_b, "connection_type": "INPUT", "connection_index": input_index
    }
    wire = Wire(f"{unit_a.get_name()}----{unit_b.get_name()}")
    wire.link_wire_to_unites(wire_data_output, wire_data_input)
    return wire


def convert(number: int) -> list:
    res = []
    while number != 0:
        res.insert(0, number % 2)
        number //= 2
    if len(res) == 0:
        res = [0]
    return res


def make_all_bit_combination(element_size: int) -> list:
    result = []
    for i in range(2 ** element_size):
        res = convert(i)
        while len(res) < element_size:
            res.insert(0, 0)
        result.append(res)
    return result


def list_to_str(lst: list) -> str:
    result = ""
    for elt in lst:
        result += f"{elt} "
    return result[:-1]


def convert_ship_to_logic_gate(ship: Ship) -> LogicGate:
    input_count = ship.get_input_unit_count()
    input_unit_list = ship.get_input_unit_list()
    new_pin_list = []

    wire_data = []
    for input_pin in input_unit_list:
        assert isinstance(input_pin, Pin), "The unit isn't a pin !"
        wire = input_pin.get_input_unit(0)
        if isinstance(wire, Wire):
            # Stockage des data concernant les connections
            unit_a, unit_b = wire.get_connected_unit()
            connection_type_a, connection_type_b = wire.get_connection_types()
            connection_index_a, connection_index_b = wire.get_connection_index()
            if connection_type_a == "OUTPUT":
                wire_data.append((unit_a, connection_index_a))
            else:
                wire_data.append((unit_b, connection_index_b))
            # Déconnection des fils
            wire.disconnect()
        else:
            wire_data.append(None)
        # Connection avec les pin de test
        new_pin = Pin(f"pin_{input_pin.get_name()}", "0")
        connect_wire(new_pin, 0, input_pin, 0)
        new_pin_list.append(new_pin)

    # Partie test
    bit_combination_list = make_all_bit_combination(input_count)
    logic_dict = {}
    for bit_combination in bit_combination_list:
        bit_combination_string = list_to_str(bit_combination)
        for i in range(len(bit_combination)):
            new_pin_list[i].set_value(bit_combination[i])
        value = ship.get_value()
        logic_dict[bit_combination_string] = value

    # Reconnection aux unitées d'avant
    for i in range(input_count):
        input_pin = input_unit_list[i]
        assert isinstance(input_pin, Pin), "The unit isn't a pin !"
        wire = input_pin.get_input_unit(0)
        assert isinstance(wire, Wire), "The unit isn't a wire !"
        wire.disconnect()
        if wire_data[i] is not None:
            unit, index = wire_data[i]
            connect_wire(unit, index, input_pin, 0)

    return LogicGate(ship.get_name(), logic_dict)
