"""
Objective: Make classes representing the logic unites of a computer
Creator: XenonEGG

using: python 3.6
encoding: utf-8

Try to avoid as possible the creation of loop with wires because this could make error
"""


class DigitalUnit:
    def __init__(self, name: str):
        """
        Represent the abstract part of a logic unit
        """
        self.name = name
        self.value = "0"

    def copy(self):
        return DigitalUnit(self.name)

    def get_name(self) -> str:
        return self.name

    def get_current_value(self) -> str:
        return self.value

    def set_name(self, new_name: str):
        self.name = new_name

    def set_value(self, new_value: str):
        self.value = new_value

    def update_value(self):
        pass


class PhysicalUnit(DigitalUnit):
    def __init__(self, name: str, input_unit_count: int, output_unit_list_count: int):
        """
        Represent the physical part of a logic unit
        """
        super().__init__(name)

        self.input_unit_count = input_unit_count
        self.input_unit_list = [DigitalUnit("NONE")] * input_unit_count

        self.output_unit_list_count = output_unit_list_count
        self.output_unit_main_list = []
        for i in range(output_unit_list_count):
            self.output_unit_main_list.append([])

    def copy(self):
        return PhysicalUnit(self.name, self.input_unit_count, self.output_unit_list_count)

    def get_input_unit_count(self) -> int:
        return self.input_unit_count

    def get_input_unit(self, index: int) -> DigitalUnit:
        return self.input_unit_list[index]

    def get_input_unit_list(self) -> list:
        return self.input_unit_list

    def get_free_input_index(self) -> list:
        index = []
        for i in range(self.input_unit_count):
            unit = self.input_unit_list[i]
            if unit.get_name() == "NONE":
                index.append(i)
        return index

    def get_output_unit_list_count(self) -> int:
        return self.output_unit_list_count

    def get_output_unit_list(self, output_unit_list_index: int) -> list:
        return self.output_unit_main_list[output_unit_list_index]

    def get_output_unit(self, output_unit_list_index: int, output_unit_index: int) -> DigitalUnit:
        return self.output_unit_main_list[output_unit_list_index][output_unit_index]

    def get_output_unit_main_list(self) -> list:
        return self.output_unit_main_list

    def get_all_output_unit(self) -> list:
        unit_list = []
        for output_unit_list in self.output_unit_main_list:
            for output_unit in output_unit_list:
                unit_list.append(output_unit)
        return unit_list

    def get_all_connected_unit(self) -> list:
        """
        Return all connected unit to this unit,
        without this unit in the list if she is not connected to itself with the help of another unit(s)
        """
        connected_unit = []
        take_every_connected_unit(connected_unit, self, True, True)
        return connected_unit

    def set_value(self, new_value: str):
        super().set_value(new_value)
        self.update_all_output_unit()

    def set_input_unit(self, index: int, new_unit: DigitalUnit):
        current_unit = self.input_unit_list[index]
        if current_unit.get_name() != "NONE":
            raise Exception(f"{self.get_name()}: You need to disconnect the unit at index {index} "
                            f"before connecting '{new_unit.get_name()}'")
        self.input_unit_list[index] = new_unit

    def pop_input_unit(self, index: int):
        self.input_unit_list[index] = DigitalUnit("NONE")

    def clear_input_unit_list(self):
        for i in range(self.input_unit_count):
            self.pop_input_unit(i)

    def add_output_unit(self, output_unit_list_index: int, new_unit: DigitalUnit):
        target_output_unit_list = self.get_output_unit_list(output_unit_list_index)
        if new_unit not in target_output_unit_list:
            target_output_unit_list.append(new_unit)
        else:
            raise Exception(f"This unit is already in output pin index: {output_unit_list_index}")

    def pop_output_unit(self, output_unit_list_index: int, unit_index: int):
        self.output_unit_main_list[output_unit_list_index].pop(unit_index)

    def remove_output_unit(self, output_unit_list_index: int, unit: DigitalUnit):
        self.output_unit_main_list[output_unit_list_index].remove(unit)

    def clear_output_unit_list(self, output_unit_list_index: int):
        self.output_unit_main_list[output_unit_list_index].clear()

    def clear_output_unit_main_list(self):
        for i in range(self.output_unit_list_count):
            self.clear_output_unit_list(i)

    def disconnect(self) -> tuple:
        disconnected_unit_list = []
        for wire in self.get_input_unit_list() + self.get_all_output_unit():
            if isinstance(wire, Wire):
                wire.disconnect()
                disconnected_unit_list.append(wire)
        return tuple(disconnected_unit_list)

    def update_all_output_unit(self):
        for output_unit in self.get_all_output_unit():
            assert isinstance(output_unit, DigitalUnit), "This unit isn't a DigitalUnit !"
            output_unit.update_value()


class Pin(PhysicalUnit):
    def __init__(self, name: str):
        """
        Represent a pin used to set a value in the start of a circuit or gather the result in the end of it
        """
        super().__init__(name, 1, 1)

    def copy(self):
        return Pin(self.name)

    def update_value(self):
        input_unit = self.get_input_unit(0)
        if input_unit.get_name() != "NONE":
            input_value = input_unit.get_current_value()
            if input_value != self.get_current_value():
                self.set_value(input_value)
                self.update_all_output_unit()


class Wire(PhysicalUnit):
    def __init__(self, name: str):
        """
        Represent a wire that will be connected to other unit

        When you connect a wire with the connection type "INPUT" the wire is connected to the input pin of a unit
        """
        super().__init__(name, 1, 1)

        self.unit_datas = []

    def copy(self):
        return Wire(self.name)

    def get_wire_connected_unit(self) -> tuple:
        return self.unit_datas[0]["unit"], self.unit_datas[1]["unit"]

    def get_wire_connection_types(self) -> tuple:
        return self.unit_datas[0]["connection_type"], self.unit_datas[1]["connection_type"]

    def get_wire_connection_index(self) -> tuple:
        return self.unit_datas[0]["connection_index"], self.unit_datas[1]["connection_index"]

    def link_wire_to_unites(self, unit_data_a: dict, unit_data_b: dict):
        """
        unit_data: a dict with keys 'unit', 'connection_type', 'connection_index'
        representing the connection type between the wire and the unit

        Example: unit_data = {"unit": nand_ship, "connection_type": "INPUT", "connection_index": 0}

        pin_type can be 'INPUT' or 'OUTPUT'
        """
        unit_a, connection_type_a, connection_index_a = (unit_data_a["unit"], unit_data_a["connection_type"],
                                                         unit_data_a["connection_index"])
        unit_b, connection_type_b, connection_index_b = (unit_data_b["unit"], unit_data_b["connection_type"],
                                                         unit_data_b["connection_index"])
        allowed_type = ["INPUT", "OUTPUT"]
        assert connection_type_a != connection_type_b, "The wire need to go from an output pin to an input pin"
        assert connection_type_a in allowed_type, "The pin_a need to have a type of: INPUT or OUTPUT"
        assert connection_type_b in allowed_type, "The pin_a need to have a type of: INPUT or OUTPUT"

        allowed_keys = ["unit", "connection_type", "connection_index"]
        for key in unit_data_a.keys():
            assert key in allowed_keys, f"The key referred is not allowed: {key}"
        for key in unit_data_b.keys():
            assert key in allowed_keys, f"The key referred is not allowed: {key}"

        self.unit_datas = [unit_data_a, unit_data_b]

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
                raise Exception("The unit isn't a PhysicalUnit !")

        connected_units = self.get_wire_connected_unit()
        try:
            self.update_value()
            for unit in connected_units:
                assert isinstance(unit, PhysicalUnit), "This unit isn't a PhysicalUnit !"
                unit.update_value()
            self.update_value()
        except RecursionError as err:
            self.disconnect()
            for unit in connected_units:
                assert isinstance(unit, PhysicalUnit), "This unit isn't a PhysicalUnit !"
                unit.update_value()
            raise err
        except Exception as exc:
            raise exc

    def disconnect(self):
        for unit_data in self.unit_datas:
            unit, connection_type, connection_index = (unit_data["unit"], unit_data["connection_type"],
                                                       unit_data["connection_index"])
            if isinstance(unit, PhysicalUnit):
                if connection_type == "INPUT":
                    unit.pop_input_unit(connection_index)
                elif connection_type == "OUTPUT":
                    unit.remove_output_unit(connection_index, self)
            else:
                raise Exception("The unit isn't a PhysicalUnit !")

        for unit in self.get_wire_connected_unit():
            assert isinstance(unit, DigitalUnit), "This unit isn't a DigitalUnit !"
            unit.update_value()

        self.unit_datas = []

    def update_value(self):
        unit_a, unit_b = self.get_wire_connected_unit()
        assert isinstance(unit_a, PhysicalUnit), "This unit isn't a PhysicalUnit !"
        assert isinstance(unit_b, PhysicalUnit), "This unit isn't a PhysicalUnit !"
        connection_type_a, connection_type_b = self.get_wire_connection_types()
        connection_index_a, connection_index_b = self.get_wire_connection_index()

        output_value = "-1"
        if connection_type_a == "OUTPUT":
            brut_value = unit_a.get_current_value()
            brut_value_list = brut_value.split(" ")
            output_value = brut_value_list[connection_index_a]
        elif connection_type_b == "OUTPUT":
            brut_value = unit_b.get_current_value()
            brut_value_list = brut_value.split(" ")
            output_value = brut_value_list[connection_index_b]

        if output_value == "-1":
            raise Exception(f"The wire '{self.name}' isn't linked properly, input missing")

        if output_value != self.get_current_value():
            self.set_value(output_value)
            self.update_all_output_unit()


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

        self.verify_input()  # set: input/output pin count, logic count

        super().__init__(name, self.input_unit_count, self.output_unit_list_count)

        self.update_value()

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
        self.output_unit_list_count = first_output_unit_count

        self.logic_count = 2 ** first_input_unit_count
        if len(self.logic.keys()) != self.logic_count:
            raise Exception(f"A door with {first_input_unit_count} pin need to have a rule composed of "
                            f"{self.logic_count} logic...")

    def get_logic(self) -> dict:
        return self.logic

    def get_logic_count(self) -> int:
        return self.logic_count

    def update_value(self):
        input_string = ""
        for input_unit in self.input_unit_list:
            assert isinstance(input_unit, DigitalUnit), "The referred object isn't a Unit !"
            input_string += f"{input_unit.get_current_value()} "
        input_string = input_string[:-1]

        try:
            output_string = self.logic[input_string]
        except:
            raise Exception(f"{self.get_name()}: The logic input doesn't match logic dictionary (get:{input_string})")

        if output_string != self.get_current_value():
            self.set_value(output_string)
            self.update_all_output_unit()


class Ship(PhysicalUnit):
    def __init__(self, name: str, input_unit_count: int, output_unit_count: int):
        """
        Represent a more complex unit composed of other unit

        The internal unit are only the one connected to the internal input/output of the ship
        """
        super().__init__(name, input_unit_count, output_unit_count)

        # Unités internes au ship
        self.internal_input_pin_list = []
        self.internal_output_pin_list = []

    def copy(self):
        # Internal entity list: Pin, Wire, LogicalGate
        internal_unit_list = self.get_every_internal_unit()
        # Création de la liste contenant la copie de chaque entitée
        internal_unit_list_copy = []

        # Création de la liste contenant les liens entre les entitées
        internal_link_list = []

        # Recherche des liens et copie des unitées
        for i in range(len(internal_unit_list)):
            current_unit = internal_unit_list[i]
            assert isinstance(current_unit, PhysicalUnit), "This unit isn't a PhysicalUnit !"

            internal_unit_list_copy.append(current_unit.copy())

            # Récupération des informations des fils et rangement dans link_list
            if isinstance(current_unit, Wire):
                unit_a, unit_b = current_unit.get_wire_connected_unit()
                connection_type_a, connection_type_b = current_unit.get_wire_connection_types()
                connection_index_a, connection_index_b = current_unit.get_wire_connection_index()

                # Positions utilisées pour retrouver la bonne copie où se brancher
                unit_a_position = find_unit_index_in_list(internal_unit_list, unit_a)
                unit_b_position = find_unit_index_in_list(internal_unit_list, unit_b)

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
            else:
                internal_link_list.append(None)

        # Branchement des fils aux portes logiques et aux pins
        for i in range(len(internal_unit_list_copy)):
            current_unit_copy = internal_unit_list_copy[i]

            if isinstance(current_unit_copy, Wire):
                wire_data = internal_link_list[i]
                assert isinstance(wire_data, dict), "This object isn't a dictionary !"

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
                current_unit_copy.link_wire_to_unites(unit_data_a, unit_data_b)

        # Création du nouveau ship
        new_ship = Ship(self.name, self.input_unit_count, self.output_unit_list_count)

        internal_input_pin_list_copy = []
        internal_output_pin_list_copy = []
        for pin in self.internal_input_pin_list:
            pin_index = find_unit_index_in_list(internal_unit_list, pin)
            assert pin_index != -1, "The pin was not found on the list !"

            pin_copy = internal_unit_list_copy[pin_index]
            assert isinstance(pin_copy, Pin), "This unit isn't a Pin !"

            internal_input_pin_list_copy.append(pin_copy)

        for pin in self.internal_output_pin_list:
            pin_index = find_unit_index_in_list(internal_unit_list, pin)
            assert pin_index != -1, "The pin was not found on the list !"

            pin_copy = internal_unit_list_copy[pin_index]
            assert isinstance(pin_copy, Pin), "This unit isn't a Pin !"

            internal_output_pin_list_copy.append(pin_copy)

        new_ship.make_internal_logic(internal_input_pin_list_copy, internal_output_pin_list_copy)

        return new_ship

    def get_every_internal_unit(self, from_input: bool = True, from_output: bool = True) -> list:
        internal_unit_list = []
        if from_input:
            for internal_input_pin in self.get_internal_input_pin_list():
                if isinstance(internal_input_pin, Pin):
                    internal_unit_list.append(internal_input_pin)
                    take_every_connected_unit(internal_unit_list, internal_input_pin, False, True)
                else:
                    raise Exception(f"The unit ({internal_input_pin.get_name()}) isn't a pin !")

        if from_output:
            for internal_output_pin in self.get_internal_output_pin_list():
                if isinstance(internal_output_pin, Pin):
                    internal_unit_list.append(internal_output_pin)
                    take_every_connected_unit(internal_unit_list, internal_output_pin, True, False)
                else:
                    raise Exception(f"The unit ({internal_output_pin.get_name()}) isn't a pin !")

        return internal_unit_list

    def get_internal_logic_unit(self, from_input: bool = True, from_output: bool = True) -> list:
        logic_unit_list = self.get_every_internal_unit(from_input, from_output)

        i = 0
        while i < len(logic_unit_list):
            unit = logic_unit_list[i]
            if isinstance(unit, Wire) or isinstance(unit, Pin):
                logic_unit_list.pop(i)
                i -= 1
            i += 1
        return logic_unit_list

    def get_internal_wires(self, from_input: bool = True, from_output: bool = True) -> list:
        wire_list = self.get_every_internal_unit(from_input, from_output)

        i = 0
        while i < len(wire_list):
            unit = wire_list[i]
            if not isinstance(unit, Wire):
                wire_list.pop(i)
                i -= 1
            i += 1
        return wire_list

    def get_internal_connections(self) -> str:
        """
        Gives a string representing all the internal unit connected to the internal OUTPUT of the ship
        """

        wires = self.get_internal_wires(False, True)
        wires = reverse_list(wires)

        result = ""
        last_unit = DigitalUnit("NONE")
        for wire in wires:
            unit_a, unit_b = wire.get_wire_connected_unit()
            assert isinstance(unit_a, PhysicalUnit), "This unit isn't a PhysicalUnit !"
            assert isinstance(unit_b, PhysicalUnit), "This unit isn't a PhysicalUnit !"
            co_type_a, co_type_b = wire.get_wire_connection_types()
            co_index_a, co_index_b = wire.get_wire_connection_index()

            if co_type_a == "OUTPUT":
                in_unit, out_unit = unit_a, unit_b
                in_index, out_index = co_index_a, co_index_b
            else:
                in_unit, out_unit = unit_b, unit_a
                in_index, out_index = co_index_b, co_index_a

            if last_unit.get_name() == "NONE":
                result += f"{in_unit.get_name()}({in_index})--->({out_index}){out_unit.get_name()}"
            elif last_unit == in_unit:
                result += f"({in_index})--->({out_index}){out_unit.get_name()}"
            else:
                result += "\n"
                result += f"{in_unit.get_name()}({in_index})--->({out_index}){out_unit.get_name()}"
            last_unit = out_unit

        return result

    def get_internal_input_pin(self, index: int) -> PhysicalUnit:
        return self.internal_input_pin_list[index]

    def get_internal_input_pin_list(self) -> list:
        return self.internal_input_pin_list

    def get_internal_output_pin(self, index: int) -> PhysicalUnit:
        return self.internal_output_pin_list[index]

    def get_internal_output_pin_list(self) -> list:
        return self.internal_output_pin_list

    def make_internal_logic(self, internal_input_pin_list: list, internal_output_pin_list: list):
        """
        Use a list of input pin and a list of output pin to represent the unites who will be a part of the ship
        """
        assert len(internal_input_pin_list) == self.get_input_unit_count(), "Wrong count !"
        assert len(internal_output_pin_list) == self.get_output_unit_list_count(), "Wrong count !"

        # Destruction des liens avec l'extérieur pour les pins internes
        for internal_input_pin in internal_input_pin_list:
            assert isinstance(internal_input_pin, Pin), "This unit isn't a pin !"
            internal_input_pin.clear_input_unit_list()
        for internal_output_pin in internal_output_pin_list:
            assert isinstance(internal_output_pin, Pin), "This unit isn't a pin !"
            internal_output_pin.clear_output_unit_main_list()

        self.internal_input_pin_list = internal_input_pin_list.copy()
        self.internal_output_pin_list = internal_output_pin_list.copy()

        self.update_value()

    def update_value(self):
        # Copie des valeurs des unitées d'entrée dans les input pin internes
        for i in range(self.input_unit_count):
            interface_input_unit = self.get_input_unit(i)
            assert isinstance(interface_input_unit, DigitalUnit), "This object isn't a DigitalUnit !"
            value = interface_input_unit.get_current_value()

            internal_input_pin = self.get_internal_input_pin(i)
            assert isinstance(internal_input_pin, Pin), "This unit isn't a Pin !"
            internal_input_pin.set_value(value)
            internal_input_pin.update_all_output_unit()

        # Calcul de la valeur de sortie
        output_string = ""
        for i in range(self.output_unit_list_count):
            internal_output_pin = self.get_internal_output_pin(i)
            assert isinstance(internal_output_pin, Pin), "This unit isn't a Pin !"
            value = internal_output_pin.get_current_value()
            output_string += f"{value} "

        if output_string != "":
            output_string = output_string[:-1]
        else:
            raise Exception("output_string vide !")

        if output_string != self.get_current_value():
            self.set_value(output_string)
            # Mise a jour des valeurs dans les unitées branchées au ship
            for output_unit in self.get_all_output_unit():
                output_unit.update_all_output_unit()


"""
Useful methode
"""


def connect_wire(unit_a: PhysicalUnit, output_index: int,
                 unit_b: PhysicalUnit, input_index: int) -> Wire:
    wire_data_output = {
        "unit": unit_a, "connection_type": "OUTPUT", "connection_index": output_index
    }
    wire_data_input = {
        "unit": unit_b, "connection_type": "INPUT", "connection_index": input_index
    }
    wire = Wire(f"{unit_a.get_name()}--->{unit_b.get_name()}")

    wire.link_wire_to_unites(wire_data_output, wire_data_input)

    return wire


def get_wire(unit_a: PhysicalUnit, unit_b: PhysicalUnit) -> Wire:
    unit_a__unit_list = unit_a.get_input_unit_list() + unit_a.get_all_output_unit()
    unit_b__unit_list = unit_b.get_input_unit_list() + unit_b.get_all_output_unit()

    i = 0
    common_unit = DigitalUnit("NONE")
    while i < len(unit_a__unit_list) and common_unit.get_name() == "NONE":
        target_unit = unit_a__unit_list[i]
        if target_unit.get_name() != "NONE" and target_unit in unit_b__unit_list:
            common_unit = target_unit
        i += 1

    assert isinstance(common_unit, Wire), "This unit isn't a wire !"
    return common_unit


def disconnect_wire(unit_a: PhysicalUnit, unit_b: PhysicalUnit) -> Wire:
    common_unit = get_wire(unit_a, unit_b)
    common_unit.disconnect()
    return common_unit


def take_every_connected_unit(unit_list: list, start_unit: PhysicalUnit, take_in_input: bool, take_in_output: bool):
    if take_in_input:
        for unit in start_unit.get_input_unit_list():
            if unit.get_name() != "NONE" and unit not in unit_list:
                unit_list.append(unit)
                take_every_connected_unit(unit_list, unit, True, False)
    if take_in_output:
        for unit in start_unit.get_all_output_unit():
            if unit.get_name() != "NONE" and unit not in unit_list:
                unit_list.append(unit)
                take_every_connected_unit(unit_list, unit, False, True)


def find_unit_index_in_list(unit_list: list, unit: DigitalUnit) -> int:
    for i in range(len(unit_list)):
        current_unit = unit_list[i]
        if current_unit == unit:
            return i
    return -1


def dec_to_bin(dec_number: int) -> list:
    bin_list = []
    while dec_number != 0:
        bin_list.insert(0, dec_number % 2)
        dec_number //= 2
    if len(bin_list) == 0:
        bin_list = [0]
    return bin_list


def make_all_bit_combination(element_size: int) -> list:
    bit_combination = []
    for i in range(2 ** element_size):
        bin_list = dec_to_bin(i)
        while len(bin_list) < element_size:
            bin_list.insert(0, 0)
        bit_combination.append(bin_list)
    return bit_combination


def list_to_str(lst: list) -> str:
    result = ""
    for elt in lst:
        result += f"{elt} "
    return result[:-1]


def convert_ship_to_logic_gate(ship: Ship) -> LogicGate:
    # Récupération des données
    test_ship = ship.copy()

    test_input_pin_count = test_ship.get_input_unit_count()
    test_input_pin_list = []
    for i in range(test_input_pin_count):
        test_input_pin = Pin(f"test_pin_{i}")
        connect_wire(test_input_pin, 0, test_ship, i)
        test_input_pin_list.append(test_input_pin)

    # Partie test
    bit_combination_list = make_all_bit_combination(test_input_pin_count)
    logic_dict = {}
    for current_bit_combination in bit_combination_list:
        for i in range(test_input_pin_count):
            test_input_pin = test_input_pin_list[i]
            assert isinstance(test_input_pin, Pin), "This unit isn't a Pin !"
            test_input_pin.set_value(str(current_bit_combination[i]))
            test_input_pin.update_all_output_unit()
        current_value = test_ship.get_current_value()

        current_bit_combination_string = list_to_str(current_bit_combination)
        logic_dict[current_bit_combination_string] = current_value

    return LogicGate(f"{test_ship.get_name()}_LOGIC", logic_dict)


def reverse_list(lst: list) -> list:
    nl = []
    for e in lst:
        nl.insert(0, e)
    return nl
