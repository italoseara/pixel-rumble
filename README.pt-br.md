# Pixel Rumble

Um jogo de plataforma 2D construído com um motor de jogo customizado em Pygame. Este motor oferece uma arquitetura flexível e modular para criar jogos com Pygame, incluindo componentes para física, renderização, UI e mais.

> [!NOTE]
> Click [here](README.md) For the ![Estados Unidos](https://raw.githubusercontent.com/stevenrskelton/flag-icon/master/png/16/country-4x3/us.png "United States") English version.

## Protocolo

O jogo utiliza um protocolo customizado para comunicação em rede, definido no módulo `packets`. O protocolo inclui vários tipos de pacotes para diferentes eventos e estados do jogo.

1. [Formato do Pacote](#formato-do-pacote)
2. [Status](#status)
   - [Cliente](#cliente)
     - [Ping](#ping)
   - [Servidor](#servidor)
     - [Pong](#pong)
3. [Jogar](#jogar)
   - [Cliente](#cliente-1)
     - [Entrar](#entrar)
   - [Servidor](#servidor-1)
     - [Boas-vindas](#boas-vindas)

## Formato do Pacote

O formato do pacote é uma estrutura binária que inclui um cabeçalho e um payload. O cabeçalho contém o tipo e o tamanho do pacote, enquanto o payload contém os dados propriamente ditos.

| Nome         | Tipo    | Descrição                                                           |
| ------------ | ------- | ------------------------------------------------------------------- |
| ID do Pacote | `uint8` | O id do pacote.                                                     |
| Dados        | `bytes` | O payload de dados do pacote. Varia de acordo com o tipo do pacote. |

## Status

O status é usado para verificar se há um servidor de jogo rodando neste endereço. O cliente pode enviar um pacote [ping](#ping) para a porta `1337` para checar se o servidor está disponível. O servidor responderá com um pacote [pong](#pong) se estiver rodando.

### Cliente

#### Ping

| ID do Pacote | Estado   | Destino    | Nome do Campo | Tipo do Campo | Descrição |
| ------------ | -------- | ---------- | ------------- | ------------- | --------- |
| `0x00`       | `Status` | `Servidor` | _Sem campos_  |               |           |

### Servidor

#### Pong

| ID do Pacote | Estado   | Destino   | Nome do Campo | Tipo do Campo | Descrição                                                |
| ------------ | -------- | --------- | ------------- | ------------- | -------------------------------------------------------- |
| `0x01`       | `Status` | `Cliente` | Endereço IP   | `string`      | O endereço IP e porta do servidor no formato `ip:porta`. |

## Jogar

O estado "Jogar" é utilizado durante a partida. Inclui pacotes para ações dos jogadores, atualizações do estado do jogo e outros eventos relacionados à jogabilidade.

### Cliente

#### Entrar

| ID do Pacote | Estado  | Destino    | Nome do Campo | Tipo do Campo | Descrição                                    |
| ------------ | ------- | ---------- | ------------- | ------------- | -------------------------------------------- |
| `0x02`       | `Jogar` | `Servidor` | Nome          | `string`      | O nome do jogador que está entrando no jogo. |

### Servidor

#### Boas-vindas

<table>
  <thead>
    <tr>
      <th>ID do Pacote</th>
      <th>Estado</th>
      <th>Destino</th>
      <th>Nome do Campo</th>
      <th>Tipo do Campo</th>
      <th>Descrição</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td rowspan="2"><code>0x03</code></td>
      <td rowspan="2"><code>Play</code></td>
      <td rowspan="2"><code>Cliente</code></td>
      <td>É Bem-Vindo</td>
      <td><code>boolean</code></td>
      <td>Indica se o jogador é bem-vindo para entrar no jogo.</td>
    </tr>
    <tr>
      <td>Mensagem</td>
      <td><code>string</code></td>
      <td>Uma mensagem de erro no caso do jogador não ser bem-vindo.</td>
    </tr>
  </tbody>
</table>
