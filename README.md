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
3. [Play](#play)
   - [Client](#client-1)
     - [Join](#join)
     - [Disconnect](#disconnect)
   - [Server](#server-1)
     - [Welcome](#welcome)

## Packet Format

The packet format is a binary structure that includes a header and a payload. The header contains the packet type and length, while the payload contains the actual data.

| Name      | Type    | Description                                                                |
| --------- | ------- | -------------------------------------------------------------------------- |
| Packet ID | `uint8` | The id of the packet.                                                      |
| Data      | `bytes` | The data payload of the packet. It will vary depending on the packet type. |

## Status

The status is used to check if there is a game server running on this address. The client can send a [ping](#ping) packet to the port `1337` to check if the server is available. The server will respond with a [pong](#pong) packet if it is running.

### Client

#### Ping

| Packet ID | State    | Bound To | Field Name  | Field Type | Description |
| --------- | -------- | -------- | ----------- | ---------- | ----------- |
| `0x00`    | `Status` | `Server` | _No fields_ |            |             |

### Server

#### Pong

<table>
  <thead>
    <tr>
      <th>Packet ID</th>
      <th>State</th>
      <th>Bound To</th>
      <th>Field Name</th>
      <th>Field Type</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td rowspan="3"><code>0x01</code></td>
      <td rowspan="3"><code>Play</code></td>
      <td rowspan="3"><code>Client</code></td>
      <td>Name</td>
      <td><code>string</code></td>
      <td>The Name of the server.</td>
    </tr>
    <tr>
      <td>IP Adress</td>
      <td><code>string</code></td>
      <td>The IP address of the server.</td>
    </tr>
    <tr>
      <td>Port</td>
      <td><code>uint16</code></td>
      <td>The port of the server.</td>
    </tr>
  </tbody>
</table>


## Play

The play state is used during the game. It includes packets for player actions, game state updates, and other gameplay-related events.

### Client

#### Join

| Packet ID | State  | Bound To | Field Name | Field Type | Description                              |
| --------- | ------ | -------- | ---------- | ---------- | ---------------------------------------- |
| `0x02`    | `Play` | `Server` | Name       | `string`   | The name of the player joining the game. |

#### Disconnect

| Packet ID | State  | Bound To | Field Name  | Field Type | Description                                               |
| --------- | ------ | -------- | ----------- | ---------- | --------------------------------------------------------- |
| `0x04`    | `Play` | `Server` | _No fields_ |            | Indicates that the player is disconnecting from the game. |

### Server

#### Welcome

<table>
  <thead>
    <tr>
      <th>Packet ID</th>
      <th>State</th>
      <th>Bound To</th>
      <th>Field Name</th>
      <th>Field Type</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td rowspan="2"><code>0x03</code></td>
      <td rowspan="2"><code>Play</code></td>
      <td rowspan="2"><code>Client</code></td>
      <td>Is Welcome</td>
      <td><code>boolean</code></td>
      <td>Indicates if the player is welcome to join the game.</td>
    </tr>
    <tr>
      <td>Message</td>
      <td><code>string</code></td>
      <td>An error message if the player is not welcome.</td>
    </tr>
  </tbody>
</table>
