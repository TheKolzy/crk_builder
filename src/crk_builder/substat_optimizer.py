from typing import Optional

import os
import re

class SubstatOptimizer:
    def __init__(self, strict: bool):
        # List of tuples, each containing: (topping index, value)

        # Specifying the index of each list for later use
        # | 0 ATK | 1 HP | 2 ATK SPD | 3 CRIT% | 4 Cooldown | 5 DMG Resist |
        self.__atk_list    : list = [] # 0
        self.__hp_list     : list = [] # 1
        self.__atk_spd_list: list = [] # 2
        self.__crit_list   : list = [] # 3
        self.__cd_list     : list = [] # 4
        self.__dr_list     : list = [] # 5
        self.__strict      : bool = strict # To make the optimization stricter

    def perform_optimization(self, substats: tuple[int, ...]) -> None:
        self.__extract_substats()

        # Only 2 or 3 substats can be specified at the same time
        if len(substats) < 2 or len(substats) > 3:
            return

        # Case of 2 substats
        if len(substats) == 2:
            optimized_list: list = self.__optimize_two_substats(substats)
            self.__print_two_substats(optimized_list)

        # Case of 3 substats
        if len(substats) == 3:
            optimized_list: list = self.__optimize_three_substats(substats)
            self.__print_three_substats(optimized_list)

    def __optimize_three_substats(self, substats: tuple[int, ...]) -> list:
        # Help list to find the specified substats
        substat_list: list = [self.__atk_list, self.__hp_list, self.__atk_spd_list
            , self.__crit_list, self.__cd_list, self.__dr_list]

        # List with the optimized values
        optimized_list: list = []

        substat_one_list  : list = substat_list[substats[0]]  # First  substat list requested
        substat_two_list  : list = substat_list[substats[1]]  # Second substat list requested
        substat_three_list: list = substat_list[substats[2]]  # Third  substat list requested

        # Lists with toppings that include the three specified substats
        matched_substat_one  : list = []
        matched_substat_two  : list = []
        matched_substat_three: list = []

        # Check and put in the new lists the toppings that contain these three substats
        # Variable topping_one/two/three is the tuple (topping_index, topping_value)
        for topping_one in substat_one_list:
            for topping_two in substat_two_list:
                # Variable topping_one/two/three[0] is the index of the topping
                if topping_one[0] == topping_two[0]:
                    # The current topping contains the two substats
                    # But we need to contain three so we make another for loop
                    for topping_three in substat_three_list:
                        if topping_one[0] == topping_three[0]:
                            # The current topping contains the three substats
                            # topping_one/two/three[1] is the value of the topping
                            matched_substat_one.append((topping_one[0], topping_one[1]))
                            matched_substat_two.append((topping_two[0], topping_two[1]))
                            matched_substat_three.append((topping_three[0], topping_three[1]))

        # Once we have the toppings that share substats, we optimize
        for topping_one, topping_two, topping_three in (zip
            (matched_substat_one, matched_substat_two, matched_substat_three)):
            # Will be used to store and insert the optimized value in the list
            optimized_value: float = 0

            # Checks are carried out three times, once for the first list, once for the second list and once for the third list
            # substats[0] is the first substat specified, substats[1] is the second substat specified
            # substats[2] is the third substat specified
            # topping_one/two/three[1] is the value of the topping

            # ATK, HP, ATK SPD, CRIT%
            if substats[0] in (0, 1, 2, 3):
                if self.__strict == True:
                    if topping_one[1] >= 1.8:
                        optimized_value += topping_one[1] / 3.0
                else:
                    optimized_value += topping_one[1] / 3.0
            if substats[1] in (0, 1, 2, 3):
                if self.__strict == True:
                    if topping_two[1] >= 1.8:
                        optimized_value += topping_two[1] / 3.0
                else:
                    optimized_value += topping_two[1] / 3.0
            if substats[2] in (0, 1, 2, 3):
                if self.__strict == True:
                    if topping_three[1] >= 1.8:
                        optimized_value += topping_three[1] / 3.0
                else:
                    optimized_value += topping_three[1] / 3.0

            # Cooldown
            if substats[0] == 4:
                if self.__strict == True:
                    if topping_one[1] >= 1.4:
                        optimized_value += topping_one[1] / 2.0
                else:
                    optimized_value += topping_one[1] / 2.0
            if substats[1] == 4:
                if self.__strict == True:
                    if topping_two[1] >= 1.4:
                        optimized_value += topping_two[1] / 2.0
                else:
                    optimized_value += topping_two[1] / 2.0
            if substats[2] == 4:
                if self.__strict == True:
                    if topping_three[1] >= 1.4:
                        optimized_value += topping_three[1] / 2.0
                else:
                    optimized_value += topping_three[1] / 2.0

            # DMG Resist
            if substats[0] == 5:
                if self.__strict == True:
                    if topping_one[1] >= 4.6:
                        optimized_value += topping_one[1] / 6.0
                else:
                    optimized_value += topping_one[1] / 6.0
            if substats[1] == 5:
                if self.__strict == True:
                    if topping_two[1] >= 4.6:
                        optimized_value += topping_two[1] / 6.0
                else:
                    optimized_value += topping_two[1] / 6.0
            if substats[2] == 5:
                if self.__strict == True:
                    if topping_three[1] >= 4.6:
                        optimized_value += topping_three[1] / 6.0
                else:
                    optimized_value += topping_three[1] / 6.0

            # We add the value to the optimized list
            # Variable topping_one/two/three[0] is the topping index
            # As they are the same, it doesn't matter
            optimized_list.append((topping_one[0], optimized_value))

        return optimized_list

    def __optimize_two_substats(self, substats: tuple[int, ...]) -> list:
        # Help list to find the specified substats
        substat_list: list = [self.__atk_list, self.__hp_list, self.__atk_spd_list
            , self.__crit_list, self.__cd_list, self.__dr_list]

        # List with the optimized values
        optimized_list: list = []

        substat_one_list: list = substat_list[substats[0]]  # First  substat list requested
        substat_two_list: list = substat_list[substats[1]]  # Second substat list requested

        # Lists with toppings that include the two specified substats
        matched_substat_one: list = []
        matched_substat_two: list = []

        # Check and put in the new lists the toppings that contain these two substats
        # Variable topping_one/two is the tuple (topping_index, topping_value)
        for topping_one in substat_one_list:
            for topping_two in substat_two_list:
                # Variable topping_one/two[0] is the index of the topping
                if topping_one[0] == topping_two[0]:
                    # The current topping contains both substats
                    # Variable topping_one/two[1] is the value of the topping
                    matched_substat_one.append((topping_one[0], topping_one[1]))
                    matched_substat_two.append((topping_two[0], topping_two[1]))

        # Once we have the toppings that share substats, we optimize
        for topping_one, topping_two in zip(matched_substat_one, matched_substat_two):
            # Will be used to store and insert the optimized value in the list
            optimized_value: float = 0

            # Checks are carried out twice, once for the first list and once for the second list
            # substats[0] is the first substat specified and substats[1] is the second substat specified
            # topping_one/two[1] is the value of the topping

            # ATK, HP, ATK SPD, CRIT%
            if substats[0] in (0, 1, 2, 3):
                # If strict optimization is activated
                if self.__strict == True:
                    # The higher the value, the better the results, but the quantity also decreases
                    if topping_one[1] >= 1.8:
                        optimized_value += topping_one[1] / 3.0
                else:
                    optimized_value += topping_one[1] / 3.0
            if substats[1] in (0, 1, 2, 3):
                if self.__strict == True:
                    if topping_two[1] > 1.8:
                        optimized_value += topping_two[1] / 3.0
                else:
                    optimized_value += topping_two[1] / 3.0

            # Cooldown
            if substats[0] == 4:
                if self.__strict == True:
                    if topping_one[1] >= 1.4:
                        optimized_value += topping_one[1] / 2.0
                else:
                    optimized_value += topping_one[1] / 2.0
            if substats[1] == 4:
                if self.__strict == True:
                    if topping_two[1] >= 1.4:
                        optimized_value += topping_two[1] / 2.0
                else:
                    optimized_value += topping_two[1] / 2.0

            # DMG Resist
            if substats[0] == 5:
                if self.__strict == True:
                    if topping_one[1] >= 4.6:
                        optimized_value += topping_one[1] / 6.0
                else:
                    optimized_value += topping_one[1] / 6.0
            if substats[1] == 5:
                if self.__strict == True:
                    if topping_two[1] >= 4.6:
                        optimized_value += topping_two[1] / 6.0
                else:
                    optimized_value += topping_two[1] / 6.0

            # We add the value to the optimized list
            # topping_one[0] and topping_two[0] is the topping index
            # As they are the same, it doesn't matter
            optimized_list.append((topping_one[0], optimized_value))

        return optimized_list

    # Extract the topping index and its substats in the list that belongs to it
    def __extract_substats(self) -> None:
        # Get the path of the substats file
        current_path : str = os.path.dirname(os.path.abspath(__file__))
        substats_file: str = os.path.abspath(os.path.join(current_path
            , "..", "..", "topping_substats.txt"))

        # Read the file to extract the substats
        with open(substats_file, "r") as topping_file:
            # Number used to differentiate toppings
            topping_index: int = 0
            for line in topping_file:
                # Topping Number Regex
                match: Optional[re.Match] = re.search(r"\[Topping (\d+)]", line)
                if match:
                    topping_index = int(match.group(1))

                # ATK Regex
                match: Optional[re.Match] = re.search(r"ATK\s+(\d+(?:\.\d+)?)%", line)
                if match:
                    atk_value: float = float(match.group(1))
                    self.__atk_list.append((topping_index, atk_value))

                # HP Regex
                match: Optional[re.Match] = re.search(r"HP\s+(\d+(?:\.\d+)?)%", line)
                if match:
                    hp_value: float = float(match.group(1))
                    self.__hp_list.append((topping_index, hp_value))

                # ATK SPD Regex
                match: Optional[re.Match] = re.search(r"ATK SPD\s+(\d+(?:\.\d+)?)%", line)
                if match:
                    atk_spd_value: float = float(match.group(1))
                    self.__atk_spd_list.append((topping_index, atk_spd_value))

                # CRIT% Regex
                match: Optional[re.Match] = re.search(r"CRIT%\s+(\d+(?:\.\d+)?)%", line)
                if match:
                    crit_value: float = float(match.group(1))
                    self.__crit_list.append((topping_index, crit_value))

                # Cooldown Regex
                match: Optional[re.Match] = re.search(r"Cooldown\s+(\d+(?:\.\d+)?)%", line)
                if match:
                    cd_value: float = float(match.group(1))
                    self.__cd_list.append((topping_index, cd_value))

                # DMG Resist Regex
                match: Optional[re.Match] = re.search(r"DMG Resist\s+(\d+(?:\.\d+)?)%", line)
                if match:
                    dr_value: float = float(match.group(1))
                    self.__dr_list.append((topping_index, dr_value))

    def __print_two_substats(self, optimized_list: list) -> None:
        # We order from the highest to lowest optimized value
        # Variable x[1] represents the second element of the tuple, meaning the optimized value
        optimized_list.sort(key = lambda x: x[1], reverse = True)

        # To ensure that all the toppings have been read, for the developer
        iterator: int = 1
        print("[The maximum value with 2 substats is: 2.0]")
        for topping_position, topping_score in optimized_list:
            # If strict optimization is activated
            if self.__strict == True:
                # Only consider those that are strictly optimized
                if topping_score > 1.0:
                    print(f"[{iterator}] Topping Position ({topping_position}): Score => {topping_score}")
                    iterator += 1
            else:
                print(f"[{iterator}] Topping Position ({topping_position}): Score => {topping_score}")
                iterator += 1

    def __print_three_substats(self, optimized_list: list) -> None:
        # We order from the highest to lowest optimized value
        # Variable x[1] represents the second element of the tuple, meaning the optimized value
        optimized_list.sort(key = lambda x: x[1], reverse = True)

        # To ensure that all the toppings have been read, for the developer
        iterator: int = 1
        print("[The maximum value with 3 substats is: 3.0]")
        for topping_position, topping_score in optimized_list:
            if self.__strict == True:
                if topping_score > 2.0:
                    print(f"[{iterator}] Topping Position ({topping_position}): Score => {topping_score}")
                    iterator += 1
            else:
                print(f"[{iterator}] Topping Position ({topping_position}): Score => {topping_score}")
                iterator += 1