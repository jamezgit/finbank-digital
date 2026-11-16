# Simulação de Rede — Cisco Packet Tracer
**Projeto 02 — FinBank Digital: Infraestrutura & Monitoramento**

Este diretório contém os artefatos, scripts de configuração e instruções para a topologia de rede simulada da agência bancária no **Cisco Packet Tracer (v8.x ou superior)**.

---

## 📁 Arquivos deste Diretório

* **`FinBank_Digital_Topologia.pkt`**: Arquivo oficial da topologia de rede pronta e homologada.
* **`comandos_cisco_ios.txt`**: Código e comandos completos do Cisco IOS para o Switch Catalyst 2960 e Roteador Cisco 1941.

---

## 🛠️ Como Adicionar / Salvar seu arquivo `.pkt` aqui

Se você montou a rede diretamente no Cisco Packet Tracer:
1. No Cisco Packet Tracer, clique em **File > Save As...**
2. Salve o arquivo com o nome **`FinBank_Digital_Topologia.pkt`** exatamente dentro desta pasta:
   `cisco_packet_tracer/FinBank_Digital_Topologia.pkt`
3. Ao realizar o `git add .` e `git commit`, o arquivo `.pkt` será sincronizado e versionado automaticamente no seu GitHub!

---

## 📐 Topologia e Arquitetura Empregada

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
   |    SETOR ATENDIMENTO     |       |    OPERAÇÕES & ADMIN     |         |  SERVIDORES DATA CENTER  |
   |        (VLAN 10)         |       |        (VLAN 20)         |         |        (VLAN 30)         |
   |   Rede: 192.168.10.0/24  |       |   Rede: 192.168.20.0/24  |         |   Rede: 192.168.30.0/24  |
   |                          |       |                          |         |                          |
   | [PC-ATEND-01] (DHCP)     |       | [PC-OPER-01] (Caixa)     |         | [SRV-WEB-BANCO] (Est.)   |
   | [PC-ATEND-02] (DHCP)     |       | [PC-ADMIN-01] (Admin)    |         | Servicos: HTTP e DNS     |
   |                          |       |                          |         | [SRV-MONITOR] (Est.)     |
   | Gateway: 192.168.10.1    |       | Gateway: 192.168.20.1    |         | Gateway: 192.168.30.1    |
   +--------------------------+       +--------------------------+         +--------------------------+
```

---

## 🧪 Testes de Validação no Packet Tracer

1. **Atribuição Automática via DHCP:**
   * Clique em qualquer PC cliente (`PC-ATEND-01` ou `PC-OPER-01`), abra a aba **Desktop > IP Configuration** e marque a opção **DHCP**. O PC deve receber endereço IP na faixa correspondente e máscara `255.255.255.0`.
2. **Ping Inter-VLAN:**
   * No `PC-ATEND-01` (VLAN 10), abra o **Command Prompt** e digite:
     ```bash
     ping 192.168.30.10
     ```
   * O roteador Cisco 1941 deve intermediar a comunicação via subinterfaces 802.1Q com 0% de perda.
3. **Resolução de Nomes e Acesso Web:**
   * No `PC-OPER-01` (VLAN 20), abra o navegador (**Web Browser**) e acerte a URL `http://finbank.local`. O portal institucional central deve carregar imediatamente.
4. **Simulação de Interrupção de Serviço:**
   * Para simular a indisponibilidade monitorada pelo script Python, desconecte o cabo do `SRV-WEB-BANCO` ou desligue a porta `fa0/11` no switch:
     ```ios
     interface fastEthernet 0/11
      shutdown
     ```
