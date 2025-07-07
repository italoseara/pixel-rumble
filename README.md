# Pixel Rumble

A 2d platformer game built using a custom Pygame game engine. This engine provides a flexible and modular architecture for creating games with Pygame, featuring components for physics, rendering, UI, and more.

> [!NOTE]
> Clique [aqui](README.pt-br.md) para a versão em ![Brazil](https://raw.githubusercontent.com/stevenrskelton/flag-icon/master/png/16/country-4x3/br.png "Brazil") Português.

## Protocol

The game uses a custom protocol for network communication, which is defined in the `packets` module. The protocol includes various packet types for different game events and states.

1. [Packet Format](#packet-format)
2. [Status](#status)
   - [Client](#client)
     - [Ping](#ping)
   - [Server](#server)
     - [Pong](#pong)

## Packet Format

The packet format is a binary structure that includes a header and a payload. The header contains the packet type and length, while the payload contains the actual data.

| Name      | Type    | Description                                                                |
| --------- | ------- | -------------------------------------------------------------------------- |
| Packet ID | `uint8` | The id of the packet.                                                      |
| Data      | `bytes` | The data payload of the packet. It will vary depending on the packet type. |

## Status

The status is used to check if there is a game server running on this address. The client can send a [ping](#ping) packet to the port `3567` to check if the server is available. The server will respond with a [pong](#pong) packet if it is running.

### Client

#### Ping

| Packet ID | State    | Bound To | Field Name  | Field Type | Description |
| --------- | -------- | -------- | ----------- | ---------- | ----------- |
| `0x00`    | `Status` | `Client` | _No fields_ |            |             |

### Server

#### Pong

| Packet ID | State    | Bound To | Field Name | Field Type | Description                                                    |
| --------- | -------- | -------- | ---------- | ---------- | -------------------------------------------------------------- |
| `0x01`    | `Status` | `Client` | IP Adress  | `string`   | The IP address and port of the server in the format `ip:port`. |
