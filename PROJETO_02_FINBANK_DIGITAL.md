# PROJETO 02 — FinBank Digital: Infraestrutura & Monitoramento
**Divisão do Projeto em 2 Equipes:**
- **GRUPO 01 (Sua Equipe):** Infraestrutura de Rede, Cabeamento, VLANs, Roteamento e Serviços no **Cisco Packet Tracer**.
- **GRUPO 02:** Sistema Lógico de Monitoramento, Métricas de Uptime e Regras de Alerta em **Python**.

---

## 1. Divisão de Responsabilidades das Equipes

```
+---------------------------------------------------------------------------------+
|                                FINBANK DIGITAL                                  |
+---------------------------------------+-----------------------------------------+
|      GRUPO 01: INFRAESTRUTURA         |           GRUPO 02: LÓGICA              |
|       (Cisco Packet Tracer)           |         (Software de Monitor)           |
+---------------------------------------+-----------------------------------------+
| • Montagem física da topologia        | • Implementação dos Requisitos Funcionais|
| • Cabeamento e conexões de portas     |   (RF01 a RF06 em Python)               |
| • Configuração de VLANs (10, 20 e 30) | • Coleta periódica de ICMP / Ping       |
| • Enlace Tronco 802.1Q                | • Lógica de indisponibilidade           |
| • Router-on-a-Stick e Pools DHCP      |   persistente (3 falhas consecutivas)   |
| • Configuração de HTTP, DNS e Syslog  | • Cálculo percentual de Uptime          |
| • Testes de conectividade física      | • Emissão de alertas por criticidade    |
| • Arquivo .PKT final para entrega     | • Relatório consolidado em tela/arquivo |
+---------------------------------------+-----------------------------------------+
```

### O que o Grupo 01 entrega ao Grupo 02 (Tabela de Handover):
O Grupo 01 finaliza a rede no Packet Tracer e entrega a seguinte tabela de parâmetros para o Grupo 02 cadastrar no monitor:

| Dispositivo | IP Designado | Setor | Serviço Ativo | Criticidade |
| :--- | :--- | :--- | :--- | :--- |
| `R-FINBANK` | `192.168.30.1` | Gateway Geral | Roteamento / ICMP | **CRÍTICA** |
| `SRV-WEB-BANCO` | `192.168.30.10` | VLAN 30 (Data Center) | HTTP (80) & DNS (`finbank.local`) | **CRÍTICA** |
| `SRV-MONITOR` | `192.168.30.20` | VLAN 30 (Data Center) | Syslog | **NORMAL** |
| `PC-OPER-01` | `192.168.20.11` | VLAN 20 (Operações) | Terminal de Caixa | **ALTA** |
| `PC-ADMIN-01` | `192.168.20.12` | VLAN 20 (Admin) | Gestão Interna | **NORMAL** |
| `PC-ATEND-01` | `192.168.10.11` | VLAN 10 (Atendimento) | Estação Cliente | **NORMAL** |
| `PC-ATEND-02` | `192.168.10.12` | VLAN 10 (Atendimento) | Estação Cliente | **NORMAL** |

---

## 2. Passo a Passo Completo da Infraestrutura (Grupo 01)

### Passo 1: Selecionar e Posicionar os Equipamentos
No Cisco Packet Tracer, arraste para a tela de trabalho:
- **1 Roteador:** `Routers` -> modelo **1941** (Nomeie como `R-FINBANK`)
- **1 Switch:** `Switches` -> modelo **2960-24TT** (Nomeie como `SW-FINBANK`)
- **2 Servidores:** `End Devices` -> `Server-PT` (Nomeie como `SRV-WEB-BANCO` e `SRV-MONITOR`)
- **4 Computadores:** `End Devices` -> `PC-PT` (`PC-ATEND-01`, `PC-ATEND-02`, `PC-OPER-01`, `PC-ADMIN-01`)

---

### Passo 2: Cabeamento Físico (Cabo Direto / Copper Straight-Through)
Use o cabo contínuo preto e conecte porta a porta:

1. **Roteador para Switch (Tronco):**
   - `R-FINBANK` porta `GigabitEthernet 0/0` ➔ `SW-FINBANK` porta `GigabitEthernet 0/1`
2. **VLAN 10 — Atendimento:**
   - `PC-ATEND-01` porta `FastEthernet 0` ➔ `SW-FINBANK` porta `FastEthernet 0/1`
   - `PC-ATEND-02` porta `FastEthernet 0` ➔ `SW-FINBANK` porta `FastEthernet 0/2`
3. **VLAN 20 — Operações e Administração:**
   - `PC-OPER-01` porta `FastEthernet 0` ➔ `SW-FINBANK` porta `FastEthernet 0/6`
   - `PC-ADMIN-01` porta `FastEthernet 0` ➔ `SW-FINBANK` porta `FastEthernet 0/7`
4. **VLAN 30 — Servidores Internos:**
   - `SRV-WEB-BANCO` porta `FastEthernet 0` ➔ `SW-FINBANK` porta `FastEthernet 0/11`
   - `SRV-MONITOR` porta `FastEthernet 0` ➔ `SW-FINBANK` porta `FastEthernet 0/12`

---

### Passo 3: Configuração do Switch (`SW-FINBANK`)
Clique no switch, abra a aba **CLI** e cole:

```ios
enable
configure terminal
hostname SW-FINBANK

! 1. Criacao das 3 VLANs
vlan 10
 name ATENDIMENTO
exit

vlan 20
 name OPERACOES_ADMIN
exit

vlan 30
 name SERVIDORES
exit

! 2. Portas da VLAN 10 (Fa0/1 a Fa0/5)
interface range fastEthernet 0/1 - 5
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
exit

! 3. Portas da VLAN 20 (Fa0/6 a Fa0/10)
interface range fastEthernet 0/6 - 10
 switchport mode access
 switchport access vlan 20
 spanning-tree portfast
exit

! 4. Portas da VLAN 30 (Fa0/11 a Fa0/15)
interface range fastEthernet 0/11 - 15
 switchport mode access
 switchport access vlan 30
 spanning-tree portfast
exit

! 5. Porta de Tronco para o Roteador
interface gigabitEthernet 0/1
 switchport mode trunk
 description LINK_TRUNK_ROUTER
exit

end
write memory
```

---

### Passo 4: Configuração do Roteador (`R-FINBANK`)
No roteador, abra a aba **CLI**. Se surgir a pergunta de configuração inicial, responda **`no`** e cole:

```ios
enable
configure terminal
hostname R-FINBANK

! 1. Habilitar a interface fisica principal
interface gigabitEthernet 0/0
 no shutdown
exit

! 2. Subinterface VLAN 10 (Atendimento)
interface gigabitEthernet 0/0.10
 encapsulation dot1Q 10
 ip address 192.168.10.1 255.255.255.0
 description GATEWAY_VLAN10_ATENDIMENTO
exit

! 3. Subinterface VLAN 20 (Operacoes e Admin)
interface gigabitEthernet 0/0.20
 encapsulation dot1Q 20
 ip address 192.168.20.1 255.255.255.0
 description GATEWAY_VLAN20_OPERACOES
exit

! 4. Subinterface VLAN 30 (Servidores)
interface gigabitEthernet 0/0.30
 encapsulation dot1Q 30
 ip address 192.168.30.1 255.255.255.0
 description GATEWAY_VLAN30_SERVIDORES
exit

! 5. Pools de DHCP para Atendimento e Operacoes
ip dhcp excluded-address 192.168.10.1 192.168.10.10
ip dhcp excluded-address 192.168.20.1 192.168.20.10

ip dhcp pool POOL_ATENDIMENTO
 network 192.168.10.0 255.255.255.0
 default-router 192.168.10.1
 dns-server 192.168.30.10
exit

ip dhcp pool POOL_OPERACOES
 network 192.168.20.0 255.255.255.0
 default-router 192.168.20.1
 dns-server 192.168.30.10
exit

end
write memory
```

---

### Passo 5: Configuração dos Servidores (Serviços e IPs Estáticos)

#### A. Servidor Web e DNS (`SRV-WEB-BANCO`)
1. **Configurar IP:**
   - Acesse **Desktop** ➔ **IP Configuration**:
     - IP: `192.168.30.10`
     - Subnet: `255.255.255.0`
     - Default Gateway: `192.168.30.1`
     - DNS Server: `192.168.30.10`
2. **Ativar Serviço Web:**
   - Acesse **Services** ➔ **HTTP**.
   - Ligue **HTTP** e **HTTPS** em **On**.
   - No arquivo `index.html`, clique em **edit** e coloque:
     ```html
     <html>
       <center><h1>FinBank Digital - Servidor Central Ativo</h1></center>
       <p align="center">Sistema Bancario Interno Operando Normalmente</p>
     </html>
     ```
   - Clique em **Save**.
3. **Ativar Serviço DNS:**
   - Acesse **Services** ➔ **DNS**.
   - Marque **On**.
   - Campo Name: `finbank.local`
   - Campo Address: `192.168.30.10`
   - Clique em **Add**.

#### B. Servidor Syslog (`SRV-MONITOR`)
1. **Configurar IP:**
   - Acesse **Desktop** ➔ **IP Configuration**:
     - IP: `192.168.30.20`
     - Subnet: `255.255.255.0`
     - Default Gateway: `192.168.30.1`
     - DNS Server: `192.168.30.10`
2. **Ativar Syslog:**
   - Acesse **Services** ➔ **Syslog** ➔ marque **On**.

---

### Passo 6: Ativação dos PCs Clientes
Para os computadores `PC-ATEND-01`, `PC-ATEND-02`, `PC-OPER-01` e `PC-ADMIN-01`:
1. Abra o computador ➔ aba **Desktop** ➔ **IP Configuration**.
2. Clique na opção **DHCP**.
3. Confirme que ele recebe automaticamente um IP de sua respectiva VLAN (ex: `192.168.10.11` ou `192.168.20.11`).

---

### Passo 7: Testes e Validação Obrigatória da Infraestrutura
1. **Teste de Ping Inter-VLAN:** No `PC-ATEND-01` (VLAN 10), abra o Command Prompt e digite:
   `ping 192.168.30.10`  
   *(Deve responder com Reply from 192.168.30.10).*
2. **Teste de Resolução DNS e Web:** No `PC-OPER-01` (VLAN 20), abra o **Web Browser** e acesse:
   `http://finbank.local`  
   *(A página do FinBank Digital deve abrir imediatamente).*
3. **Teste de Simulação de Falha:** Desconecte o cabo do `SRV-WEB-BANCO` ou dê um `shutdown` na porta `fa0/11` do switch. Repita o ping e mostre que o serviço ficou inalcançável (cenário que o Grupo 02 irá monitorar).
