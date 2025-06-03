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

    def perform_optimization(self) -> None:
        self.__extract_substats()

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