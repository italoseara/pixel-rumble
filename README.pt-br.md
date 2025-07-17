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
     - [Manter Vivo](#manter-vivo)
     - [Entrar](#entrar)
     - [Desconectar](#desconectar)
     - [Mover Jogador](#mover-jogador)
   - [Servidor](#servidor-1)
     - [Manter Vivo](#manter-vivo-1)
     - [Boas-vindas](#boas-vindas)
     - [Mover Jogador](#mover-jogador-1)
     - [Jogador Entrou](#jogador-entrou)

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
      <td rowspan="3"><code>0x01</code></td>
      <td rowspan="3"><code>Jogar</code></td>
      <td rowspan="3"><code>Cliente</code></td>
      <td>Nome</td>
      <td><code>string</code></td>
      <td>O nome do servidor.</td>
    </tr>
    <tr>
      <td>Endereço IP</td>
      <td><code>string</code></td>
      <td>O endereço IP do servidor.</td>
    </tr>
    <tr>
      <td>Porta</td>
      <td><code>uint32</code></td>
      <td>A porta do servidor.</td>
    </tr>
  </tbody>
</table>

## Jogar

O estado "Jogar" é utilizado durante a partida. Inclui pacotes para ações dos jogadores, atualizações do estado do jogo e outros eventos relacionados à jogabilidade.

### Cliente

#### Manter Vivo

| ID do Pacote | Estado  | Destino    | Nome do Campo | Tipo do Campo | Descrição                                                                                   |
| ------------ | ------- | ---------- | ------------- | ------------- | ------------------------------------------------------------------------------------------- |
| `0x05`       | `Jogar` | `Servidor` | Valor         | `uint32`      | Um valor esperado para ser retornado pelo cliente, verificando se ele ainda está conectado. |

#### Entrar

| ID do Pacote | Estado  | Destino    | Nome do Campo | Tipo do Campo | Descrição                                    |
| ------------ | ------- | ---------- | ------------- | ------------- | -------------------------------------------- |
| `0x02`       | `Jogar` | `Servidor` | Nome          | `string`      | O nome do jogador que está entrando no jogo. |

#### Desconectar

| ID do Pacote | Estado  | Destino    | Nome do Campo | Tipo do Campo | Descrição                                           |
| ------------ | ------- | ---------- | ------------- | ------------- | --------------------------------------------------- |
| `0x04`       | `Jogar` | `Servidor` | _Sem campos_  |               | Indica que o jogador está se desconectando do jogo. |

#### Mover Jogador

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
      <td rowspan="4"><code>0x09</code></td>
      <td rowspan="4"><code>Jogar</code></td>
      <td rowspan="4"><code>Servidor</code></td>
      <td>ID do Jogador</td>
      <td><code>uint32</code></td>
      <td>O ID do jogador que está se movendo.</td>
    </tr>
    <tr>
      <td>Posição</td>
      <td><code>float[2]</code></td>
      <td>A nova posição do jogador no mundo do jogo.</td>
    </tr>
    <tr>
      <td>Aceleração</td>
      <td><code>float[2]</code></td>
      <td>O vetor de aceleração do jogador.</td>
    </tr>
    <tr>
      <td>Velocidade</td>
      <td><code>float[2]</code></td>
      <td>O vetor de velocidade do jogador.</td>
    </tr>
  </tbody>
</table>

### Servidor

#### Manter Vivo

| ID do Pacote | Estado  | Destino   | Nome do Campo | Tipo do Campo | Descrição                                                                                                                   |
| ------------ | ------- | --------- | ------------- | ------------- | --------------------------------------------------------------------------------------------------------------------------- |
| `0x06`       | `Jogar` | `Cliente` | Valor         | `uint32`      | Um valor enviado pelo servidor ao cliente para verificar se ele está conectado. O cliente deve responder com o mesmo valor. |

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
      <td rowspan="3"><code>0x03</code></td>
      <td rowspan="3"><code>Jogar</code></td>
      <td rowspan="3"><code>Cliente</code></td>
      <td>É Bem-Vindo</td>
      <td><code>boolean</code></td>
      <td>Indica se o jogador é bem-vindo para entrar no jogo.</td>
    </tr>
    <tr>
      <td>ID do Jogador</td>
      <td><code>uint32</code></td>
      <td>O ID do jogador, se ele for bem-vindo. Se não, será `0`.</td>
    </tr>
    <tr>
      <td>Mensagem</td>
      <td><code>string</code></td>
      <td>Uma mensagem de erro no caso do jogador não ser bem-vindo.</td>
    </tr>
  </tbody>
</table>

#### Mover Jogador

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
      <td rowspan="4"><code>0x08</code></td>
      <td rowspan="4"><code>Jogar</code></td>
      <td rowspan="4"><code>Cliente</code></td>
      <td>ID do Jogador</td>
      <td><code>uint32</code></td>
      <td>O ID do jogador que está se movendo.</td>
    </tr>
    <tr>
      <td>Posição</td>
      <td><code>float[2]</code></td>
      <td>A nova posição do jogador no mundo do jogo.</td>
    </tr>
    <tr>
      <td>Aceleração</td>
      <td><code>float[2]</code></td>
      <td>O vetor de aceleração do jogador.</td>
    </tr>
    <tr>
      <td>Velocidade</td>
      <td><code>float[2]</code></td>
      <td>O vetor de velocidade do jogador.</td>
    </tr>
  </tbody>
</table>

#### Jogador Entrou

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
      <td rowspan="2"><code>0x07</code></td>
      <td rowspan="2"><code>Jogar</code></td>
      <td rowspan="2"><code>Cliente</code></td>
      <td>ID do Jogador</td>
      <td><code>uint32</code></td>
      <td>O ID do jogador que entrou.</td>
    </tr>
    <tr>
      <td>Nome</td>
      <td><code>string</code></td>
      <td>O apelido do jogador que entrou.</td>
    </tr>
  </tbody>
</table>
