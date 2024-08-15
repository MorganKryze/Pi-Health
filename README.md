# Pi-Health

> Lightweight health monitoring websocket server for Raspberry Pi (CPU % and °C, RAM %).

![screenshot](./assets/img/screenshot.png)

## Getting Started

### Introduction

This project is a lightweight health monitoring websocket server for Raspberry Pi. It provides the CPU usage in percentage and temperature in Celsius degrees, as well as the RAM usage in percentage through websocket channels.

### Prerequisites

- Raspberry Pi (tested on zero/3/4/5)
- Network connectivity
- `git` installed
- `docker` & `docker compose` installed

### Install

First, we clone the project locally using `git`:

```bash
git clone --depth=1 https://github.com/MorganKryze/Pi-Health.git
```

> [!NOTE]
> The `--depth=1` option is used to clone only the last commit of the repository, which is useful to save time and space.

Move to the project directory:

```bash
cd Pi-Health
```

Open the `.env` file using an editor (`nano`, `vim`, ...) and set the `PORT` variable to the desired exposed port (default is `9876`).

Then, we can pull the docker image the project using `docker compose`:

```bash
docker compose pull
```

When the image is pulled, we can build the project using `docker compose`:

```bash
docker compose up -d
```

> [!TIP]
> The `-d` option is used to run the container in the background (detached mode).

### Usage

Once the container is running, you can connect using a websocket client to the server with the following URL:

```bash
ws://<raspberry-pi-ip>:<port>/general/debug
```

> [!NOTE]
> You may want to access these information from a remote machine, so you will need to use an NGINX reverse proxy or a Cloudflare tunnel (for example) to expose the service to the internet.

The available channels are:

- `general/debug`: simple incrementing debug channel
- `sensor/cpu_usage`: CPU usage in percentage
- `sensor/cpu_temp`: CPU temperature in Celsius degrees
- `sensor/ram_usage`: RAM usage in percentage

## Supported platforms

Built for arm Linux machines (Raspberry Pi). Will only need to change the functions that get the CPU and RAM usage to work on other platforms.

## Future improvements

- Add disk space usage
- Add network connection status
- Add a web interface to display the data

## Contributing

If you want to contribute to the project, you can follow the steps described in the [CONTRIBUTING](CONTRIBUTING) file.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details.
