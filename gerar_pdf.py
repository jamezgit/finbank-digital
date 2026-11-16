import os
import sys

class RelatorioPDF:
    def __init__(self, filename):
        self.filename = filename
        self.objects = []
        self.pages = []
        self.current_stream = []
        self.width = 595.28   # A4 width in pt
        self.height = 841.89  # A4 height in pt
        self.margin_x = 36    # Margem lateral 36pt (~12.7mm)
        self.margin_y = 36
        self.content_w = self.width - (self.margin_x * 2)

    def _add_object(self, content):
        self.objects.append(content)
        return len(self.objects)

    def new_page(self):
        if self.current_stream:
            self._finish_page()
        self.current_stream = []

    def _finish_page(self):
        stream_str = "\n".join(self.current_stream)
        stream_bytes = stream_str.encode('latin1', 'replace')
        length = len(stream_bytes)
        stream_obj = f"<< /Length {length} >>\nstream\n{stream_str}\nendstream"
        stream_id = self._add_object(stream_obj)
        self.pages.append(stream_id)
        self.current_stream = []

    def draw_rect(self, x, y, w, h, fill_rgb=None, stroke_rgb=None, line_width=1):
        cmds = []
        if stroke_rgb:
            r, g, b = stroke_rgb
            cmds.append(f"{r:.3f} {g:.3f} {b:.3f} RG")
            cmds.append(f"{line_width:.2f} w")
        if fill_rgb:
            r, g, b = fill_rgb
            cmds.append(f"{r:.3f} {g:.3f} {b:.3f} rg")
        
        cmds.append(f"{x:.2f} {y:.2f} {w:.2f} {h:.2f} re")
        if fill_rgb and stroke_rgb:
            cmds.append("B")
        elif fill_rgb:
            cmds.append("f")
        else:
            cmds.append("S")
        self.current_stream.append(" ".join(cmds))

    def draw_text(self, text, x, y, font="F1", size=10, rgb=(0,0,0)):
        r, g, b = rgb
        clean_text = text.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')
        clean_text = clean_text.encode('latin1', 'replace').decode('latin1')
        cmd = f"BT /{font} {size} Tf {r:.3f} {g:.3f} {b:.3f} rg 1 0 0 1 {x:.2f} {y:.2f} Tm ({clean_text}) Tj ET"
        self.current_stream.append(cmd)

    def draw_line(self, x1, y1, x2, y2, rgb=(0.75,0.75,0.75), width=1):
        r, g, b = rgb
        cmd = f"{r:.3f} {g:.3f} {b:.3f} RG {width:.2f} w {x1:.2f} {y1:.2f} m {x2:.2f} {y2:.2f} l S"
        self.current_stream.append(cmd)

    def add_header(self, page_num, total_pages=4):
        # Header banner
        self.draw_rect(self.margin_x, self.height - 28, self.content_w, 18, fill_rgb=(0.04, 0.15, 0.28))
        self.draw_text("FINBANK DIGITAL  •  PROJETO 02 — RELATÓRIO TÉCNICO DE INFRAESTRUTURA", self.margin_x + 8, self.height - 23, font="F2", size=7.5, rgb=(1,1,1))
        self.draw_text("GRUPO 01: CISCO PACKET TRACER", self.width - self.margin_x - 145, self.height - 23, font="F2", size=7.5, rgb=(0.35, 0.85, 0.70))
        
        # Footer
        self.draw_line(self.margin_x, 26, self.width - self.margin_x, 26, rgb=(0.8,0.8,0.8), width=0.8)
        self.draw_text("Ambiente de Simulação: Cisco Packet Tracer v8.x | Roteamento 802.1Q | VLANs 10, 20, 30", self.margin_x, 16, font="F1", size=7.5, rgb=(0.4,0.4,0.4))
        self.draw_text(f"Página {page_num} de {total_pages}", self.width - self.margin_x - 55, 16, font="F2", size=7.5, rgb=(0.2,0.2,0.2))

    def build_pdf(self):
        # ==========================================
        # PÁGINA 1: CAPA, ESCOPO E DIVISÃO DE GRUPOS
        # ==========================================
        self.new_page()
        self.add_header(1, 4)

        # Bloco de Título Principal
        y = self.height - 50
        self.draw_rect(self.margin_x, y - 55, self.content_w, 55, fill_rgb=(0.95, 0.97, 1.0), stroke_rgb=(0.75, 0.82, 0.95), line_width=1)
        self.draw_text("PROJETO 02 — INFRAESTRUTURA E MONITORAMENTO DE REDE", self.margin_x + 12, y - 18, font="F2", size=13, rgb=(0.04, 0.15, 0.28))
        self.draw_text("Documentação Executiva de Implementação, Configurações e Homologação", self.margin_x + 12, y - 32, font="F1", size=9.5, rgb=(0.25, 0.35, 0.50))
        self.draw_text("STATUS: HOMOLOGADO, TESTADO E 100% OPERACIONAL", self.margin_x + 12, y - 46, font="F2", size=8.5, rgb=(0.05, 0.55, 0.35))

        # Tabela Metadados
        y -= 68
        self.draw_rect(self.margin_x, y - 28, self.content_w, 28, fill_rgb=(0.98, 0.98, 0.98), stroke_rgb=(0.88, 0.88, 0.88), line_width=0.8)
        self.draw_text("Instituição: FinBank Digital", self.margin_x + 10, y - 12, font="F2", size=8, rgb=(0.1, 0.1, 0.1))
        self.draw_text("Equipe Responsável: GRUPO 01 (Infraestrutura)", self.margin_x + 155, y - 12, font="F2", size=8, rgb=(0.1, 0.1, 0.1))
        self.draw_text("Topologia: Router-on-a-Stick", self.margin_x + 380, y - 12, font="F2", size=8, rgb=(0.1, 0.1, 0.1))
        self.draw_text("Arquivo de Projeto: FinBank_Digital_Infraestrutura_Grupo01.pkt", self.margin_x + 10, y - 23, font="F1", size=8, rgb=(0.3, 0.3, 0.3))
        self.draw_text("Serviços: HTTP, DNS, DHCP, Syslog", self.margin_x + 380, y - 23, font="F1", size=8, rgb=(0.3, 0.3, 0.3))

        # 1. Contexto e Problema de Negócio
        y -= 45
        self.draw_text("1. CONTEXTO E PROBLEMA DE NEGÓCIO", self.margin_x, y, font="F2", size=10, rgb=(0.04, 0.15, 0.28))
        self.draw_line(self.margin_x, y - 3, self.margin_x + self.content_w, y - 3, rgb=(0.04, 0.15, 0.28), width=1)
        
        y -= 15
        p1 = "A FinBank Digital opera uma agência física composta por três setores críticos: Atendimento ao Cliente, Operações"
        p2 = "Financeiras e Administração, e Serviços Internos (Data Center Local). A infraestrutura necessitava de uma segmentação"
        p3 = "robusta por VLANs para isolar o tráfego sensível dos terminais financeiros e um sistema educacional de monitoramento"
        p4 = "capaz de detectar indisponibilidades e alertar sobre falhas persistentes em ativos críticos."
        for line in [p1, p2, p3, p4]:
            self.draw_text(line, self.margin_x, y, font="F1", size=8.5, rgb=(0.2, 0.2, 0.2))
            y -= 11

        # 2. Divisão de Responsabilidades (2 Grupos)
        y -= 12
        self.draw_text("2. DIVISÃO DE RESPONSABILIDADES DAS EQUIPES", self.margin_x, y, font="F2", size=10, rgb=(0.04, 0.15, 0.28))
        self.draw_line(self.margin_x, y - 3, self.margin_x + self.content_w, y - 3, rgb=(0.04, 0.15, 0.28), width=1)

        y -= 15
        box_w = (self.content_w - 12) / 2
        # Box Grupo 01
        self.draw_rect(self.margin_x, y - 120, box_w, 120, fill_rgb=(0.96, 0.97, 1.0), stroke_rgb=(0.39, 0.36, 0.95), line_width=1.2)
        self.draw_text("GRUPO 01: INFRAESTRUTURA (Nosso Grupo)", self.margin_x + 8, y - 14, font="F2", size=8.5, rgb=(0.25, 0.20, 0.75))
        self.draw_text("Ambiente: Cisco Packet Tracer v8.x", self.margin_x + 8, y - 26, font="F2", size=7.5, rgb=(0.4, 0.4, 0.4))
        g1_items = [
            "• Montagem física da topologia e cabeamento porta a porta.",
            "• Criação e isolamento das VLANs 10, 20 e 30 no Switch 2960.",
            "• Roteamento Router-on-a-Stick via tronco 802.1Q (Gig0/0 a Gig0/1).",
            "• Configuração de Subinterfaces (.10, .20, .30) e Gateways.",
            "• Configuração dos servidores DHCP no Roteador Cisco 1941.",
            "• Implantação de HTTP (Web), DNS (finbank.local) e Syslog.",
            "• Homologação completa de conectividade e testes de falha."
        ]
        gy = y - 38
        for item in g1_items:
            self.draw_text(item, self.margin_x + 8, gy, font="F1", size=7.5, rgb=(0.15, 0.15, 0.15))
            gy -= 11

        # Box Grupo 02
        gx2 = self.margin_x + box_w + 12
        self.draw_rect(gx2, y - 120, box_w, 120, fill_rgb=(0.98, 0.98, 0.99), stroke_rgb=(0.7, 0.75, 0.85), line_width=1)
        self.draw_text("GRUPO 02: LÓGICA E SOFTWARE (Outro Grupo)", gx2 + 8, y - 14, font="F2", size=8.5, rgb=(0.2, 0.25, 0.35))
        self.draw_text("Ambiente: Python 3 / Script de Monitoramento", gx2 + 8, y - 26, font="F2", size=7.5, rgb=(0.4, 0.4, 0.4))
        g2_items = [
            "• Implementação dos Requisitos Funcionais RF01 ao RF06.",
            "• Cadastro dos ativos conforme tabela de IPs do Grupo 01.",
            "• Execução periódica de verificações de disponibilidade (Ping).",
            "• Regra de 3 falhas consecutivas: Alerta de indisponibilidade.",
            "• Cálculo matemático de Uptime %: (sucessos / total) * 100.",
            "• Priorização de alarmes de ativos Críticos e de Alta criticidade.",
            "• Emissão de relatórios consolidados em console e arquivo."
        ]
        gy2 = y - 38
        for item in g2_items:
            self.draw_text(item, gx2 + 8, gy2, font="F1", size=7.5, rgb=(0.2, 0.2, 0.2))
            gy2 -= 11

        # 3. Arquitetura da Solução
        y -= 142
        self.draw_text("3. ARQUITETURA DE REDE E DIMENSIONAMENTO", self.margin_x, y, font="F2", size=10, rgb=(0.04, 0.15, 0.28))
        self.draw_line(self.margin_x, y - 3, self.margin_x + self.content_w, y - 3, rgb=(0.04, 0.15, 0.28), width=1)
        
        y -= 16
        t_items = [
            ("Roteador Core:", "Cisco 1941 / Concentrador de Gateways e Servidor DHCP para as estações."),
            ("Switch Central:", "Cisco Catalyst 2960-24TT / Gerenciamento de VLANs, Portfast e Tronco 802.1Q."),
            ("Servidor Aplicação:", "Server-PT (SRV-WEB-BANCO) / Hospeda o portal Web institucional e o servidor DNS."),
            ("Servidor Eventos:", "Server-PT (SRV-MONITOR) / Servidor interno de coleta de mensagens Syslog."),
            ("Estações Clientes:", "4x PC-PT distribuídos nas VLANs de Atendimento e Operações Financeiras.")
        ]
        for t_label, t_desc in t_items:
            self.draw_text(t_label, self.margin_x + 5, y, font="F2", size=8, rgb=(0.1, 0.25, 0.45))
            self.draw_text(t_desc, self.margin_x + 115, y, font="F1", size=8, rgb=(0.2, 0.2, 0.2))
            y -= 13

        # Box Destaque de Homologação
        y -= 8
        self.draw_rect(self.margin_x, y - 32, self.content_w, 32, fill_rgb=(0.94, 0.99, 0.96), stroke_rgb=(0.20, 0.70, 0.40), line_width=1)
        self.draw_text("RESULTADO DA ENTREGA DO GRUPO 01:", self.margin_x + 10, y - 13, font="F2", size=8.5, rgb=(0.05, 0.50, 0.25))
        self.draw_text("Todas as estações de trabalho obtiveram IPs válidos via DHCP, o roteamento inter-VLAN operou com 0% de perda,", self.margin_x + 10, y - 24, font="F1", size=7.8, rgb=(0.15, 0.35, 0.20))
        self.draw_text("e a página http://finbank.local foi carregada com sucesso a partir dos navegadores dos clientes.", self.margin_x + 10, y - 33, font="F1", size=7.8, rgb=(0.15, 0.35, 0.20))


        # ==========================================
        # PÁGINA 2: TOPOLOGIA, CABEAMENTO E TABELA IP
        # ==========================================
        self.new_page()
        self.add_header(2, 4)

        y = self.height - 45
        self.draw_text("4. ESQUEMA VISUAL DA TOPOLOGIA (CISCO PACKET TRACER)", self.margin_x, y, font="F2", size=10, rgb=(0.04, 0.15, 0.28))
        self.draw_line(self.margin_x, y - 3, self.margin_x + self.content_w, y - 3, rgb=(0.04, 0.15, 0.28), width=1)

        # Diagrama ASCII Box
        y -= 14
        diag_lines = [
            "                                   +--------------------------+",
            "                                   |        R-FINBANK         |",
            "                                   |   Roteador Cisco 1941    |",
            "                                   +------------+-------------+",
            "                                                | Gig0/0",
            "                                                | [Enlace Tronco 802.1Q]",
            "                                                | Gig0/1",
            "                                   +------------+-------------+",
            "                                   |        SW-FINBANK        |",
            "                                   |    Switch Cisco 2960     |",
            "                                   +---+----------+---------+-+",
            "                                       |          |         |",
            "            +--------------------------+          |         +--------------------------+",
            "            | Fa0/1 e Fa0/2                       | Fa0/6 e Fa0/7                      | Fa0/11 e Fa0/12",
            "    +-------v------------------+       +----------v---------------+         +----------v---------------+",
            "    |    SETOR ATENDIMENTO     |       |    OPERACOES & ADMIN     |         |   SERVIDORES / DATA CTR  |",
            "    |        (VLAN 10)         |       |        (VLAN 20)         |         |        (VLAN 30)         |",
            "    | [PC-ATEND-01]            |       | [PC-OPER-01] (Caixa)     |         | [SRV-WEB-BANCO]          |",
            "    | IP: 192.168.10.11 (DHCP) |       | IP: 192.168.20.11 (DHCP) |         | IP: 192.168.30.10 (Fix)  |",
            "    | [PC-ATEND-02]            |       | [PC-ADMIN-01]            |         | [SRV-MONITOR]            |",
            "    | IP: 192.168.10.12 (DHCP) |       | IP: 192.168.20.12 (DHCP) |         | IP: 192.168.30.20 (Fix)  |",
            "    | Gateway: 192.168.10.1    |       | Gateway: 192.168.20.1    |         | Gateway: 192.168.30.1    |",
            "    +--------------------------+       +--------------------------+         +--------------------------+"
        ]
        self.draw_rect(self.margin_x, y - 180, self.content_w, 180, fill_rgb=(0.97, 0.98, 0.99), stroke_rgb=(0.80, 0.85, 0.90), line_width=1)
        dy = y - 12
        for dline in diag_lines:
            self.draw_text(dline, self.margin_x + 12, dy, font="F3", size=7.2, rgb=(0.10, 0.15, 0.25))
            dy -= 7.4

        # 5. Mapeamento de Portas e Cabeamento Físico
        y -= 195
        self.draw_text("5. MAPEAMENTO DE PORTAS E CABEAMENTO FÍSICO (CABO DIRETO)", self.margin_x, y, font="F2", size=10, rgb=(0.04, 0.15, 0.28))
        self.draw_line(self.margin_x, y - 3, self.margin_x + self.content_w, y - 3, rgb=(0.04, 0.15, 0.28), width=1)

        y -= 14
        cables = [
            ("R-FINBANK (Gig0/0)", "SW-FINBANK (Gig0/1)", "Enlace Tronco 802.1Q (Transporta VLANs 10, 20 e 30)"),
            ("SW-FINBANK (Fa0/1)", "PC-ATEND-01 (Fa0)", "Porta de Acesso - VLAN 10 (Atendimento ao Cliente)"),
            ("SW-FINBANK (Fa0/2)", "PC-ATEND-02 (Fa0)", "Porta de Acesso - VLAN 10 (Atendimento ao Cliente)"),
            ("SW-FINBANK (Fa0/6)", "PC-OPER-01 (Fa0)", "Porta de Acesso - VLAN 20 (Operações Financeiras / Caixa)"),
            ("SW-FINBANK (Fa0/7)", "PC-ADMIN-01 (Fa0)", "Porta de Acesso - VLAN 20 (Administração e Gerência)"),
            ("SW-FINBANK (Fa0/11)", "SRV-WEB-BANCO (Fa0)", "Porta de Acesso - VLAN 30 (Servidor Web HTTP e DNS)"),
            ("SW-FINBANK (Fa0/12)", "SRV-MONITOR (Fa0)", "Porta de Acesso - VLAN 30 (Servidor de Monitoramento Syslog)")
        ]
        # Header tabela cabos
        self.draw_rect(self.margin_x, y - 14, self.content_w, 14, fill_rgb=(0.10, 0.20, 0.35))
        self.draw_text("Origem (Equipamento / Porta)", self.margin_x + 6, y - 10, font="F2", size=7.5, rgb=(1,1,1))
        self.draw_text("Destino (Equipamento / Porta)", self.margin_x + 160, y - 10, font="F2", size=7.5, rgb=(1,1,1))
        self.draw_text("Função e Modo da Porta", self.margin_x + 315, y - 10, font="F2", size=7.5, rgb=(1,1,1))

        cy = y - 14
        for idx, (c_orig, c_dest, c_func) in enumerate(cables):
            bg = (0.96, 0.97, 0.98) if idx % 2 == 0 else (1, 1, 1)
            self.draw_rect(self.margin_x, cy - 12, self.content_w, 12, fill_rgb=bg, stroke_rgb=(0.85, 0.85, 0.85), line_width=0.5)
            self.draw_text(c_orig, self.margin_x + 6, cy - 9, font="F2", size=7, rgb=(0.1, 0.2, 0.3))
            self.draw_text(c_dest, self.margin_x + 160, cy - 9, font="F1", size=7, rgb=(0.2, 0.2, 0.2))
            self.draw_text(c_func, self.margin_x + 315, cy - 9, font="F1", size=7, rgb=(0.2, 0.2, 0.2))
            cy -= 12

        # 6. Tabela Oficial de Endereçamento e Criticidade
        y = cy - 18
        self.draw_text("6. TABELA OFICIAL DE ENDEREÇAMENTO IPV4 E MATRIZ DE CRITICIDADE", self.margin_x, y, font="F2", size=10, rgb=(0.04, 0.15, 0.28))
        self.draw_line(self.margin_x, y - 3, self.margin_x + self.content_w, y - 3, rgb=(0.04, 0.15, 0.28), width=1)

        y -= 14
        # Header tabela IP
        self.draw_rect(self.margin_x, y - 14, self.content_w, 14, fill_rgb=(0.10, 0.20, 0.35))
        self.draw_text("Dispositivo", self.margin_x + 4, y - 10, font="F2", size=7.2, rgb=(1,1,1))
        self.draw_text("Segmento / VLAN", self.margin_x + 85, y - 10, font="F2", size=7.2, rgb=(1,1,1))
        self.draw_text("Endereço IPv4", self.margin_x + 175, y - 10, font="F2", size=7.2, rgb=(1,1,1))
        self.draw_text("Gateway", self.margin_x + 255, y - 10, font="F2", size=7.2, rgb=(1,1,1))
        self.draw_text("Criticidade", self.margin_x + 335, y - 10, font="F2", size=7.2, rgb=(1,1,1))
        self.draw_text("Serviço / Aplicação", self.margin_x + 405, y - 10, font="F2", size=7.2, rgb=(1,1,1))

        ip_rows = [
            ("R-FINBANK", "Gateway Central", "192.168.10/20/30.1", "—", "CRÍTICA", (0.9, 0.1, 0.1), "Roteamento 802.1Q / DHCP"),
            ("SRV-WEB-BANCO", "VLAN 30 (Servidores)", "192.168.30.10 (Est.)", "192.168.30.1", "CRÍTICA", (0.9, 0.1, 0.1), "HTTP (80) & DNS finbank.local"),
            ("SRV-MONITOR", "VLAN 30 (Servidores)", "192.168.30.20 (Est.)", "192.168.30.1", "NORMAL", (0.1, 0.6, 0.3), "Syslog Server / Eventos"),
            ("PC-OPER-01", "VLAN 20 (Operações)", "192.168.20.11 (DHCP)", "192.168.20.1", "ALTA", (0.8, 0.5, 0.0), "Terminal Financeiro de Caixa"),
            ("PC-ADMIN-01", "VLAN 20 (Admin)", "192.168.20.12 (DHCP)", "192.168.20.1", "NORMAL", (0.1, 0.6, 0.3), "Gestão Operacional"),
            ("PC-ATEND-01", "VLAN 10 (Atendimento)", "192.168.10.11 (DHCP)", "192.168.10.1", "NORMAL", (0.1, 0.6, 0.3), "Atendimento Presencial"),
            ("PC-ATEND-02", "VLAN 10 (Atendimento)", "192.168.10.12 (DHCP)", "192.168.10.1", "NORMAL", (0.1, 0.6, 0.3), "Atendimento Presencial")
        ]

        iy = y - 14
        for idx, (d_name, d_vlan, d_ip, d_gw, d_crit, c_color, d_serv) in enumerate(ip_rows):
            bg = (0.97, 0.98, 0.99) if idx % 2 == 0 else (1, 1, 1)
            self.draw_rect(self.margin_x, iy - 13, self.content_w, 13, fill_rgb=bg, stroke_rgb=(0.85, 0.85, 0.85), line_width=0.5)
            self.draw_text(d_name, self.margin_x + 4, iy - 10, font="F2", size=7, rgb=(0.1, 0.15, 0.25))
            self.draw_text(d_vlan, self.margin_x + 85, iy - 10, font="F1", size=7, rgb=(0.25, 0.25, 0.25))
            self.draw_text(d_ip, self.margin_x + 175, iy - 10, font="F2", size=7, rgb=(0.05, 0.25, 0.55))
            self.draw_text(d_gw, self.margin_x + 255, iy - 10, font="F1", size=7, rgb=(0.3, 0.3, 0.3))
            self.draw_text(d_crit, self.margin_x + 335, iy - 10, font="F2", size=7, rgb=c_color)
            self.draw_text(d_serv, self.margin_x + 405, iy - 10, font="F1", size=7, rgb=(0.2, 0.2, 0.2))
            iy -= 13


        # ==========================================
        # PÁGINA 3: CONFIGURAÇÕES EXATAS CISCO IOS
        # ==========================================
        self.new_page()
        self.add_header(3, 4)

        y = self.height - 45
        self.draw_text("7. CONFIGURAÇÃO COMPLETA APLICADA NO SWITCH CATALYST 2960", self.margin_x, y, font="F2", size=10, rgb=(0.04, 0.15, 0.28))
        self.draw_line(self.margin_x, y - 3, self.margin_x + self.content_w, y - 3, rgb=(0.04, 0.15, 0.28), width=1)

        y -= 12
        sw_code = [
            "enable",
            "configure terminal",
            "hostname SW-FINBANK",
            "! 1. Criacao das 3 VLANs segmentadas da instituicao",
            "vlan 10",
            " name ATENDIMENTO",
            "exit",
            "vlan 20",
            " name OPERACOES_ADMIN",
            "exit",
            "vlan 30",
            " name SERVIDORES",
            "exit",
            "! 2. Associacao das Portas de Acesso com Spanning-Tree PortFast",
            "interface range fastEthernet 0/1 - 5",
            " switchport mode access",
            " switchport access vlan 10",
            " spanning-tree portfast",
            "exit",
            "interface range fastEthernet 0/6 - 10",
            " switchport mode access",
            " switchport access vlan 20",
            " spanning-tree portfast",
            "exit",
            "interface range fastEthernet 0/11 - 15",
            " switchport mode access",
            " switchport access vlan 30",
            " spanning-tree portfast",
            "exit",
            "! 3. Configuracao do Enlace Tronco (802.1Q) ligado a GigabitEthernet 0/0 do Roteador",
            "interface gigabitEthernet 0/1",
            " switchport mode trunk",
            " switchport trunk allowed vlan all",
            " no shutdown",
            " description LINK_TRUNK_ROUTER",
            "exit",
            "end",
            "write memory"
        ]
        sw_box_h = len(sw_code) * 7.6 + 8
        self.draw_rect(self.margin_x, y - sw_box_h, self.content_w, sw_box_h, fill_rgb=(0.08, 0.11, 0.16), stroke_rgb=(0.2, 0.25, 0.35), line_width=1)
        cy = y - 10
        for cline in sw_code:
            color = (0.4, 0.75, 0.5) if cline.startswith("!") else (0.9, 0.95, 1.0)
            font = "F4" if cline.startswith("hostname") or cline.startswith("switchport mode") else "F3"
            self.draw_text(cline, self.margin_x + 8, cy, font=font, size=6.8, rgb=color)
            cy -= 7.6

        y = y - sw_box_h - 16
        self.draw_text("8. CONFIGURAÇÃO COMPLETA APLICADA NO ROTEADOR CISCO 1941", self.margin_x, y, font="F2", size=10, rgb=(0.04, 0.15, 0.28))
        self.draw_line(self.margin_x, y - 3, self.margin_x + self.content_w, y - 3, rgb=(0.04, 0.15, 0.28), width=1)

        y -= 12
        rt_code = [
            "enable",
            "configure terminal",
            "hostname R-FINBANK",
            "service dhcp",
            "! 1. Habilitacao da Interface Fisica Principal (sem IP)",
            "interface gigabitEthernet 0/0",
            " no shutdown",
            "exit",
            "! 2. Subinterfaces dot1Q e Enderecamento dos Gateways de cada VLAN",
            "interface gigabitEthernet 0/0.10",
            " encapsulation dot1Q 10",
            " ip address 192.168.10.1 255.255.255.0",
            " description GATEWAY_ATENDIMENTO",
            "exit",
            "interface gigabitEthernet 0/0.20",
            " encapsulation dot1Q 20",
            " ip address 192.168.20.1 255.255.255.0",
            " description GATEWAY_OPERACOES_ADMIN",
            "exit",
            "interface gigabitEthernet 0/0.30",
            " encapsulation dot1Q 30",
            " ip address 192.168.30.1 255.255.255.0",
            " description GATEWAY_SERVIDORES",
            "exit",
            "! 3. Exclusao dos IPs de Gateways e Servidores do escopo DHCP",
            "ip dhcp excluded-address 192.168.10.1 192.168.10.10",
            "ip dhcp excluded-address 192.168.20.1 192.168.20.10",
            "! 4. Pools de Distribuicao Dinamica de IP (VLAN 10 e VLAN 20)",
            "ip dhcp pool POOL_ATENDIMENTO",
            " network 192.168.10.0 255.255.255.0",
            " default-router 192.168.10.1",
            " dns-server 192.168.30.10",
            "exit",
            "ip dhcp pool POOL_OPERACOES",
            " network 192.168.20.0 255.255.255.0",
            " default-router 192.168.20.1",
            " dns-server 192.168.30.10",
            "exit",
            "end",
            "write memory"
        ]
        rt_box_h = len(rt_code) * 7.5 + 8
        self.draw_rect(self.margin_x, y - rt_box_h, self.content_w, rt_box_h, fill_rgb=(0.08, 0.11, 0.16), stroke_rgb=(0.2, 0.25, 0.35), line_width=1)
        cy = y - 10
        for rline in rt_code:
            color = (0.4, 0.75, 0.5) if rline.startswith("!") else (0.9, 0.95, 1.0)
            font = "F4" if rline.startswith("hostname") or rline.startswith("encapsulation") or rline.startswith("ip dhcp pool") else "F3"
            self.draw_text(rline, self.margin_x + 8, cy, font=font, size=6.7, rgb=color)
            cy -= 7.5


        # ==========================================
        # PÁGINA 4: SERVIÇOS, TESTES E HANDOVER
        # ==========================================
        self.new_page()
        self.add_header(4, 4)

        y = self.height - 45
        self.draw_text("9. CONFIGURAÇÃO DOS SERVIDORES E SERVIÇOS DE REDE", self.margin_x, y, font="F2", size=10, rgb=(0.04, 0.15, 0.28))
        self.draw_line(self.margin_x, y - 3, self.margin_x + self.content_w, y - 3, rgb=(0.04, 0.15, 0.28), width=1)

        y -= 14
        s_box_w = (self.content_w - 12) / 2
        # Servidor Web
        self.draw_rect(self.margin_x, y - 75, s_box_w, 75, fill_rgb=(0.98, 0.98, 1.0), stroke_rgb=(0.8, 0.85, 0.95), line_width=1)
        self.draw_text("SRV-WEB-BANCO (192.168.30.10)", self.margin_x + 8, y - 12, font="F2", size=8, rgb=(0.05, 0.2, 0.45))
        self.draw_text("• Servico HTTP / HTTPS: Marcado como ON.", self.margin_x + 8, y - 24, font="F1", size=7.2, rgb=(0.2, 0.2, 0.2))
        self.draw_text("• Pagina index.html: FinBank Digital - Servidor Central Ativo.", self.margin_x + 8, y - 35, font="F1", size=7.2, rgb=(0.2, 0.2, 0.2))
        self.draw_text("• Servico DNS: Marcado como ON.", self.margin_x + 8, y - 46, font="F1", size=7.2, rgb=(0.2, 0.2, 0.2))
        self.draw_text("• Registro Tipo A: finbank.local -> 192.168.30.10.", self.margin_x + 8, y - 57, font="F2", size=7.2, rgb=(0.1, 0.45, 0.25))
        self.draw_text("• Default Gateway: 192.168.30.1 | Subnet: 255.255.255.0", self.margin_x + 8, y - 68, font="F1", size=7.2, rgb=(0.3, 0.3, 0.3))

        # Servidor Monitor
        sx2 = self.margin_x + s_box_w + 12
        self.draw_rect(sx2, y - 75, s_box_w, 75, fill_rgb=(0.98, 0.98, 1.0), stroke_rgb=(0.8, 0.85, 0.95), line_width=1)
        self.draw_text("SRV-MONITOR (192.168.30.20)", sx2 + 8, y - 12, font="F2", size=8, rgb=(0.05, 0.2, 0.45))
        self.draw_text("• Endereco IP: 192.168.30.20 (Estatico).", sx2 + 8, y - 24, font="F1", size=7.2, rgb=(0.2, 0.2, 0.2))
        self.draw_text("• Default Gateway: 192.168.30.1 | DNS: 192.168.30.10.", sx2 + 8, y - 35, font="F1", size=7.2, rgb=(0.2, 0.2, 0.2))
        self.draw_text("• Servico Syslog: Marcado como ON.", sx2 + 8, y - 46, font="F2", size=7.2, rgb=(0.1, 0.45, 0.25))
        self.draw_text("• Funcao: Receptor de logs de conectividade e alertas.", sx2 + 8, y - 57, font="F1", size=7.2, rgb=(0.2, 0.2, 0.2))
        self.draw_text("• Ponto de integracao com a ferramenta do Grupo 02.", sx2 + 8, y - 68, font="F1", size=7.2, rgb=(0.3, 0.3, 0.3))

        # 10. Troubleshooting Resolvido
        y = y - 90
        self.draw_text("10. RELATÓRIO DE TROUBLESHOOTING E RESOLUÇÃO DE INCIDENTES", self.margin_x, y, font="F2", size=10, rgb=(0.04, 0.15, 0.28))
        self.draw_line(self.margin_x, y - 3, self.margin_x + self.content_w, y - 3, rgb=(0.04, 0.15, 0.28), width=1)

        y -= 13
        # Box Incidente 1
        self.draw_rect(self.margin_x, y - 38, self.content_w, 38, fill_rgb=(0.99, 0.96, 0.96), stroke_rgb=(0.9, 0.6, 0.6), line_width=0.8)
        self.draw_text("Incidente 1: Seta Vermelha no Link R-FINBANK <-> SW-FINBANK", self.margin_x + 8, y - 11, font="F2", size=7.5, rgb=(0.7, 0.1, 0.1))
        self.draw_text("Causa: Interfaces de roteadores Cisco iniciam desativadas por padrao (administratively down).", self.margin_x + 8, y - 21, font="F1", size=7.2, rgb=(0.25, 0.25, 0.25))
        self.draw_text("Solucao: Execucao de 'no shutdown' na interface fisica GigabitEthernet0/0 e porta Gig0/1 do switch.", self.margin_x + 8, y - 31, font="F2", size=7.2, rgb=(0.05, 0.5, 0.2))

        y -= 43
        # Box Incidente 2
        self.draw_rect(self.margin_x, y - 38, self.content_w, 38, fill_rgb=(0.99, 0.96, 0.96), stroke_rgb=(0.9, 0.6, 0.6), line_width=0.8)
        self.draw_text("Incidente 2: Estacoes Clientes Obtendo IP 169.254.x.x (APIPA)", self.margin_x + 8, y - 11, font="F2", size=7.5, rgb=(0.7, 0.1, 0.1))
        self.draw_text("Causa: Conflito de sintaxe na CLI com comandos 'enable' encadeados, deixando as subinterfaces sem dot1Q.", self.margin_x + 8, y - 21, font="F1", size=7.2, rgb=(0.25, 0.25, 0.25))
        self.draw_text("Solucao: Aplicacao limpa das subinterfaces .10, .20 e dos pools DHCP POOL_ATENDIMENTO e POOL_OPERACOES.", self.margin_x + 8, y - 31, font="F2", size=7.2, rgb=(0.05, 0.5, 0.2))

        # 11. Bateria de Testes Homologados
        y -= 48
        self.draw_text("11. BATERIA DE TESTES E HOMOLOGAÇÃO DE FUNCIONAMENTO", self.margin_x, y, font="F2", size=10, rgb=(0.04, 0.15, 0.28))
        self.draw_line(self.margin_x, y - 3, self.margin_x + self.content_w, y - 3, rgb=(0.04, 0.15, 0.28), width=1)

        y -= 14
        # Header testes
        self.draw_rect(self.margin_x, y - 13, self.content_w, 13, fill_rgb=(0.10, 0.20, 0.35))
        self.draw_text("Teste", self.margin_x + 4, y - 9, font="F2", size=7, rgb=(1,1,1))
        self.draw_text("Origem", self.margin_x + 80, y - 9, font="F2", size=7, rgb=(1,1,1))
        self.draw_text("Destino", self.margin_x + 160, y - 9, font="F2", size=7, rgb=(1,1,1))
        self.draw_text("Protocolo", self.margin_x + 250, y - 9, font="F2", size=7, rgb=(1,1,1))
        self.draw_text("Resultado Obtido", self.margin_x + 330, y - 9, font="F2", size=7, rgb=(1,1,1))
        self.draw_text("Status", self.margin_x + 460, y - 9, font="F2", size=7, rgb=(1,1,1))

        t_rows = [
            ("DHCP Lease", "R-FINBANK", "Todas as estacoes", "UDP 67/68", "IPs 192.168.10.x e 20.x recebidos com sucesso", "APROVADO", (0.05, 0.55, 0.25)),
            ("Gateway Ping", "PC-ATEND-01", "192.168.10.1", "ICMP Echo", "0% de perda, tempo < 1ms", "APROVADO", (0.05, 0.55, 0.25)),
            ("Inter-VLAN", "PC-ATEND-01", "192.168.30.10", "802.1Q / ICMP", "Comunicacao cruzando subinterfaces .10 e .30", "APROVADO", (0.05, 0.55, 0.25)),
            ("Resolucao DNS", "PC-OPER-01", "finbank.local", "UDP 53", "Resolvido para o IP 192.168.30.10", "APROVADO", (0.05, 0.55, 0.25)),
            ("Web Banking", "PC-OPER-01", "http://finbank.local", "TCP 80 (HTTP)", "Portal FinBank carregado no Web Browser", "APROVADO", (0.05, 0.55, 0.25)),
            ("Falha Controlada", "SW-FINBANK", "Porta Fa0/11", "Link State", "Shutdown simulando interrupcao para o monitor", "APROVADO", (0.05, 0.55, 0.25))
        ]
        ty = y - 13
        for idx, (t_name, t_orig, t_dest, t_prot, t_res, t_st, t_st_col) in enumerate(t_rows):
            bg = (0.97, 0.98, 0.99) if idx % 2 == 0 else (1, 1, 1)
            self.draw_rect(self.margin_x, ty - 11, self.content_w, 11, fill_rgb=bg, stroke_rgb=(0.85, 0.85, 0.85), line_width=0.5)
            self.draw_text(t_name, self.margin_x + 4, ty - 8, font="F2", size=6.8, rgb=(0.1, 0.15, 0.25))
            self.draw_text(t_orig, self.margin_x + 80, ty - 8, font="F1", size=6.8, rgb=(0.2, 0.2, 0.2))
            self.draw_text(t_dest, self.margin_x + 160, ty - 8, font="F1", size=6.8, rgb=(0.2, 0.2, 0.2))
            self.draw_text(t_prot, self.margin_x + 250, ty - 8, font="F1", size=6.8, rgb=(0.2, 0.2, 0.2))
            self.draw_text(t_res, self.margin_x + 330, ty - 8, font="F1", size=6.8, rgb=(0.15, 0.15, 0.15))
            self.draw_text(t_st, self.margin_x + 460, ty - 8, font="F2", size=6.8, rgb=t_st_col)
            ty -= 11

        # 12. Termo de Handover Final
        y = ty - 16
        self.draw_rect(self.margin_x, y - 36, self.content_w, 36, fill_rgb=(0.95, 0.97, 1.0), stroke_rgb=(0.3, 0.5, 0.8), line_width=1)
        self.draw_text("12. TERMO DE ENTREGA (HANDOVER) PARA O GRUPO 02:", self.margin_x + 8, y - 12, font="F2", size=8.2, rgb=(0.05, 0.2, 0.5))
        self.draw_text("• A infraestrutura fisica e logica esta homologada e pronta no arquivo 'FinBank_Digital_Infraestrutura_Grupo01.pkt'.", self.margin_x + 8, y - 22, font="F1", size=7.2, rgb=(0.2, 0.2, 0.2))
        self.draw_text("• O Grupo 02 pode iniciar a execucao do software 'monitor_finbank.py' utilizando os IPs e niveis de criticidade da Secao 6.", self.margin_x + 8, y - 32, font="F1", size=7.2, rgb=(0.2, 0.2, 0.2))

        self.save()

    def save(self):
        if self.current_stream:
            self._finish_page()

        font1 = "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"
        font2 = "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>"
        font3 = "<< /Type /Font /Subtype /Type1 /BaseFont /Courier >>"
        font4 = "<< /Type /Font /Subtype /Type1 /BaseFont /Courier-Bold >>"

        font1_id = self._add_object(font1)
        font2_id = self._add_object(font2)
        font3_id = self._add_object(font3)
        font4_id = self._add_object(font4)

        page_obj_ids = []
        for stream_id in self.pages:
            page_obj = f"""<<
  /Type /Page
  /Parent 2 0 R
  /MediaBox [0 0 {self.width:.2f} {self.height:.2f}]
  /Contents {stream_id} 0 R
  /Resources <<
    /Font <<
      /F1 {font1_id} 0 R
      /F2 {font2_id} 0 R
      /F3 {font3_id} 0 R
      /F4 {font4_id} 0 R
    >>
  >>
>>"""
            page_obj_ids.append(self._add_object(page_obj))

        kids_str = " ".join([f"{pid} 0 R" for pid in page_obj_ids])
        pages_obj = f"""<<
  /Type /Pages
  /Kids [{kids_str}]
  /Count {len(page_obj_ids)}
>>"""
        pages_id = self._add_object(pages_obj)

        catalog_obj = f"""<<
  /Type /Catalog
  /Pages {pages_id} 0 R
>>"""
        catalog_id = self._add_object(catalog_obj)

        with open(self.filename, 'wb') as f:
            f.write(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
            offsets = []
            
            for i, obj_str in enumerate(self.objects, 1):
                offsets.append(f.tell())
                f.write(f"{i} 0 obj\n{obj_str}\nendobj\n".encode('latin1'))

            xref_pos = f.tell()
            f.write(f"xref\n0 {len(self.objects) + 1}\n0000000000 65535 f \n".encode('latin1'))
            for off in offsets:
                f.write(f"{off:010d} 00000 n \n".encode('latin1'))

            trailer = f"""trailer
<<
  /Size {len(self.objects) + 1}
  /Root {catalog_id} 0 R
>>
startxref
{xref_pos}
%%EOF\n"""
            f.write(trailer.encode('latin1'))

if __name__ == "__main__":
    out_pdf = r"C:\Users\jamerson.albuquerque\.gemini\antigravity\scratch\finbank_digital\FinBank_Digital_Relatorio_Final.pdf"
    gerador = RelatorioPDF(out_pdf)
    gerador.build_pdf()
    print("PDF Oficial gerado com sucesso em:", out_pdf)
