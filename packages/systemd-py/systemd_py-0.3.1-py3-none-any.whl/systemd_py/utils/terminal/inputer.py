from typing import List, Any, Dict, TypeVar, Optional


class Inputer:
    Empty = TypeVar("Empty", str, None)

    @staticmethod
    def input(prompt: str, default: Any = None, choices: List[Any] = None, force: bool = False) -> Any:
        """
        Input a value from the user

        :param prompt: The prompt to display to the user
        :type prompt: str

        :param default: The default value to use if the user does not input anything
        :type default: Any

        :param choices: The choices to display to the user
        :type choices: List[Any]

        :param force: Force the user to input a value that exist in choices
        :type force: bool

        :return: The value the user input
        :rtype: Any
        """

        prompt = prompt.strip()

        if choices is None:
            choices = []
        if default is not None:
            choices.append(default)
        if choices:
            prompt += f" ({', '.join(str(choice) for choice in choices)})"

        if not prompt.endswith(":"):
            prompt += ": "
        if not prompt.endswith(" "):
            prompt += " "

        while True:
            value = input(prompt)

            if value:
                if choices:
                    if force:
                        if value not in choices:
                            print(f"Invalid choice: {value}")
                            continue
                return value
            if default is not None:
                if default == Inputer.Empty:
                    return None
                return default
            print(f'Invalid input: "{value}"')

    @staticmethod
    def input_bool(prompt: str, default: bool = None, force: bool = False) -> bool:
        """
        Input a boolean value from the user

        :param prompt: The prompt to display to the user
        :type prompt: str

        :param default: The default value to use if the user does not input anything
        :type default: bool

        :param force: Force the user to input a value that exist in choices
        :type force: bool

        :return: The value the user input
        :rtype: bool
        """

        choices = ["y", "n"]
        if default is not None:
            choices.append(default)
        value = Inputer.input(prompt, choices=choices, force=force)
        if value == "y":
            return True
        if value == "n":
            return False
        return default

    @staticmethod
    def input_int(prompt: str, default: int = None, force: bool = False) -> Optional[int]:
        """
        Input an integer value from the user

        :param prompt: The prompt to display to the user
        :type prompt: str

        :param default: The default value to use if the user does not input anything
        :type default: int

        :param force: Force the user to input a value that exist in choices
        :type force: bool

        :return: The value the user input
        :rtype: Optional[int]
        """

        while True:
            value = Inputer.input(prompt, default=default, force=force)
            if value is Inputer.Empty:
                return None
            try:
                return int(value)
            except (ValueError, TypeError):
                print("Invalid input")

    @staticmethod
    def input_float(prompt: str, default: float = None, force: bool = False) -> float:
        """
        Input a float value from the user
        
        :param prompt: The prompt to display to the user
        :type prompt: str
        
        :param default: The default value to use if the user does not input anything
        :type default: float
        
        :param force: Force the user to input a value that exist in choices
        :type force: bool

        :return: The value the user input
        :rtype: float
        """

        while True:
            value = Inputer.input(prompt, default=default, force=force)
            try:
                return float(value)
            except ValueError:
                print("Invalid input")

    @staticmethod
    def input_list(prompt: str, default: List[str] = None, force: bool = False) -> List[str]:
        """
        Input a list of values from the user

        :param prompt: The prompt to display to the user
        :type prompt: str

        :param default: The default value to use if the user does not input anything
        :type default: List[str]

        :param force: Force the user to input a value that exist in choices
        :type force: bool

        :return: The value the user input
        :rtype: List[str]
        """

        if default is None:
            default = []
        value = Inputer.input(prompt, default=",".join(default), force=force)
        return value.split(",")

    @staticmethod
    def input_dict(prompt: str, default: Dict[str, str] = None, force: bool = False) -> Dict[str, str]:
        """
        Input a dictionary of values from the user

        :param prompt: The prompt to display to the user
        :type prompt: str

        :param default: The default value to use if the user does not input anything
        :type default: Dict[str, str]

        :param force: Force the user to input a value that exist in choices
        :type force: bool

        :return: The value the user input
        :rtype: Dict[str, str]
        """

        if default is None:
            default = {}
        value = Inputer.input(
            prompt,
            default=",".join(f"{key}={value}" for key, value in default.items()),
            force=force
        )
        return {key: value for key, value in (item.split("=") for item in value.split(","))}

    @staticmethod
    def input_choice(prompt: str, choices: List[Any], default: Any = None, force: bool = False) -> Any:
        """
        Input a choice from the user

        :param prompt: The prompt to display to the user
        :type prompt: str

        :param choices: The choices to display to the user
        :type choices: List[Any]

        :param default: The default value to use if the user does not input anything
        :type default: Any

        :param force: Force the user to input a value that exist in choices
        :type force: bool

        :return: The value the user input
        :rtype: Any
        """

        if default is not None:
            choices.append(default)
        value = Inputer.input(prompt, choices=choices, force=force)
        if value in choices:
            return value
        return default

    @staticmethod
    def input_choice_bool(prompt: str, choices: List[bool], default: bool = None, force: bool = False) -> bool:
        """
        Input a choice from the user

        :param prompt: The prompt to display to the user
        :type prompt: str

        :param choices: The choices to display to the user
        :type choices: List[bool]

        :param default: The default value to use if the user does not input anything
        :type default: bool

        :param force: Force the user to input a value that exist in choices
        :type force: bool

        :return: The value the user input
        :rtype: bool
        """

        if default is not None:
            choices.append(default)
        value = Inputer.input(prompt, choices=choices, force=force)
        if value in choices:
            return value
        return default
