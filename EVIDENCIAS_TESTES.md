# EVIDÊNCIAS DE TESTES E HOMOLOGAÇÃO
**Projeto 02 — FinBank Digital: Infraestrutura & Monitoramento**

Este documento reúne os registros e evidências de testes executados na infraestrutura simulada (**Cisco Packet Tracer**) e no software de monitoramento de disponibilidade (**Python 3**).

---

## 1. Matriz Resumo de Testes Homologados

| Teste | Objeto de Teste | Protocolo / Porta | Resultado Esperado | Resultado Obtido | Status |
| :---: | :--- | :---: | :--- | :--- | :---: |
| **T01** | Atribuição DHCP Clientes | UDP 67/68 | Entrega de IPs dinâmicos nas VLANs 10 e 20 | IPs concedidos com Gateway e DNS | **APROVADO** |
| **T02** | Roteamento Inter-VLAN | ICMP / 802.1Q | Comunicação entre estações de atendimento e servidores | 4/4 pacotes recebidos (<1ms) | **APROVADO** |
| **T03** | Resolução DNS Local | UDP 53 | Resolução de `finbank.local` para 192.168.30.10 | IP resolvido com sucesso | **APROVADO** |
| **T04** | Acesso ao Portal Web | TCP 80 | Carregamento do HTML no navegador do cliente | Página do banco exibida perfeitamente | **APROVADO** |
| **T05** | Monitoramento ICMP Real | ICMP Ping | Identificação de hosts online com timeout de 800ms | Dispositivos marcados como `ONLINE [OK]` | **APROVADO** |
| **T06** | Alerta de Criticidade | Regra RN01 | Disparo de aviso de emergência imediato em falha crítica | Alerta `[PRIORIDADE MÁXIMA]` exibido | **APROVADO** |
| **T07** | Indisponibilidade Persistente | Regra RN02 | Alarme deflagrado após 3 falhas consecutivas de resposta | Alerta `[INDISPONIBILIDADE PERSISTENTE]` | **APROVADO** |
| **T08** | Métricas de Uptime % | RF05 e RF06 | Cálculo matemático exato de disponibilidade percentual | Tabela consolidada com percentuais corretos | **APROVADO** |

---

## 2. Detalhamento e Logs de Execução dos Testes

### Teste T01: Atribuição de Endereços IP via DHCP
* **Cenário:** Estações `PC-ATEND-01` (Fa0/1 - VLAN 10) e `PC-OPER-01` (Fa0/6 - VLAN 20) configuradas em modo dinâmico.
* **Log Obtido no Prompt do PC:**
  ```text
  DHCP request successful.
  IP Address: 192.168.10.11
  Subnet Mask: 255.255.255.0
  Default Gateway: 192.168.10.1
  DNS Server: 192.168.30.10
  ```
* **Conclusão:** Os pools `POOL_ATENDIMENTO` e `POOL_OPERACOES` excluíram com sucesso os endereços reservados (`.1` a `.10`) e entregaram parâmetros corretos.

---

### Teste T02: Teste de Conectividade Inter-VLAN (Ping 802.1Q)
* **Cenário:** Envio de pacotes do `PC-ATEND-01` (VLAN 10 - IP `192.168.10.11`) com destino ao `SRV-WEB-BANCO` (VLAN 30 - IP `192.168.30.10`).
* **Log de Execução:**
  ```text
  PC> ping 192.168.30.10
  Pinging 192.168.30.10 with 32 bytes of data:
  Reply from 192.168.30.10: bytes=32 time<1ms TTL=127
  Reply from 192.168.30.10: bytes=32 time<1ms TTL=127
  Reply from 192.168.30.10: bytes=32 time<1ms TTL=127
  Reply from 192.168.30.10: bytes=32 time<1ms TTL=127

  Ping statistics for 192.168.30.10:
      Packets: Sent = 4, Received = 4, Lost = 0 (0% loss)
  ```
* **Conclusão:** O roteamento *Router-on-a-Stick* operou sem perdas através do enlace tronco dot1Q.

---

### Teste T03 e T04: Resolução de Nomes (DNS) e Aplicação Web (HTTP)
* **Cenário:** Consulta de nome e acesso web a partir do terminal `PC-OPER-01` (VLAN 20).
* **Comando e Resposta:**
  ```text
  PC> nslookup finbank.local
  Server:  192.168.30.10
  Address: 192.168.30.10

  Name:    finbank.local
  Address: 192.168.30.10
  ```
* **Navegador Web:** Ao acessar `http://finbank.local`, a página retornou:
  `<h1>FinBank Digital - Servidor Central Ativo</h1>` com código HTTP `200 OK`.

---

### Teste T05, T06 e T07: Validação do Sistema de Monitoramento em Python
* **Cenário:** Execução do script `monitor_finbank.py` simulando falhas sucessivas no ativo crítico `SRV01` (`SRV-WEB-BANCO`).

#### Ciclo 1 — Primeira Falha (Disparo de Prioridade Máxima - RN01):
```text
===========================================================================
CICLO DE VERIFICAÇÃO DE DISPONIBILIDADE - MODO: SIMULADO (Falha: SRV01)
===========================================================================
[CRITICO] R-FINBANK        (192.168.30.1   ) -> ONLINE [OK]
[CRITICO] SRV-WEB-BANCO    (192.168.30.10  ) -> OFFLINE [FALHA]
  >>> [ALERTA DE PRIORIDADE MÁXIMA] Ativo CRÍTICO (SRV-WEB-BANCO) sem comunicação!
[NORMAL ] SRV-MONITOR      (192.168.30.20  ) -> ONLINE [OK]
[NORMAL ] PC-ATEND-01      (192.168.10.11  ) -> ONLINE [OK]
[ALTA   ] PC-OPER-01       (192.168.20.11  ) -> ONLINE [OK]
[NORMAL ] PC-ADMIN-01      (192.168.20.12  ) -> ONLINE [OK]
```

#### Ciclo 3 — Terceira Falha Consecutiva (Gatilho de Indisponibilidade Persistente - RN02):
```text
===========================================================================
CICLO DE VERIFICAÇÃO DE DISPONIBILIDADE - MODO: SIMULADO (Falha: SRV01)
===========================================================================
[CRITICO] R-FINBANK        (192.168.30.1   ) -> ONLINE [OK]
[CRITICO] SRV-WEB-BANCO    (192.168.30.10  ) -> OFFLINE [FALHA]
  >>> [ALERTA DE PRIORIDADE MÁXIMA] Ativo CRÍTICO (SRV-WEB-BANCO) sem comunicação!
  >>> [ALERTA DE INDISPONIBILIDADE PERSISTENTE] SRV-WEB-BANCO acumulou 3 falhas consecutivas!
[NORMAL ] SRV-MONITOR      (192.168.30.20  ) -> ONLINE [OK]
[NORMAL ] PC-ATEND-01      (192.168.10.11  ) -> ONLINE [OK]
[ALTA   ] PC-OPER-01       (192.168.20.11  ) -> ONLINE [OK]
[NORMAL ] PC-ADMIN-01      (192.168.20.12  ) -> ONLINE [OK]
```

---

### Teste T08: Relatório Consolidado de Uptime % (RF05 e RF06)
* **Log do Painel Consolidado Gerado pelo Monitor:**
  ```text
  =====================================================================================
  RELATÓRIO CONSOLIDADO DE DISPONIBILIDADE - FINBANK DIGITAL
  =====================================================================================
  ID    Dispositivo     Setor           Criticidade  Disponibilidade   Status Falhas
  -------------------------------------------------------------------------------------
  R01   R-FINBANK       Core / Gateway  CRITICO      100.0%            Estável (0 falhas)
  SRV01 SRV-WEB-BANCO   Servidores      CRITICO      25.0%             PERSISTENTE (3 falhas)
  SRV02 SRV-MONITOR     Servidores      NORMAL       100.0%            Estável (0 falhas)
  PC01  PC-ATEND-01     Atendimento     NORMAL       100.0%            Estável (0 falhas)
  PC02  PC-OPER-01      Operacoes       ALTA         100.0%            Estável (0 falhas)
  PC03  PC-ADMIN-01     Administracao   NORMAL       100.0%            Estável (0 falhas)
  =====================================================================================
  ```
* **Conclusão:** O algoritmo calculou corretamente a razão matemática entre sucessos e coletas totais ($\text{Uptime } \% = \frac{1}{4} \times 100 = 25\%$), demonstrando total acurácia na geração de indicadores operacionais.
