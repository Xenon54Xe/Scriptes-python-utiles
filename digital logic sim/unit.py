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
        self.value = "0"  # Represent the logic state of the unit

    def copy(self):
        """
        Copy the unit as a new unit (the original and the copy are not linked)
        The logic state of the copied unit is the same as the original
        """
        unit = DigitalUnit(self.name)
        unit.set_value(self.value)
        return unit

    def get_name(self) -> str:
        return self.name

    def get_current_value(self) -> str:
        """
        Return the current logic state of the unit
        """
        return self.value

    def set_name(self, new_name: str):
        self.name = new_name

    def set_value(self, new_value: str):
        """
        Set the logical state of the unit
        """
        self.value = new_value

    def update_value(self):
        """
        Update the logic state of this unit according to the state of units linked to its inputs
        """
        pass


class PhysicalUnit(DigitalUnit):
    def __init__(self, name: str, input_unit_count: int, output_unit_list_count: int):
        """
        Represent the physical part of a logic unit
        """
        super().__init__(name)

        # Represent the inputs of the unit
        self.input_unit_count = input_unit_count
        self.input_unit_list = [DigitalUnit("NONE")] * input_unit_count

        # Represent the outputs of the unit
        # Each output has a list that represent every other unit linked to this output
        self.output_unit_list_count = output_unit_list_count
        self.output_unit_main_list = []
        for i in range(output_unit_list_count):
            self.output_unit_main_list.append([])

    def copy(self):
        return PhysicalUnit(self.name, self.input_unit_count, self.output_unit_list_count)

    def get_input_unit_count(self) -> int:
        """
        Return the number of input of this unit (linked to other unit or not)
        """
        return self.input_unit_count

    def get_input_unit(self, index: int) -> DigitalUnit:
        """
        Return the unit linked to the input at index <index>
        """
        return self.input_unit_list[index]

    def get_input_unit_list(self) -> list:
        """
        Return the list of unit linked to the inputs
        If an input is not linked the unit will have the name 'NONE'
        """
        return self.input_unit_list

    def get_free_input_index(self) -> list:
        """
        Return the list of index of input that are not already linked
        """
        index = []
        for i in range(self.input_unit_count):
            unit = self.input_unit_list[i]
            if unit.get_name() == "NONE":
                index.append(i)
        return index

    def get_output_unit_list_count(self) -> int:
        """
        Return the number of output of this unit
        """
        return self.output_unit_list_count

    def get_output_unit_list(self, index: int) -> list:
        """
        Return the list of unit linked to the output at index <index>
        """
        return self.output_unit_main_list[index]

    def get_all_output_unit(self) -> list:
        """
        Return the list of every unit linked to every output of this unit
        """
        unit_list = []
        for output_unit_list in self.output_unit_main_list:
            for output_unit in output_unit_list:
                unit_list.append(output_unit)
        return unit_list

    def get_all_connected_unit(self) -> list:
        """
        Return all connected unit to this unit, without this unit in the list if she is not connected to itself
        """
        connected_unit = []
        take_every_connected_unit(connected_unit, self, True, True)
        return connected_unit

    def set_value(self, new_value: str):
        super().set_value(new_value)
        self.update_all_output_unit()

    def set_input_unit(self, index: int, new_unit: DigitalUnit):
        """
        Link the unit <new_unit> to the input at index <index> if this input hasn't already another unit linked to
        """
        current_unit = self.input_unit_list[index]
        if current_unit.get_name() != "NONE":
            raise Exception(f"{self.get_name()}: You need to disconnect the unit at index {index} "
                            f"before connecting '{new_unit.get_name()}'")
        self.input_unit_list[index] = new_unit

    def pop_input_unit(self, index: int):
        """
        Unlink the unit linked to the input at index <index>
        """
        self.input_unit_list[index] = DigitalUnit("NONE")

    def clear_input_unit_list(self):
        """
        Unlink every unit linked to the inputs
        """
        for i in range(self.input_unit_count):
            self.pop_input_unit(i)

    def add_output_unit(self, index: int, new_unit: DigitalUnit):
        """
        Link a <new_unit> to the output at index <index> if the unit isn't already linked
        """
        target_output_unit_list = self.get_output_unit_list(index)
        if new_unit not in target_output_unit_list:
            target_output_unit_list.append(new_unit)
        else:
            raise Exception(f"The unit <{new_unit.get_name()}> is already in output pin index: {index}")

    def pop_output_unit(self, output_index: int, unit_index: int):
        """
        Pop the unit at index <unit_index> linked from the output at index <output_index>
        """
        self.output_unit_main_list[output_index].pop(unit_index)

    def remove_output_unit(self, index: int, unit: DigitalUnit):
        """
        Remove the unit <unit> from the output at index <index> if this unit is linked to the output
        """
        self.output_unit_main_list[index].remove(unit)

    def clear_output_unit_list(self, index: int):
        """
        Remove every unit linked to the output at index <index>
        """
        self.output_unit_main_list[index].clear()

    def clear_output_unit_main_list(self):
        """
        Remove every unit linked to every output of the unit
        """
        for i in range(self.output_unit_list_count):
            self.clear_output_unit_list(i)

    def disconnect(self) -> tuple:
        """
        Remove every unit linked to every input or output of the unit and return the list of unlinked unit
        The disconnection is done by wire
        """
        disconnected_unit_list = []
        for wire in self.get_input_unit_list() + self.get_all_output_unit():
            if isinstance(wire, Wire):
                wire.disconnect()
                disconnected_unit_list.append(wire)
        return tuple(disconnected_unit_list)

    def update_all_output_unit(self):
        """
        Update the logic state of every unit linked to the outputs of this unit
        """
        for output_unit in self.get_all_output_unit():
            assert isinstance(output_unit, DigitalUnit), f"The unit isn't a DigitalUnit !"
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
        Represent a wire that will be linked to other unit

        When you link a wire with the link type "INPUT" the wire is linked to the input of a unit
        """
        super().__init__(name, 1, 1)

        # Example: unit_data = {"unit": nand_ship, "link_type": "INPUT", "link_index": 0}
        self.unit_datas = []

    def copy(self):
        return Wire(self.name)

    def get_linked_unit(self) -> tuple:
        """
        Return the units linked to the wire
        """
        return self.unit_datas[0]["unit"], self.unit_datas[1]["unit"]

    def get_link_types(self) -> tuple:
        """
        Return the link type (input or output) of the wire in other units
        """
        return self.unit_datas[0]["link_type"], self.unit_datas[1]["link_type"]

    def get_link_index(self) -> tuple:
        """
        Return the link index of the wire in other units
        """
        return self.unit_datas[0]["link_index"], self.unit_datas[1]["link_index"]

    def link_wire_to_units(self, unit_data_a: dict, unit_data_b: dict):
        """
        unit_data: a dict with keys 'unit', 'link_type', 'link_index'
        representing the link type between the wire and the unit

        Example: unit_data = {"unit": nand_ship, "link_type": "INPUT", "link_index": 0}

        pin_type can be 'INPUT' or 'OUTPUT'
        """
        unit_a, link_type_a, link_index_a = (unit_data_a["unit"], unit_data_a["link_type"],
                                             unit_data_a["link_index"])
        unit_b, link_type_b, link_index_b = (unit_data_b["unit"], unit_data_b["link_type"],
                                             unit_data_b["link_index"])
        allowed_type = ["INPUT", "OUTPUT"]
        assert link_type_a != link_type_b, "The wire need to go from an output pin to an input pin"
        assert link_type_a in allowed_type, "The pin_a need to have a type of: INPUT or OUTPUT"
        assert link_type_b in allowed_type, "The pin_a need to have a type of: INPUT or OUTPUT"

        allowed_keys = ["unit", "link_type", "link_index"]
        for key in unit_data_a.keys():
            assert key in allowed_keys, f"The key referred is not allowed: {key}"
        for key in unit_data_b.keys():
            assert key in allowed_keys, f"The key referred is not allowed: {key}"

        self.unit_datas = [unit_data_a, unit_data_b]

        for unit_data in self.unit_datas:
            unit, link_type, link_index = (unit_data["unit"], unit_data["link_type"],
                                           unit_data["link_index"])
            if isinstance(unit, PhysicalUnit):
                if link_type == "INPUT":
                    unit.set_input_unit(link_index, self)
                    self.add_output_unit(0, unit)
                elif link_type == "OUTPUT":
                    unit.add_output_unit(link_index, self)
                    self.set_input_unit(0, unit)
            else:
                raise Exception(f"The unit isn't a PhysicalUnit !")

        linked_units = self.get_linked_unit()
        try:
            self.update_value()
            for unit in linked_units:
                assert isinstance(unit, PhysicalUnit), f"The unit isn't a PhysicalUnit !"
                unit.update_value()
            self.update_value()
        except RecursionError as err:
            self.disconnect()
            for unit in linked_units:
                assert isinstance(unit, PhysicalUnit), f"The unit isn't a PhysicalUnit !"
                unit.update_value()
            raise err
        except Exception as exc:
            raise exc

    def disconnect(self):
        """
        Remove every unit linked to this wire
        """
        # Remove units
        for unit_data in self.unit_datas:
            unit, link_type, link_index = (unit_data["unit"], unit_data["link_type"],
                                           unit_data["link_index"])
            if isinstance(unit, PhysicalUnit):
                if link_type == "INPUT":
                    unit.pop_input_unit(link_index)
                elif link_type == "OUTPUT":
                    unit.remove_output_unit(link_index, self)
            else:
                raise Exception(f"The unit isn't a PhysicalUnit !")

        # Update units
        for unit in self.get_linked_unit():
            assert isinstance(unit, DigitalUnit), f"The unit isn't a DigitalUnit !"
            unit.update_value()

        self.unit_datas = []

    def update_value(self):
        unit_a, unit_b = self.get_linked_unit()
        assert isinstance(unit_a, PhysicalUnit), f"The unit isn't a PhysicalUnit !"
        assert isinstance(unit_b, PhysicalUnit), f"The unit isn't a PhysicalUnit !"
        link_type_a, link_type_b = self.get_link_types()
        link_index_a, link_index_b = self.get_link_index()

        output_value = "-1"
        if link_type_a == "OUTPUT":
            brut_value = unit_a.get_current_value()
            brut_value_list = brut_value.split(" ")
            output_value = brut_value_list[link_index_a]
        elif link_type_b == "OUTPUT":
            brut_value = unit_b.get_current_value()
            brut_value_list = brut_value.split(" ")
            output_value = brut_value_list[link_index_b]

        assert output_value != "-1", f"The wire <{self.name}> isn't linked properly (input missing)"

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
        # Number of different input logic states possible
        self.logic_count = -1

        self.make_unit()  # set: input/output pin count, logic count

        super().__init__(name, self.input_unit_count, self.output_unit_list_count)

        self.update_value()

    def copy(self):
        return LogicGate(self.name, self.logic)

    def make_unit(self):
        """
        Make the logic unit according to his logic dictionary
        """
        # Input pin count
        first_input_unit_count = -1
        last_logic_input = None
        # Output pin count
        first_output_unit_count = -1
        last_logic_output = None

        # Counting and verification in the logic dictionary
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
        """
        Return the logic dictionary of the logic gate
        """
        return self.logic

    def get_logic_count(self) -> int:
        """
        Return the number of different input logic states possible
        """
        return self.logic_count

    def update_value(self):
        # Gathering of input unit states
        input_string = ""
        for input_unit in self.input_unit_list:
            assert isinstance(input_unit, DigitalUnit), "The object isn't a DigitalUnit !"
            input_string += f"{input_unit.get_current_value()} "
        input_string = input_string[:-1]

        # Making output
        try:
            output_string = self.logic[input_string]
        except:
            raise Exception(f"{self.get_name()}: The logic input doesn't match logic dictionary (got:{input_string})")

        # Update of every linked units if necessary
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

        # Internal units of the ship
        self.internal_input_pin_list = []
        self.internal_output_pin_list = []

    def copy(self):
        # Internal unit list: Pin, Wire, LogicalGate
        unit_list = self.get_every_internal_unit()
        # Creation of the list that will contain a copy of every internal entities
        unit_list_copy = []

        # Creation of the list that will contain every link between units
        link_list = []

        # Searching of links and copy of every unit
        for i in range(len(unit_list)):
            current_unit = unit_list[i]
            assert isinstance(current_unit, PhysicalUnit), "This unit isn't a PhysicalUnit !"

            unit_list_copy.append(current_unit.copy())

            # If the unit is a wire, make a copy of the data of this wire and put this in link list
            if isinstance(current_unit, Wire):
                unit_a, unit_b = current_unit.get_linked_unit()
                link_type_a, link_type_b = current_unit.get_link_types()
                link_index_a, link_index_b = current_unit.get_link_index()

                # Positions in unit_list are used to find the right copy in unit_list_copy
                unit_a_position = find_unit_index_in_list(unit_list, unit_a)
                unit_b_position = find_unit_index_in_list(unit_list, unit_b)

                assert unit_a_position != -1, f"The unit ({unit_a.get_name()}) was not found on the list !"
                assert unit_b_position != -1, f"The unit ({unit_b.get_name()}) was not found on the list !"

                wire_data = {
                    "unit_a_position": unit_a_position,
                    "unit_b_position": unit_b_position,
                    "link_type_a": link_type_a,
                    "link_type_b": link_type_b,
                    "link_index_a": link_index_a,
                    "link_index_b": link_index_b
                }
                link_list.append(wire_data)
            else:
                link_list.append(None)

        # Linking of copied wires to the right copied units
        for i in range(len(unit_list_copy)):
            current_unit_copy = unit_list_copy[i]

            # If it's a wire, take his data from link_list and link him to the rights units
            if isinstance(current_unit_copy, Wire):
                wire_data = link_list[i]
                assert isinstance(wire_data, dict), "This object isn't a dictionary !"

                unit_a, unit_b = (unit_list_copy[wire_data["unit_a_position"]],
                                  unit_list_copy[wire_data["unit_b_position"]])

                link_type_a, link_type_b = wire_data["link_type_a"], wire_data["link_type_b"]
                link_index_a, link_index_b = wire_data["link_index_a"], wire_data["link_index_b"]

                unit_data_a = {
                    "unit": unit_a,
                    "link_type": link_type_a,
                    "link_index": link_index_a
                }
                unit_data_b = {
                    "unit": unit_b,
                    "link_type": link_type_b,
                    "link_index": link_index_b
                }
                current_unit_copy.link_wire_to_units(unit_data_a, unit_data_b)

        # Creation of the new ship
        new_ship = Ship(self.name, self.input_unit_count, self.output_unit_list_count)

        # Copy of the internal pins
        internal_input_pin_list_copy = []
        internal_output_pin_list_copy = []
        for pin in self.internal_input_pin_list:
            pin_index = find_unit_index_in_list(unit_list, pin)
            assert pin_index != -1, "The pin was not found on the list !"

            pin_copy = unit_list_copy[pin_index]
            assert isinstance(pin_copy, Pin), "This unit isn't a Pin !"

            internal_input_pin_list_copy.append(pin_copy)

        for pin in self.internal_output_pin_list:
            pin_index = find_unit_index_in_list(unit_list, pin)
            assert pin_index != -1, "The pin was not found on the list !"

            pin_copy = unit_list_copy[pin_index]
            assert isinstance(pin_copy, Pin), "This unit isn't a Pin !"

            internal_output_pin_list_copy.append(pin_copy)

        # Finalization of the new ship
        new_ship.make_internal_logic(internal_input_pin_list_copy, internal_output_pin_list_copy)

        return new_ship

    def get_every_internal_unit(self, from_input: bool = True, from_output: bool = True) -> list:
        """
        Return every internal units that are linked directly or not to an input pin or an output pin

        if from_input is set True, the algorithm will search every unit that are linked directly
        or not to an input pin from its input
        """
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
        """
        Return every logic unit in the ship that are not wire or pin
        """
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
        """
        Return every internal wires
        """
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
            unit_a, unit_b = wire.get_linked_unit()
            assert isinstance(unit_a, PhysicalUnit), "This unit isn't a PhysicalUnit !"
            assert isinstance(unit_b, PhysicalUnit), "This unit isn't a PhysicalUnit !"
            co_type_a, co_type_b = wire.get_link_types()
            co_index_a, co_index_b = wire.get_link_index()

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
        """
        Return the internal input pin at index <index>
        """
        return self.internal_input_pin_list[index]

    def get_internal_input_pin_list(self) -> list:
        """
        Return every internal input pin
        """
        return self.internal_input_pin_list

    def get_internal_output_pin(self, index: int) -> PhysicalUnit:
        """
        Return the internal output pin at index <index>
        """
        return self.internal_output_pin_list[index]

    def get_internal_output_pin_list(self) -> list:
        """
        Return every internal output pin
        """
        return self.internal_output_pin_list

    def make_internal_logic(self, internal_input_pin_list: list, internal_output_pin_list: list):
        """
        Use a list of input pin and a list of output pin to represent the unites who will be a part of the ship
        """
        assert len(internal_input_pin_list) == self.get_input_unit_count(), "Wrong count !"
        assert len(internal_output_pin_list) == self.get_output_unit_list_count(), "Wrong count !"

        # Destruction of external links for the internal pins
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
        # Copying of the logic states of the input of this ship to the internal input pins
        for i in range(self.input_unit_count):
            interface_input_unit = self.get_input_unit(i)
            assert isinstance(interface_input_unit, DigitalUnit), "This object isn't a DigitalUnit !"
            value = interface_input_unit.get_current_value()

            internal_input_pin = self.get_internal_input_pin(i)
            assert isinstance(internal_input_pin, Pin), "This unit isn't a Pin !"
            internal_input_pin.set_value(value)
            internal_input_pin.update_all_output_unit()

        # Calculation of the new logic state of the ship
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
            # Update of the logic state of every unit linked to the ship
            for output_unit in self.get_all_output_unit():
                output_unit.update_all_output_unit()


"""
Useful methode
"""


def connect_wire(unit_a: PhysicalUnit, output_index: int,
                 unit_b: PhysicalUnit, input_index: int) -> Wire:
    """
    Create and connect a wire between two unit
    """
    wire_data_output = {
        "unit": unit_a, "link_type": "OUTPUT", "link_index": output_index
    }
    wire_data_input = {
        "unit": unit_b, "link_type": "INPUT", "link_index": input_index
    }
    wire = Wire(f"{unit_a.get_name()}--->{unit_b.get_name()}")

    wire.link_wire_to_units(wire_data_output, wire_data_input)

    return wire


def get_wire(unit_a: PhysicalUnit, unit_b: PhysicalUnit) -> Wire:
    """
    Get the wire that link two units
    """
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
    """
    Disconnect a wire between two units
    """
    common_unit = get_wire(unit_a, unit_b)
    common_unit.disconnect()
    return common_unit


def take_every_connected_unit(unit_list: list, start_unit: PhysicalUnit, take_in_input: bool, take_in_output: bool):
    """
    Recursively go through every unit linked to the first unit and store them in a list
    """
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
    """
    Return the index of a unit in a list
    """
    for i in range(len(unit_list)):
        current_unit = unit_list[i]
        if current_unit == unit:
            return i
    return -1


def dec_to_bin(dec_number: int) -> list:
    """
    Convert a decimal number to a binary number
    """
    bin_list = []
    while dec_number != 0:
        bin_list.insert(0, dec_number % 2)
        dec_number //= 2
    if len(bin_list) == 0:
        bin_list = [0]
    return bin_list


def make_all_bit_combination(n: int) -> list:
    """
    Return a list representing every combination of zero and one with a length of <n>
    """
    bit_combination = []
    for i in range(2 ** n):
        bin_list = dec_to_bin(i)
        while len(bin_list) < n:
            bin_list.insert(0, 0)
        bit_combination.append(bin_list)
    return bit_combination


def list_to_str(lst: list) -> str:
    """
    Convert a list to a string
    """
    result = ""
    for elt in lst:
        result += f"{elt} "
    return result[:-1]


def convert_ship_to_logic_gate(ship: Ship) -> LogicGate:
    """
    Convert a ship to a logic gate by using a brutal method to determine the logic dictionary
    """
    # Récupération des données
    test_ship = ship.copy()

    test_input_pin_count = test_ship.get_input_unit_count()
    test_input_pin_list = []
    for i in range(test_input_pin_count):
        test_input_pin = Pin(f"test_pin_{i}")
        connect_wire(test_input_pin, 0, test_ship, i)
        test_input_pin_list.append(test_input_pin)

    # Testing
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
    """
    Reverse a list
    """
    nl = []
    for e in lst:
        nl.insert(0, e)
    return nl
