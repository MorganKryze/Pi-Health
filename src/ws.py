from typing import Callable, Coroutine
from fastapi import WebSocket
from dotenv import load_dotenv
from functools import wraps
import asyncio
import psutil
import os

from . import main
from .utils import Utils


@Utils.loading(
    "Loading environment variables...",
    "Environment variables loaded successfully.",
    "Failed to load environment variables.",
)
def load_variables(docker_path: str = "../config/.env") -> int:
    """
    Loads environment variables from a specified path.

    Args:
        docker_path (str): The path to the .env file. Defaults to "../config/.env".

    Returns:
        int: 0 if environment variables were loaded successfully, 1 otherwise.
    """
    return 0 if load_dotenv() or load_dotenv(docker_path) else 1


class Websockets:
    Utils.clear_console()
    if load_variables() != 0:
        exit(1)

    @Utils.loading(
        "(General) Initializing Websockets...",
        "(General) Websockets initialized successfully.",
        "(General) Failed to initialize Websockets.",
    )
    def init_ws_general() -> int:
        """
        Initializes general WebSocket services.

        Returns:
            int: 0 if initialization was successful, 1 otherwise.
        """
        try:
            Websockets.setup_websocket_service(
                "general",
                "debug",
                Websockets.ws_debug,
            )

            return 0
        except Exception:
            return 1

    @Utils.loading(
        "(Internal Sensor) Initializing Websockets...",
        "(Internal Sensor) Websockets initialized successfully.",
        "(Internal Sensor) Failed to initialize Websockets.",
    )
    def init_ws_internal_sensor() -> int:
        """
        Initializes internal sensor WebSocket services.

        Returns:
            int: 0 if initialization was successful, 1 otherwise.
        """
        try:
            Websockets.setup_websocket_service(
                "internal_sensor",
                "CPU_temperature",
                Websockets.ws_internal_cpu_temperature,
            )
            Websockets.setup_websocket_service(
                "internal_sensor",
                "CPU_usage",
                Websockets.ws_internal_cpu_usage,
            )
            Websockets.setup_websocket_service(
                "internal_sensor",
                "RAM_usage",
                Websockets.ws_internal_ram_usage,
            )

            return 0
        except Exception:
            return 1

    def setup_websocket_service(
        ws_category: str,
        ws_name: str,
        func: Callable[[WebSocket], Coroutine[None, None, None]],
    ):
        """
        Sets up a WebSocket service by decorating the given function with the WebSocket route.

        Args:
            ws_category (str): The category of the WebSocket service.
            ws_name (str): The name of the WebSocket service.
            func (Callable[[WebSocket], Coroutine[None, None, None]]): The async function to be called when the WebSocket is accessed.
        """

        @main.app.websocket(f"/{ws_category}/{ws_name}")
        @wraps(func)
        async def wrapper(websocket: WebSocket):
            await websocket.accept()
            try:
                if main.services_status[ws_category][ws_name]:
                    raise Exception("Service already running.")
                else:
                    main.services_status[ws_category][ws_name] = True
                await func(websocket)
            except Exception:
                main.services_status[ws_category][ws_name] = False
                await websocket.send_text("[WebSocket Closed]")
            finally:
                main.services_status[ws_category][ws_name] = False
                await websocket.send_text("[WebSocket Closed]")

        return wrapper

    async def ws_debug(websocket: WebSocket):
        """
        A WebSocket endpoint for debugging purposes. Sends an incrementing count every second.

        Args:
            websocket (WebSocket): The WebSocket connection instance.
        """
        count = 0
        while True:
            await websocket.send_text(str(count))
            count += 1
            await asyncio.sleep(1)

    async def ws_internal_cpu_temperature(websocket: WebSocket, delay: int = 1):
        """
        A WebSocket endpoint for internal CPU temperature data. Placeholder for actual data retrieval.

        Args:
            websocket (WebSocket): The WebSocket connection instance.
            delay (int): The delay between data sends. Defaults to 1 second.
        """
        while True:
            # TODO: try on Rpi
            cpu_temp = os.popen("vcgencmd measure_temp").readline()
            cpu_temp_float = float(cpu_temp.replace("temp=", "").replace("'C\n", ""))
            await websocket.send_text(str(round(cpu_temp_float, 2)))
            await asyncio.sleep(delay)

    async def ws_internal_cpu_usage(websocket: WebSocket, delay: int = 1):
        """
        A WebSocket endpoint for internal CPU usage data. Placeholder for actual data retrieval.

        Args:
            websocket (WebSocket): The WebSocket connection instance.
            delay (int): The delay between data sends. Defaults to 1 second.
        """
        while True:
            # TODO: try on Rpi
            await websocket.send_text(str(round(psutil.cpu_percent(interval=1), 2)))
            await asyncio.sleep(delay)

    async def ws_internal_ram_usage(websocket: WebSocket, delay: int = 1):
        """
        A WebSocket endpoint for internal RAM usage data. Placeholder for actual data retrieval.

        Args:
            websocket (WebSocket): The WebSocket connection instance.
            delay (int): The delay between data sends. Defaults to 1 second.
        """
        while True:
            # TODO: try on Rpi
            await websocket.send_text(str(round(psutil.virtual_memory().percent, 2)))
            await asyncio.sleep(delay)
