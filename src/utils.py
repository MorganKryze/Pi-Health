from typing import List, Callable, Any
from functools import wraps
from halo import Halo
import time
import os


class Utils:
    """
    A utility class providing methods for unwrapping messages, demonstrating loading spinners,
    applying loading decorators, getting Wi-Fi information, reading environment variables,
    and listing spinner types.
    """

    def clear_console() -> None:
        """
        Clears the console screen.

        This function uses the 'clear' command on Unix/Linux/Mac systems to clear the console screen.
        """
        os.system("clear")

    def loadings_demo(delay: int = 3) -> None:
        """
        Demonstrates various loading spinners with a dummy job.

        Args:
            delay (int): The delay in seconds for the dummy job. Defaults to 3.
        """

        def dummy_job() -> None:
            time.sleep(delay)

        for spinner_type in Utils.spinner_types:
            spinner = Halo(text=f"Loading using: {spinner_type}", spinner=spinner_type)
            spinner.start()
            dummy_job()
            spinner.stop()

    def loading(
        loading_message: str = "Loading...",
        success_message: str = "Loading complete.",
        failure_message: str = "Loading failed.",
        startup_time: float = 0.75,
        spinner_type: str = "line",
    ) -> Callable:
        """
        A decorator for adding a loading spinner to functions.

        Args:
            loading_message (str): The message displayed while loading.
            success_message (str): The message displayed on success.
            failure_message (str): The message displayed on failure.
            startup_time (float): The startup time before the function execution.
            spinner_type (str): The type of spinner to use.

        Returns:
            Callable: The decorated function.
        """

        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                spinner = Halo(text=loading_message, spinner=spinner_type)
                spinner.start()
                time.sleep(startup_time)
                try:
                    result = func(*args, **kwargs)
                    spinner.succeed(success_message) if result == 0 else spinner.fail(
                        failure_message
                    )
                    return result
                except Exception as e:
                    spinner.fail(str(e))

            return wrapper

        return decorator

    def read_variable(var_name: str) -> str:
        """
        Reads an environment variable.

        Args:
            var_name (str): The name of the environment variable.

        Returns:
            str: The value of the environment variable or None if not found.
        """
        return os.environ.get(var_name)

    spinner_types: List[str] = [
        "dots",
        "dots2",
        "dots3",
        "dots4",
        "dots5",
        "line",
        "line2",
        "pipe",
        "star",
        "star2",
        "flip",
        "hamburger",
        "growVertical",
        "growHorizontal",
        "squareCorners",
        "circleHalves",
        "balloon",
        "balloon2",
        "noise",
        "bounce",
        "boxBounce",
        "boxBounce2",
        "triangle",
        "arc",
        "circle",
        "circleCorners",
        "bouncingBar",
        "bouncingBall",
        "earth",
        "moon",
        "pong",
        "shark",
        "dqpb",
    ]
    """
    A list of spinner types supported by the Halo library.
    """
