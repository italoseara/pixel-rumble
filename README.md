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
     - [Keep Alive](#keep-alive)
     - [Join](#join)
     - [Disconnect](#disconnect)
     - [Player Move](#player-move)
     - [Change Character](#change-character)
     - [Start Game](#start-game)
   - [Server](#server-1)
     - [Keep Alive](#keep-alive-1)
     - [Welcome](#welcome)
     - [Player Move](#player-move)
     - [Player Join](#player-join)
     - [Player Leave](#player-leave)
     - [Change Character](#change-character-1)
     - [Start Game](#start-game-1)

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
      <td><code>uint32</code></td>
      <td>The port of the server.</td>
    </tr>
  </tbody>
</table>

## Play

The play state is used during the game. It includes packets for player actions, game state updates, and other gameplay-related events.

### Client

#### Keep Alive

| Packet ID | State  | Bound To | Field Name | Field Type | Description                                                                              |
| --------- | ------ | -------- | ---------- | ---------- | ---------------------------------------------------------------------------------------- |
| `0x05`    | `Play` | `Server` | Value      | `uint32`   | A value expected to be returned by the client to check if the client is still connected. |

#### Join

| Packet ID | State  | Bound To | Field Name | Field Type | Description                              |
| --------- | ------ | -------- | ---------- | ---------- | ---------------------------------------- |
| `0x02`    | `Play` | `Server` | Name       | `string`   | The name of the player joining the game. |

#### Disconnect

| Packet ID | State  | Bound To | Field Name  | Field Type | Description                                               |
| --------- | ------ | -------- | ----------- | ---------- | --------------------------------------------------------- |
| `0x04`    | `Play` | `Server` | _No fields_ |            | Indicates that the player is disconnecting from the game. |

#### Player Move

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
      <td rowspan="4"><code>0x09</code></td>
      <td rowspan="4"><code>Play</code></td>
      <td rowspan="4"><code>Server</code></td>
      <td>Player ID</td>
      <td><code>uint32</code></td>
      <td>The ID of the player moving.</td>
    </tr>
    <tr>
      <td>Position</td>
      <td><code>float[2]</code></td>
      <td>The new position of the player in the game world.</td>
    </tr>
    <tr>
      <td>Acceleration</td>
      <td><code>float[2]</code></td>
      <td>The acceleration vector of the player.</td>
    </tr>
    <tr>
      <td>Velocity</td>
      <td><code>float[2]</code></td>
      <td>The velocity vector of the player.</td>
    </tr>
  </tbody>
</table>

#### Change Character

| Packet ID | State  | Bound To | Field Name | Field Type | Description                                  |
| --------- | ------ | -------- | ---------- | ---------- | -------------------------------------------- |
| `0x0B`    | `Play` | `Server` | Index      | `uint8`    | The index of the character being changed to. |

#### Start Game

| Packet ID | State  | Bound To | Field Name | Field Type | Description                               |
| --------- | ------ | -------- | ---------- | ---------- | ----------------------------------------- |
| `0x0D`    | `Play` | `Server` | Map Name   | `string`   | The name of the map to start the game on. |

### Server

#### Keep Alive

| Packet ID | State  | Bound To | Field Name | Field Type | Description                                                                                                                                            |
| --------- | ------ | -------- | ---------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `0x06`    | `Play` | `Client` | Value      | `uint32`   | A value sent by the server to the client to check if the client is still connected. The client should respond with a packet containing the same value. |

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
      <td rowspan="3"><code>0x03</code></td>
      <td rowspan="3"><code>Play</code></td>
      <td rowspan="3"><code>Client</code></td>
      <td>Is Welcome</td>
      <td><code>boolean</code></td>
      <td>Indicates if the player is welcome to join the game.</td>
    </tr>
    <tr>
      <td>Player ID</td>
      <td><code>uint32</code></td>
      <td>The ID of the player if they are welcome. If not, this will be `0`.</td>
    </tr>
    <tr>
      <td>Message</td>
      <td><code>string</code></td>
      <td>An error message if the player is not welcome.</td>
    </tr>
  </tbody>
</table>

#### Player Move

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
      <td rowspan="4"><code>0x08</code></td>
      <td rowspan="4"><code>Play</code></td>
      <td rowspan="4"><code>Client</code></td>
      <td>Player ID</td>
      <td><code>uint32</code></td>
      <td>The ID of the player moving.</td>
    </tr>
    <tr>
      <td>Position</td>
      <td><code>float[2]</code></td>
      <td>The new position of the player in the game world.</td>
    </tr>
    <tr>
      <td>Acceleration</td>
      <td><code>float[2]</code></td>
      <td>The acceleration vector of the player.</td>
    </tr>
    <tr>
      <td>Velocity</td>
      <td><code>float[2]</code></td>
      <td>The velocity vector of the player.</td>
    </tr>
  </tbody>
</table>

#### Player Join

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
      <td rowspan="2"><code>0x07</code></td>
      <td rowspan="2"><code>Play</code></td>
      <td rowspan="2"><code>Client</code></td>
      <td>Player ID</td>
      <td><code>uint32</code></td>
      <td>The joining player's ID.</td>
    </tr>
    <tr>
      <td>Name</td>
      <td><code>string</code></td>
      <td>The joining player's nickname.</td>
    </tr>
  </tbody>
</table>

#### Player Leave

| Packet ID | State  | Bound To | Field Name | Field Type | Description                            |
| --------- | ------ | -------- | ---------- | ---------- | -------------------------------------- |
| `0x0A`    | `Play` | `Client` | Player ID  | `uint32`   | The ID of the player leaving the game. |

#### Change Character

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
      <td rowspan="2"><code>0x0C</code></td>
      <td rowspan="2"><code>Play</code></td>
      <td rowspan="2"><code>Client</code></td>
      <td>Player ID</td>
      <td><code>uint32</code></td>
      <td>The ID of the player changing character.</td>
    </tr>
    <tr>
      <td>Index</td>
      <td><code>uint8</code></td>
      <td>The index of the character being changed to.</td>
    </tr>
  </tbody>
</table>

#### Start Game

| Packet ID | State  | Bound To | Field Name | Field Type | Description                               |
| --------- | ------ | -------- | ---------- | ---------- | ----------------------------------------- |
| `0x0E`    | `Play` | `Client` | Map Name   | `string`   | The name of the map to start the game on. |
