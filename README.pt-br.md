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

## Formato do Pacote

O formato do pacote é uma estrutura binária que inclui um cabeçalho e um payload. O cabeçalho contém o tipo e o tamanho do pacote, enquanto o payload contém os dados propriamente ditos.

| Nome         | Tipo    | Descrição                                                           |
| ------------ | ------- | ------------------------------------------------------------------- |
| ID do Pacote | `uint8` | O id do pacote.                                                     |
| Dados        | `bytes` | O payload de dados do pacote. Varia de acordo com o tipo do pacote. |

## Status

O status é usado para verificar se há um servidor de jogo rodando neste endereço. O cliente pode enviar um pacote [ping](#ping) para a porta `3567` para checar se o servidor está disponível. O servidor responderá com um pacote [pong](#pong) se estiver rodando.

### Cliente

#### Ping

| ID do Pacote | Estado   | Destino   | Nome do Campo | Tipo do Campo | Descrição |
| ------------ | -------- | --------- | ------------- | ------------- | --------- |
| `0x00`       | `Status` | `Cliente` | _Sem campos_  |               |           |

### Servidor

#### Pong

| ID do Pacote | Estado   | Destino   | Nome do Campo | Tipo do Campo | Descrição                                                |
| ------------ | -------- | --------- | ------------- | ------------- | -------------------------------------------------------- |
| `0x01`       | `Status` | `Cliente` | Endereço IP   | `string`      | O endereço IP e porta do servidor no formato `ip:porta`. |
