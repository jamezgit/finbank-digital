# PROJETO 02 — FINBANK DIGITAL: INFRAESTRUTURA E MONITORAMENTO DE REDE

---

# TÓPICO 1: DOCUMENTAÇÃO TÉCNICA

---

## 1.1 Identificação do Projeto e Integrantes

| Campo | Detalhamento |
| :--- | :--- |
| **Nome do Projeto** | FinBank Digital — Infraestrutura de Redes Corporativas e Sistema de Monitoramento de Disponibilidade |
| **Identificador / Código** | Projeto 02 |
| **Instituição de Ensino** | [Inserir Nome da Instituição de Ensino / Faculdade] |
| **Curso / Disciplina** | [Inserir Curso: ex. Redes de Computadores / Engenharia de Software / Ciência da Computação] |
| **Período / Ano** | 2026.2 |
| **Modelo Organizacional** | Segregação Corporativa em Duas Equipes de Trabalho Especializadas (Handover Técnico) |

### Equipes e Integrantes:

#### Grupo 01 — Infraestrutura de Rede, Cabeamento e Serviços Cisco
- **Responsabilidade:** Montagem física da topologia, dimensionamento de portas, segmentação de VLANs, roteamento Router-on-a-Stick (802.1Q), configuração de serviços (DHCP, DNS, HTTP, Syslog) no **Cisco Packet Tracer**, execução de testes de conectividade e geração do arquivo `.pkt` de entrega.
- **Integrantes:**
  - Jamerson Albuquerque — *Líder de Infraestrutura & Configuração Cisco IOS*
  - [Nome do Integrante 2 / Matrícula]
  - [Nome do Integrante 3 / Matrícula]
  - [Nome do Integrante 4 / Matrícula]

#### Grupo 02 — Lógica, Software de Monitoramento e Indicadores
- **Responsabilidade:** Desenvolvimento do software de monitoramento em **Python 3**, implementação dos requisitos funcionais (RF01 a RF06), coleta contínua de status via ICMP/Ping, algoritmo de detecção de indisponibilidade persistente (3 falhas consecutivas), cálculo percentual de Uptime e geração de relatórios de alarmes por criticidade.
- **Integrantes:**
  - [Nome do Integrante 1 / Matrícula]
  - [Nome do Integrante 2 / Matrícula]
  - [Nome do Integrante 3 / Matrícula]
  - [Nome do Integrante 4 / Matrícula]

---

## 1.2 Introdução e Contextualização do Cenário Empresarial

No cenário contemporâneo de instituições bancárias e fintechs, a estabilidade e a integridade da comunicação entre setores são pilares de sustentação do negócio. A **FinBank Digital** é uma organização do setor financeiro que combina serviços bancários digitais com uma estrutura física de agência para operações presenciais de alto valor e atendimento a correntistas.

A agência física da FinBank Digital opera com três macrosetores interdependentes:
1. **Setor de Atendimento ao Cliente (VLAN 10):** Responsável pela recepção física, consultas gerais, suporte a aplicativos de clientes e abertura de contas correntes. É um ambiente de tráfego comum de clientes internos, exigindo isolamento para não interferir nas transações financeiras.
2. **Setor de Operações Financeiras e Administração (VLAN 20):** Abrange os caixas executivos, gerência de agência e estações de tesouraria. Nesse setor trafegam dados financeiros altamente sigilosos, operações em tempo real e conciliações contábeis internas, o que demanda prioridade elevada de disponibilidade e rígido isolamento de rede.
3. **Setor de Servidores e Data Center Local (VLAN 30):** Aloja os servidores centrais da agência, como a aplicação de Home/Web Banking corporativo, serviços de resolução de nomes internos (DNS) e coletor de logs e auditoria operacional (Syslog).

Nesse ecossistema, os serviços dependem fundamentalmente da conectividade ininterrupta entre as estações de trabalho e os servidores internos. Uma falha de conectividade na estação de um caixa ou a inoperância do servidor de aplicação paralisa as atividades da agência, gerando filas, perdas financeiras e danos imediatos à reputação institucional.

---

## 1.3 Descrição do Problema Identificado

Historicamente, a FinBank Digital enfrentava sérios entraves de gestão em sua infraestrutura de tecnologia, sintetizados no seguinte problema empresarial central:

> *"Como acompanhar em tempo real a disponibilidade dos dispositivos de rede corporativa e diagnosticar interrupções que comprometam o funcionamento dos serviços financeiros simulados, diferenciando oscilações momentâneas de panes persistentes e priorizando o restabelecimento de ativos críticos?"*

As principais dores técnicas identificadas incluíam:
- **Rede Plana e Ausência de Segmentação:** Todas as máquinas e servidores compartilhavam um único domínio de broadcast, permitindo que falhas em estações de atendimento ou eventuais tempestades de pacotes degradassem o tráfego dos caixas operacionais e dos servidores.
- **Abordagem Reativa de Atendimento a Falhas:** A equipe de suporte de TI só tomava ciência de uma queda após a reclamação dos colaboradores da agência ou clientes, resultando em elevado Tempo Médio de Resposta (MTTR - *Mean Time To Repair*).
- **Inexistência de Alertas Prioritários por Criticidade:** O desligamento acidental de um computador de triagem gerava o mesmo nível de alarme que a indisponibilidade do roteador central ou do servidor web de transações.
- **Falsos Positivos e Ruídos Operacionais:** Perdas pontuais de pacotes decorrentes de congestionamento momentâneo (drops esporádicos) eram confundidas com panes estruturais de enlace, sobrecarregando os analistas de infraestrutura.
- **Falta de Indicadores de SLA/Disponibilidade:** A gestão de TI não dispunha de registros históricos estruturados que comprovassem o percentual de disponibilidade (Uptime) de cada ativo para fins de conformidade e auditoria.

---

## 1.4 Objetivo Geral e Objetivos Específicos

### Objetivo Geral
Projetar, homologar e simular uma infraestrutura de rede local corporativa robusta e segmentada para a **FinBank Digital** no software **Cisco Packet Tracer**, integrada a um sistema de software em **Python** voltado ao monitoramento ativo de disponibilidade, auditoria de falhas e priorização de alarmes conforme criticidade empresarial.

### Objetivos Específicos
1. **Modelar a Topologia de Rede:** Desenvolver o projeto físico e lógico de rede utilizando o padrão de arquitetura *Router-on-a-Stick* com encapsulamento IEEE 802.1Q entre um Switch Cisco Catalyst 2960 e um Roteador Cisco 1941.
2. **Segmentar em Redes Virtuais (VLANs):** Criar e isolar três domínios de broadcast distintos: VLAN 10 (Atendimento), VLAN 20 (Operações/Admin) e VLAN 30 (Servidores e Data Center).
3. **Automatizar Serviços de Rede:** Implantar servidores DHCP dedicados no próprio roteador Cisco para entrega automática de configurações IP aos clientes, implementar servidor HTTP institucional e resolução de nomes (DNS) para o domínio corporativo `finbank.local`.
4. **Construir o Sistema Lógico de Monitoramento:** Desenvolver em Python um sistema modular orientado a objetos em conformidade com os requisitos funcionais RF01 a RF06.
5. **Implantar a Regra de Falha Persistente:** Estabelecer uma lógica algorítmica de tolerância a ruídos que deflagra o alerta de indisponibilidade persistente exclusivamente após a constatação de 3 falhas consecutivas de verificação ICMP.
6. **Classificar e Priorizar por Matriz de Criticidade:** Definir níveis de impacto operacional (`CRÍTICO`, `ALTA` e `NORMAL`), garantindo que ativos vitais gerem alertas visuais destacados imediatamente.
7. **Calcular Indicadores de Uptime:** Desenvolver o cálculo matemático automatizado do percentual de disponibilidade ($\text{Uptime } \% = \frac{\text{sucessos}}{\text{total}} \times 100$) com base nos históricos preservados.
8. **Realizar Testes de Homologação e Simulação de Falhas:** Executar bateria completa de testes de conectividade (pings inter-VLAN, acesso HTTP, consultas DNS) e simular interrupções de cabo/porta para comprovar a eficácia do monitoramento.

---

## 1.5 Escopo da Solução Proposta

### Escopo Positivo (Itens Inclusos no Projeto)
- **Topologia de Infraestrutura Simulada:** Montagem, posicionamento e interligação de 1 Roteador (Cisco 1941), 1 Switch (Cisco 2960), 2 Servidores dedicados e 4 Estações de Trabalho clientes.
- **Cabeamento e Interfaces Físicas:** Especificação detalhada de portas FastEthernet e GigabitEthernet com cabeamento par trançado direto (*Copper Straight-Through*).
- **Configuração Completa do Cisco IOS:**
  - Criação das VLANs 10, 20 e 30;
  - Atribuição de portas de acesso (*access*) com recurso `spanning-tree portfast`;
  - Configuração do enlace tronco (*trunk*) IEEE 802.1Q na porta `Gig0/1` do switch;
  - Criação de subinterfaces lógicas (`Gig0/0.10`, `Gig0/0.20`, `Gig0/0.30`) no roteador para atuar como gateways de cada segmento;
  - Configuração de pools de DHCP dedicados por VLAN com exclusão prévia de IPs estáticos.
- **Serviços de Aplicação Simulados:** Ativação de serviço HTTP com página web interna, configuração de servidor DNS para resolução do endereço `finbank.local` e serviço Syslog.
- **Sistema de Monitoramento em Python:** Software com arquitetura orientada a objetos (classes `Dispositivo` e `MonitorFinBank`), permitindo cadastramento de ativos, verificações reais via ICMP Ping, modo simulado com injeção de panes, consultas históricas e exibição de relatórios percentuais.
- **Documentação e Handover:** Especificação de todos os parâmetros técnicos e entrega formal entre os dois grupos.

### Escopo Negativo (Não Incluso na Solução)
- Interconexão com a Internet externa ou provedores de telecomunicações WAN (o projeto é restrito à infraestrutura corporativa da agência local).
- Implementação de protocolos de roteamento dinâmico complexos (como BGP ou OSPF) ou alta disponibilidade de primeiro salto (HSRP/VRRP), visto que o roteamento inter-VLAN estático/direto supre a necessidade educacional e técnica proposta.
- Persistência de dados em banco de dados relacional externo (ex: MySQL/PostgreSQL); o armazenamento histórico no escopo educacional é mantido em memória e arquivos de log.
- Mecanismos de autenticação de porta física via 802.1X ou firewalls de borda dedicados.

---

## 1.6 Requisitos Funcionais e Não Funcionais

### Requisitos Funcionais (RF)

| Código | Nome do Requisito | Descrição Detalhada |
| :--- | :--- | :--- |
| **RF01** | Cadastramento de Dispositivos e Serviços | O sistema deve permitir o cadastro de dispositivos de rede, registrando identificador único (ID), nome do ativo, endereço IP, setor físico, serviço correspondente e nível de criticidade. |
| **RF02** | Registro de Verificações de Disponibilidade | A cada ciclo de teste, o sistema deve registrar a data e hora (timestamp), a identificação do equipamento e o resultado da conectividade (`SUCESSO` ou `FALHA`). |
| **RF03** | Consulta de Histórico por Equipamento | O sistema deve disponibilizar funcionalidade para consultar o histórico individual e sequencial de todas as verificações executadas em um equipamento específico. |
| **RF04** | Identificação de Falhas Consecutivas | O sistema deve monitorar em tempo de execução o número de falhas seguidas de cada ativo, destacando visualmente quando uma indisponibilidade se tornar persistente. |
| **RF05** | Cálculo da Disponibilidade Percentual (Uptime) | O sistema deve calcular matematicamente o índice percentual de disponibilidade de cada ativo com base na fórmula: $\text{Uptime } \% = \frac{\text{Total de Sucessos}}{\text{Total de Verificações Registradas}} \times 100$. |
| **RF06** | Emissão de Alertas e Relatórios Consolidados | O sistema deve emitir avisos imediatos na console e consolidar relatórios gerais exibindo IP, criticidade, total de falhas e status operacional. |
| **RF07** | Roteamento Inter-VLAN (Infraestrutura) | O roteador deve realizar o roteamento de pacotes entre as VLANs 10, 20 e 30 por meio do enlace tronco dot1Q, permitindo que estações de qualquer setor acessem o servidor Web e DNS. |
| **RF08** | Distribuição Automática de Endereços IP (Infra) | O roteador deve atuar como servidor DHCP, entregando automaticamente IP, máscara, gateway padrão e servidor DNS para as máquinas clientes das VLANs 10 e 20. |
| **RF09** | Resolução Local de Nomes (Infra) | O servidor DNS interno deve responder às requisições dos clientes resolvendo a URL `finbank.local` para o endereço IP `192.168.30.10`. |

### Requisitos Não Funcionais (RNF)

| Código | Categoria | Descrição Detalhada |
| :--- | :--- | :--- |
| **RNF01** | Desempenho e Timeout | Cada teste de ping ICMP deve operar com tempo limite (*timeout*) máximo de 800 milissegundos por verificação, garantindo que o ciclo de coleta não congele na presença de ativos offline. |
| **RNF02** | Portabilidade e Compatibilidade | O script Python deve ser compatível com os sistemas operacionais Windows e Linux, identificando automaticamente a plataforma para aplicar os parâmetros adequados do comando ping (`-n` para Windows e `-c` para Linux). |
| **RNF03** | Segurança e Segregação Lógica | A infraestrutura deve garantir o isolamento estrito de domínios de broadcast por meio de VLANs, impedindo que tráfegos residuais ou não autorizados da área de atendimento alcancem diretamente os caixas operacionais. |
| **RNF04** | Resiliência e Prevenção de Falsos Positivos | O sistema de monitoramento não deve disparar alertas de queda definitiva após uma única falha esporádica, exigindo confirmação por amostragem acumulada (3 falhas consecutivas). |
| **RNF05** | Confiabilidade na Simulação | A infraestrutura simulada deve utilizar imagens e comandos estritamente nativos do Cisco IOS, permitindo 100% de reproducibilidade no simulador Cisco Packet Tracer v8.x. |
| **RNF06** | Usabilidade e Legibilidade | A saída visual em console e os relatórios gerados devem utilizar formatação tabular clara e intuitiva, com destaque por tags coloridas/identificadores de criticidade (`[CRITICO]`, `[ALTA]`, `[NORMAL]`). |

---

## 1.7 Regras de Negócio (RN)

1. **RN01 — Priorização Hierárquica por Criticidade:**  
   Os equipamentos de rede são classificados em três categorias de criticidade de negócio:
   - **CRÍTICA:** Ativos cuja inoperância derruba o sistema bancário por completo (ex.: Roteador Gateway `R-FINBANK` e Servidor Central `SRV-WEB-BANCO`). Falhas nesses ativos geram avisos imediatos de emergência no monitor.
   - **ALTA:** Ativos diretamente ligados a processos financeiros e de fechamento de caixa (ex.: `PC-OPER-01`).
   - **NORMAL:** Equipamentos administrativos ou de suporte a clientes (ex.: `PC-ATEND-01`, `PC-ADMIN-01`, Servidor Syslog).

2. **RN02 — Gatilho de Indisponibilidade Persistente (Regra das 3 Falhas):**  
   Uma estação ou servidor somente será declarado em estado de *\"Indisponibilidade Persistente\"* caso apresente **3 (três) verificações consecutivas com resultado de FALHA**. Essa regra evita que manutenções rápidas ou perdas transitórias de pacotes disparem ações corretivas emergenciais da equipe de campo.

3. **RN03 — Normalização e Reset do Contador:**  
   Caso um ativo com histórico recente de falhas responda com sucesso (`SUCESSO`) em uma verificação subsequente, o contador de falhas consecutivas desse ativo é zerado imediatamente, restabelecendo o status regular de comunicação.

4. **RN04 — Imutabilidade e Integridade do Histórico de Auditoria:**  
   Toda e qualquer verificação executada deve ter seu registro preservado com identificador, timestamp e status de forma cronológica. Registros de verificações passadas não podem ser alterados ou sobrescritos durante a execução do software.

5. **RN05 — Reserva Estática de Endereçamento IP:**  
   Nas sub-redes das VLANs, os 10 primeiros endereços IPs utilizáveis (`.1` a `.10`) são categoricamente reservados para interfaces de rede de gateways, roteadores, switches e servidores estáticos. O serviço de DHCP deve excluir compulsoriamente essa faixa de distribuição automática.

6. **RN06 — Alocação Exclusiva de Setores por VLAN:**  
   É estritamente vedada a mistura de portas de atendimento com portas operacionais na mesma rede virtual. Estações de Atendimento conectam-se unicamente nas portas da VLAN 10 (FastEthernet 0/1 a 0/5), estações de Operações na VLAN 20 (FastEthernet 0/6 a 0/10) e Servidores na VLAN 30 (FastEthernet 0/11 a 0/15).

---

## 1.8 Arquitetura e Tecnologias Utilizadas

### Padrão de Arquitetura de Rede: Router-on-a-Stick
A solução adota a arquitetura de rede em duas camadas (Borda/Distribuição e Acesso), empregando o consagrado modelo **Router-on-a-Stick**:
- Um único enlace físico de alta capacidade (**GigabitEthernet**) conecta o Switch de distribuição (`SW-FINBANK`) ao Roteador de borda (`R-FINBANK`).
- Essa porta é parametrizada em modo **Tronco (Trunk)** sob o protocolo de tagueamento **IEEE 802.1Q**, transportando os quadros de todas as VLANs com seus respectivos tags de identificação.
- No Roteador, a porta física `GigabitEthernet 0/0` é dividida em **subinterfaces lógicas** (`Gig0/0.10`, `Gig0/0.20` e `Gig0/0.30`), onde cada subinterface possui seu respectivo endereço IP e atua como Gateway Padrão da sua sub-rede.

### Diagrama Esquemático da Arquitetura

```
                                  +--------------------------+
                                  |        R-FINBANK         |
                                  |    Roteador Cisco 1941   |
                                  |   Gateways: .10.1 / .20.1|
                                  |             .30.1        |
                                  +------------+-------------+
                                               | GigabitEthernet 0/0
                                               | [Enlace Tronco 802.1Q]
                                               | GigabitEthernet 0/1
                                  +------------+-------------+
                                  |        SW-FINBANK        |
                                  |    Switch Cisco 2960     |
                                  +---+----------+---------+-+
                                      |          |         |
           +--------------------------+          |         +--------------------------+
           | Fa0/1 e Fa0/2                       | Fa0/6 e Fa0/7                      | Fa0/11 e Fa0/12
           |                                     |                                    |
   +-------v------------------+       +----------v---------------+         +----------v---------------+
   |    SETOR ATENDIMENTO     |       |    OPERAÇÕES & ADMIN     |         |   SERVIDORES & DATA CTR  |
   |        (VLAN 10)         |       |        (VLAN 20)         |         |        (VLAN 30)         |
   |   Rede: 192.168.10.0/24  |       |   Rede: 192.168.20.0/24  |         |   Rede: 192.168.30.0/24  |
   |                          |       |                          |         |                          |
   | [PC-ATEND-01] (DHCP)     |       | [PC-OPER-01] (Caixa)     |         | [SRV-WEB-BANCO] (Est.)   |
   | [PC-ATEND-02] (DHCP)     |       | [PC-ADMIN-01] (Admin)    |         | Servicos: HTTP e DNS     |
   |                          |       |                          |         | [SRV-MONITOR] (Est.)     |
   | Gateway: 192.168.10.1    |       | Gateway: 192.168.20.1    |         | Gateway: 192.168.30.1    |
   +--------------------------+       +--------------------------+         +--------------------------+
```

### Matriz de Endereçamento IPv4 e Dispositivos

| Ativo | Interface Física | Endereço IPv4 | Máscara | Gateway | Setor / VLAN | Criticidade | Serviço |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`R-FINBANK`** | Gig0/0.10<br>Gig0/0.20<br>Gig0/0.30 | `192.168.10.1`<br>`192.168.20.1`<br>`192.168.30.1` | `255.255.255.0` | *N/A* | Gateway Core | **CRÍTICA** | Roteamento 802.1Q e Pools DHCP |
| **`SRV-WEB-BANCO`** | FastEthernet 0 | `192.168.30.10` | `255.255.255.0` | `192.168.30.1` | VLAN 30 | **CRÍTICA** | Servidor Web HTTP e DNS (`finbank.local`) |
| **`SRV-MONITOR`** | FastEthernet 0 | `192.168.30.20` | `255.255.255.0` | `192.168.30.1` | VLAN 30 | **NORMAL** | Servidor Coletor Syslog / Logs de Auditoria |
| **`PC-OPER-01`** | FastEthernet 0 | `192.168.20.11` (DHCP) | `255.255.255.0` | `192.168.20.1` | VLAN 20 | **ALTA** | Terminal Financeiro de Caixa Operacional |
| **`PC-ADMIN-01`** | FastEthernet 0 | `192.168.20.12` (DHCP) | `255.255.255.0` | `192.168.20.1` | VLAN 20 | **NORMAL** | Estação de Gestão Administrativa |
| **`PC-ATEND-01`** | FastEthernet 0 | `192.168.10.11` (DHCP) | `255.255.255.0` | `192.168.10.1` | VLAN 10 | **NORMAL** | Estação de Atendimento ao Cliente |
| **`PC-ATEND-02`** | FastEthernet 0 | `192.168.10.12` (DHCP) | `255.255.255.0` | `192.168.10.1` | VLAN 10 | **NORMAL** | Estação de Atendimento ao Cliente |

### Tecnologias e Protocolos Utilizados

1. **Camadas Físicas e de Enlace (L1 e L2):**
   - **Cabeamento Par Trançado (Cat5e/Cat6 - Copper Straight-Through):** Conexões diretas padronizadas T568A/B entre dispositivos terminais e switches.
   - **Padrão IEEE 802.1Q:** Protocolo aberto de tagueamento de VLANs que insere uma etiqueta de 4 bytes no cabeçalho do quadro Ethernet para identificação do segmento no tronco.
   - **Spanning Tree Protocol (STP) & Cisco PortFast:** Mecanismos de prevenção de loops de camada 2 com aceleração de transição de estado (*Listening/Learning* para *Forwarding*) nas portas conectadas a computadores clientes.

2. **Camadas de Rede e Transporte (L3 e L4):**
   - **IPv4 (Internet Protocol v4):** Endereçamento privado padrão RFC 1918 (Classe C, `192.168.0.0/16`) sub-dividido em sub-redes `/24`.
   - **ICMP (Internet Control Message Protocol):** Protocolo de mensagens de controle utilizado para emissão de *Echo Request* e recepção de *Echo Reply*, sendo a base do monitoramento de disponibilidade.
   - **UDP (User Datagram Protocol):** Utilizado pelo protocolo DHCP (portas 67 e 68 no servidor e cliente), DNS (porta 53) e Syslog (porta 514).
   - **TCP (Transmission Control Protocol):** Utilizado no tráfego orientado a conexão do serviço Web bancário HTTP (porta 80).

3. **Camada de Aplicação e Serviços de Rede (L7):**
   - **DHCP (Dynamic Host Configuration Protocol):** Serviço configurado nativamente no Cisco IOS para concessão dinâmica de parâmetros de rede (IP, Gateway, Máscara e Servidor DNS).
   - **DNS (Domain Name System):** Resolução de nomes corporativos, mapeando `finbank.local` para o endereço IP fixo `192.168.30.10`.
   - **HTTP (Hypertext Transfer Protocol):** Disponibilização da interface web institucional do sistema bancário interno da FinBank Digital.
   - **Syslog Daemon:** Serviço de centralização de registros operacionais e mensagens de diagnóstico da infraestrutura.

4. **Ambiente de Simulação e Ferramentas de Desenvolvimento:**
   - **Cisco Packet Tracer v8.x:** Ambiente de simulação gráfica e execução do Cisco IOS 15.x. Equipamentos simulados: Roteador Cisco 1941, Switch Catalyst 2960-24TT, Servidores genéricos e PCs clientes.
   - **Linguagem Python 3:** Implementação completa da aplicação de monitoramento (`monitor_finbank.py`). Utilização de classes e encapsulamento em conformidade com as boas práticas de Engenharia de Software.
   - **Módulos Nativos Python:** `subprocess` (execução dos comandos nativos de ping com redirecionamento de streams), `platform` (verificação do sistema operacional anfitrião) e `datetime` (geração de carimbos temporais precisos para auditoria).
