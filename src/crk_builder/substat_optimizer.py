from typing import Optional

import os
import re

class SubstatOptimizer:
    def __init__(self):
        # List of tuples: (topping number, value)
        # I also specify the number of each list for later use
        self.__atk_list    : list = [] # 0
        self.__atk_spd_list: list = [] # 1
        self.__crit_list   : list = [] # 2
        self.__cd_list     : list = [] # 3
        self.__dr_list     : list = [] # 4

    def perform_optimization(self, substats: tuple[int, ...]) -> None:
        self.__extract_substats()

        # You can only specify 2 or 3 substats
        if len(substats) < 2 or len(substats) > 3:
            return

        # Help list to find the specified substats
        substat_list: list = [self.__atk_list, self.__atk_spd_list, self.__crit_list
            , self.__cd_list, self.__dr_list]

        # Case of 2 substats
        if len(substats) == 2:
            substat_one_list: list = substat_list[substats[0]] # First  substat list requested
            substat_two_list: list = substat_list[substats[1]] # Second substat list requested

            # Lists with toppings that include the two specified substats
            matched_substat_one: list = []
            matched_substat_two: list = []

            # Check and put in the new lists the toppings that contain these two substats
            # topping_one/two is the tuple (topping_position, topping_value)
            for topping_one in substat_one_list:
                for topping_two in substat_two_list:
                    # topping_one[0] is the position of the topping
                    if topping_one[0] == topping_two[0]:
                        # The current topping contains both substats
                        # topping_one[1] is the value of the topping
                        matched_substat_one.append((topping_one[0], topping_one[1]))
                        matched_substat_two.append((topping_two[0], topping_two[1]))

            # List with the optimized values
            optimized_list: list = []

            for topping_one, topping_two in zip(matched_substat_one, matched_substat_two):
                # Will be used to store and insert the optimized value in the list
                optimized_value: float = 0

                # Checks are carried out twice, once for the first list and once for the second list
                # substats[0] is the first substat specified and substats[1] is the second substat specified
                # topping_one/two[1] is the value of the topping

                # ATK, ATK SPD, CRIT%
                if substats[0] in (0, 1, 2):
                    optimized_value += topping_one[1] / 3.0
                if substats[1] in (0, 1, 2):
                    optimized_value += topping_two[1] / 3.0

                # CD
                if substats[0] == 3:
                    optimized_value += topping_one[1] / 2.0
                if substats[1] == 3:
                    optimized_value += topping_two[1] / 2.0

                # CD
                if substats[0] == 4:
                    optimized_value += topping_one[1] / 6.0
                if substats[1] == 4:
                    optimized_value += topping_two[1] / 6.0

                # We add the value to the optimized list
                # topping_one[0] is the topping position
                # As they are the same, it doesn't matter
                optimized_list.append((topping_one[0], optimized_value))

            # We order from the highest to lowest optimized value
            # x[1] represents the second element of the tuple, meaning the optimized value
            optimized_list.sort(key = lambda x: x[1], reverse = True)

            print("[The maximum value with 2 substats is: 2.0]")
            for topping_position, topping_score in optimized_list:
                print(f"Topping Position ({topping_position}): Score => {topping_score}")

    # Extracts the topping number and its substat in the list that belongs to it.
    def __extract_substats(self) -> None:
        # Get paths
        current_path: str = os.path.dirname(os.path.abspath(__file__))
        text_path   : str = os.path.abspath(os.path.join(current_path
            , "..", "..", "topping_substats.txt"))

        # Read the text file to extract the substats
        with open(text_path, "r") as topping_file:
            # It will indicate the number of the topping we are working with
            topping_number: int = 0
            for line in topping_file:
                # Topping Number Regex
                match: Optional[re.Match] = re.search(r"\[Topping (\d+)]", line)
                if match:
                    topping_number = int(match.group(1))

                # ATK Regex
                match: Optional[re.Match] = re.search(r"ATK\s+(\d+(?:\.\d+)?)%", line)
                if match:
                    atk_value: float = float(match.group(1))
                    self.__atk_list.append((topping_number, atk_value))

                # ATK SPD Regex
                match: Optional[re.Match] = re.search(r"ATK SPD\s+(\d+(?:\.\d+)?)%", line)
                if match:
                    atk_spd_value: float = float(match.group(1))
                    self.__atk_spd_list.append((topping_number, atk_spd_value))

                # CRIT Regex
                match: Optional[re.Match] = re.search(r"CRIT%\s+(\d+(?:\.\d+)?)%", line)
                if match:
                    crit_value: float = float(match.group(1))
                    self.__crit_list.append((topping_number, crit_value))

                # CD Regex
                match: Optional[re.Match] = re.search(r"Cooldown\s+(\d+(?:\.\d+)?)%", line)
                if match:
                    cd_value: float = float(match.group(1))
                    self.__cd_list.append((topping_number, cd_value))

                # DR Regex
                match: Optional[re.Match] = re.search(r"DMG Resist\s+(\d+(?:\.\d+)?)%", line)
                if match:
                    dr_value: float = float(match.group(1))
                    self.__dr_list.append((topping_number, dr_value))