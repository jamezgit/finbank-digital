import os
import sys

class DocumentacaoTecnicaPDF:
    def __init__(self, filename):
        self.filename = filename
        self.objects = []
        self.pages = []
        self.current_stream = []
        self.width = 595.28   # A4 largura em pontos pt
        self.height = 841.89  # A4 altura em pontos pt
        self.margin_x = 36    # Margem lateral (~12.7mm)
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
        # Header banner escuro
        self.draw_rect(self.margin_x, self.height - 28, self.content_w, 18, fill_rgb=(0.04, 0.15, 0.28))
        self.draw_text("FINBANK DIGITAL  •  PROJETO 02 — TÓPICO 1: DOCUMENTAÇÃO TÉCNICA", self.margin_x + 8, self.height - 23, font="F2", size=7.5, rgb=(1,1,1))
        self.draw_text("PADRÃO EXECUTIVO & ACADÊMICO", self.width - self.margin_x - 145, self.height - 23, font="F2", size=7.5, rgb=(0.35, 0.85, 0.70))
        
        # Footer
        self.draw_line(self.margin_x, 26, self.width - self.margin_x, 26, rgb=(0.8,0.8,0.8), width=0.8)
        self.draw_text("Infraestrutura Cisco Packet Tracer & Sistema de Monitoramento Python | FinBank Digital", self.margin_x, 16, font="F1", size=7.5, rgb=(0.4,0.4,0.4))
        self.draw_text(f"Página {page_num} de {total_pages}", self.width - self.margin_x - 55, 16, font="F2", size=7.5, rgb=(0.2,0.2,0.2))

    def build_pdf(self):
        # =========================================================================
        # PÁGINA 1: IDENTIFICAÇÃO, CONTEXTUALIZAÇÃO E PROBLEMA IDENTIFICADO
        # =========================================================================
        self.new_page()
        self.add_header(1, 4)

        # 1. Bloco de Título Principal
        y = self.height - 52
        self.draw_rect(self.margin_x, y - 56, self.content_w, 56, fill_rgb=(0.95, 0.97, 1.0), stroke_rgb=(0.75, 0.82, 0.95), line_width=1)
        self.draw_text("PROJETO 02 — FINBANK DIGITAL: DOCUMENTAÇÃO TÉCNICA", self.margin_x + 12, y - 18, font="F2", size=13, rgb=(0.04, 0.15, 0.28))
        self.draw_text("Tópico 1: Especificação de Requisitos, Escopo, Regras de Negócio e Arquitetura", self.margin_x + 12, y - 33, font="F1", size=9.5, rgb=(0.25, 0.35, 0.50))
        self.draw_text("STATUS: ESPECIFICAÇÃO TÉCNICA E HOMOLOGAÇÃO 100% OPERACIONAL", self.margin_x + 12, y - 47, font="F2", size=8, rgb=(0.05, 0.55, 0.35))

        # 1.1 Identificação do Projeto e Integrantes
        y -= 68
        self.draw_text("1.1 IDENTIFICAÇÃO DO PROJETO E INTEGRANTES", self.margin_x, y, font="F2", size=10, rgb=(0.04, 0.15, 0.28))
        self.draw_line(self.margin_x, y - 3, self.margin_x + self.content_w, y - 3, rgb=(0.04, 0.15, 0.28), width=1)

        y -= 14
        self.draw_rect(self.margin_x, y - 24, self.content_w, 24, fill_rgb=(0.98, 0.98, 0.98), stroke_rgb=(0.88, 0.88, 0.88), line_width=0.8)
        self.draw_text("Projeto: FinBank Digital (Projeto 02)", self.margin_x + 8, y - 10, font="F2", size=7.8, rgb=(0.1, 0.1, 0.1))
        self.draw_text("Disciplina: Redes de Computadores / Engenharia", self.margin_x + 185, y - 10, font="F1", size=7.8, rgb=(0.2, 0.2, 0.2))
        self.draw_text("Período: 2026.2", self.margin_x + 430, y - 10, font="F2", size=7.8, rgb=(0.1, 0.1, 0.1))
        self.draw_text("Modelo: Segregação em Duas Equipes Técnicas (Infraestrutura vs. Software de Monitoramento)", self.margin_x + 8, y - 20, font="F1", size=7.5, rgb=(0.3, 0.3, 0.3))

        y -= 32
        box_w = (self.content_w - 10) / 2
        # Box Grupo 01
        self.draw_rect(self.margin_x, y - 64, box_w, 64, fill_rgb=(0.96, 0.98, 1.0), stroke_rgb=(0.35, 0.45, 0.85), line_width=1)
        self.draw_text("GRUPO 01 — INFRAESTRUTURA DE REDE (Cisco Packet Tracer)", self.margin_x + 8, y - 12, font="F2", size=8, rgb=(0.15, 0.25, 0.65))
        self.draw_text("• Liderança Técnica / Infra: Jamerson Albuquerque", self.margin_x + 8, y - 24, font="F2", size=7.5, rgb=(0.2, 0.2, 0.2))
        self.draw_text("• Equipe de Redes: [Integrante 02] | [Integrante 03] | [Integrante 04]", self.margin_x + 8, y - 35, font="F1", size=7.2, rgb=(0.3, 0.3, 0.3))
        self.draw_text("• Atribuições: Topologia, VLANs 10/20/30, Roteador 1941, Switch 2960,", self.margin_x + 8, y - 46, font="F1", size=7.2, rgb=(0.3, 0.3, 0.3))
        self.draw_text("  enlace tronco 802.1Q, pools DHCP, HTTP, DNS e arquivo .pkt.", self.margin_x + 8, y - 56, font="F1", size=7.2, rgb=(0.3, 0.3, 0.3))

        # Box Grupo 02
        gx2 = self.margin_x + box_w + 10
        self.draw_rect(gx2, y - 64, box_w, 64, fill_rgb=(0.98, 0.98, 0.99), stroke_rgb=(0.7, 0.75, 0.85), line_width=1)
        self.draw_text("GRUPO 02 — SOFTWARE DE MONITORAMENTO (Python 3)", gx2 + 8, y - 12, font="F2", size=8, rgb=(0.2, 0.25, 0.35))
        self.draw_text("• Equipe de Desenvolvimento: [Integrante 01] | [Integrante 02]", gx2 + 8, y - 24, font="F1", size=7.5, rgb=(0.2, 0.2, 0.2))
        self.draw_text("• Integrantes Suporte Lógica: [Integrante 03] | [Integrante 04]", gx2 + 8, y - 35, font="F1", size=7.2, rgb=(0.3, 0.3, 0.3))
        self.draw_text("• Atribuições: Requisitos RF01 a RF06, testes periódicos ICMP Ping,", gx2 + 8, y - 46, font="F1", size=7.2, rgb=(0.3, 0.3, 0.3))
        self.draw_text("  regra das 3 falhas consecutivas, Uptime % e relatórios de alarmes.", gx2 + 8, y - 56, font="F1", size=7.2, rgb=(0.3, 0.3, 0.3))

        # 1.2 Introdução e Contextualização do Cenário Empresarial
        y -= 78
        self.draw_text("1.2 INTRODUÇÃO E CONTEXTUALIZAÇÃO DO CENÁRIO EMPRESARIAL", self.margin_x, y, font="F2", size=10, rgb=(0.04, 0.15, 0.28))
        self.draw_line(self.margin_x, y - 3, self.margin_x + self.content_w, y - 3, rgb=(0.04, 0.15, 0.28), width=1)

        y -= 14
        p1 = "A FinBank Digital opera uma agência física moderna, que combina serviços de alta tecnologia com pontos de atendimento presencial."
        p2 = "A infraestrutura da agência atende a três macrosetores estratégicos que dependem de alta disponibilidade de rede:"
        for line in [p1, p2]:
            self.draw_text(line, self.margin_x, y, font="F1", size=8.2, rgb=(0.2, 0.2, 0.2))
            y -= 11

        y -= 3
        # 3 boxes horizontais para os 3 setores
        sw = (self.content_w - 12) / 3
        setores = [
            ("VLAN 10: ATENDIMENTO", "Triagem de clientes, abertura de contas", "e suporte aos correntistas no autoatendimento.", (0.95, 0.98, 1.0), (0.2, 0.4, 0.7)),
            ("VLAN 20: OPERAÇÕES & ADMIN", "Terminais de caixa executivo de alta criticidade,", "operações financeiras e gestão administrativa.", (1.0, 0.98, 0.94), (0.7, 0.4, 0.1)),
            ("VLAN 30: SERVIDORES LOCAIS", "Data Center interno: Web Banking institucional,", "servidor DNS (finbank.local) e coletor Syslog.", (0.94, 0.99, 0.96), (0.1, 0.5, 0.3))
        ]
        for i, (stitle, sdesc1, sdesc2, sfill, sstroke) in enumerate(setores):
            sx = self.margin_x + (i * (sw + 6))
            self.draw_rect(sx, y - 40, sw, 40, fill_rgb=sfill, stroke_rgb=sstroke, line_width=0.8)
            self.draw_text(stitle, sx + 6, y - 11, font="F2", size=7.5, rgb=sstroke)
            self.draw_text(sdesc1, sx + 6, y - 22, font="F1", size=6.8, rgb=(0.25, 0.25, 0.25))
            self.draw_text(sdesc2, sx + 6, y - 32, font="F1", size=6.8, rgb=(0.25, 0.25, 0.25))

        # 1.3 Descrição do Problema Identificado
        y -= 54
        self.draw_text("1.3 DESCRIÇÃO DO PROBLEMA IDENTIFICADO", self.margin_x, y, font="F2", size=10, rgb=(0.04, 0.15, 0.28))
        self.draw_line(self.margin_x, y - 3, self.margin_x + self.content_w, y - 3, rgb=(0.04, 0.15, 0.28), width=1)

        y -= 14
        # Pergunta problema central
        self.draw_rect(self.margin_x, y - 32, self.content_w, 32, fill_rgb=(0.98, 0.98, 0.98), stroke_rgb=(0.85, 0.3, 0.3), line_width=1.2)
        self.draw_text("PROBLEMA EMPRESARIAL CENTRAL:", self.margin_x + 8, y - 10, font="F2", size=7.8, rgb=(0.7, 0.15, 0.15))
        self.draw_text('"Como acompanhar em tempo real a disponibilidade dos dispositivos de rede corporativa e diagnosticar interrupções que', self.margin_x + 8, y - 20, font="F1", size=7.5, rgb=(0.15, 0.15, 0.15))
        self.draw_text('possam comprometer os serviços financeiros, diferenciando oscilações pontuais de panes persistentes e priorizando ativos críticos?"', self.margin_x + 8, y - 29, font="F1", size=7.5, rgb=(0.15, 0.15, 0.15))

        y -= 44
        dores = [
            ("• Rede Plana sem Isolamento:", "Estações comuns compartilhavam o mesmo domínio de broadcast dos caixas operacionais, gerando vulnerabilidades."),
            ("• Gestão de TI Puramente Reativa:", "Interrupções eram comunicadas apenas após a reclamação dos colaboradores, elevando substancialmente o MTTR."),
            ("• Alertas Uniformes sem Criticidade:", "A queda de um PC de triagem gerava o mesmo alerta que a parada do servidor web de transações ou do gateway."),
            ("• Ruídos por Falsos Positivos:", "Perdas momentâneas de pacotes (drops passageiros) disparavam alarmes falsos de inoperância total do enlace."),
            ("• Falta de Histórico e Auditoria:", "Inexistência de dados de disponibilidade percentual (Uptime %) para comprovação de SLA perante a auditoria bancária.")
        ]
        for dtitle, ddesc in dores:
            self.draw_text(dtitle, self.margin_x, y, font="F2", size=7.8, rgb=(0.15, 0.15, 0.15))
            self.draw_text(ddesc, self.margin_x + 140, y, font="F1", size=7.8, rgb=(0.25, 0.25, 0.25))
            y -= 12

        # =========================================================================
        # PÁGINA 2: OBJETIVOS E ESCOPO DA SOLUÇÃO PROPOSTA
        # =========================================================================
        self.new_page()
        self.add_header(2, 4)

        # 1.4 Objetivo Geral e Objetivos Específicos
        y = self.height - 52
        self.draw_text("1.4 OBJETIVO GERAL E OBJETIVOS ESPECÍFICOS", self.margin_x, y, font="F2", size=10, rgb=(0.04, 0.15, 0.28))
        self.draw_line(self.margin_x, y - 3, self.margin_x + self.content_w, y - 3, rgb=(0.04, 0.15, 0.28), width=1)

        y -= 14
        self.draw_rect(self.margin_x, y - 34, self.content_w, 34, fill_rgb=(0.95, 0.98, 1.0), stroke_rgb=(0.25, 0.5, 0.85), line_width=1)
        self.draw_text("OBJETIVO GERAL DO PROJETO:", self.margin_x + 8, y - 11, font="F2", size=8, rgb=(0.1, 0.3, 0.65))
        self.draw_text("Projetar, implantar e homologar a infraestrutura de rede corporativa segmentada da FinBank Digital no Cisco Packet Tracer,", self.margin_x + 8, y - 21, font="F1", size=7.8, rgb=(0.15, 0.15, 0.15))
        self.draw_text("integrando-a a um software em Python para monitoramento ativo de disponibilidade, auditoria de falhas e priorização de alarmes.", self.margin_x + 8, y - 30, font="F1", size=7.8, rgb=(0.15, 0.15, 0.15))

        y -= 46
        self.draw_text("OBJETIVOS ESPECÍFICOS:", self.margin_x, y, font="F2", size=8.5, rgb=(0.04, 0.15, 0.28))
        y -= 12
        objs = [
            "1. Modelar a topologia Router-on-a-Stick no Cisco Packet Tracer via enlace tronco dot1Q (Roteador 1941 e Switch 2960).",
            "2. Segmentar a agência em 3 domínios de broadcast isolados: VLAN 10 (Atendimento), VLAN 20 (Operações/Admin) e VLAN 30 (Servidores).",
            "3. Configurar servidores DHCP dedicados no Roteador Cisco para concessão dinâmica com exclusão das faixas de IPs estáticos.",
            "4. Implantar os serviços centrais essenciais: servidor Web (HTTP porta 80), servidor DNS (finbank.local) e servidor Syslog.",
            "5. Desenvolver a aplicação de monitoramento em Python 3 aderente aos Requisitos Funcionais RF01 a RF06 em arquitetura orientada a objetos.",
            "6. Implementar algoritmo de detecção de indisponibilidade persistente acionado unicamente após 3 falhas consecutivas de verificação ICMP.",
            "7. Classificar ativos em matriz hierárquica de criticidade (CRÍTICA, ALTA e NORMAL) para imediato escalonamento de avisos.",
            "8. Calcular matematicamente a taxa de Uptime % acumulada e realizar homologação completa com simulação de interrupções de enlace."
        ]
        for obj in objs:
            self.draw_rect(self.margin_x + 2, y - 8, 4, 4, fill_rgb=(0.2, 0.45, 0.8))
            self.draw_text(obj, self.margin_x + 12, y - 8, font="F1", size=7.5, rgb=(0.2, 0.2, 0.2))
            y -= 13

        # 1.5 Escopo da Solução Proposta
        y -= 14
        self.draw_text("1.5 ESCOPO DA SOLUÇÃO PROPOSTA", self.margin_x, y, font="F2", size=10, rgb=(0.04, 0.15, 0.28))
        self.draw_line(self.margin_x, y - 3, self.margin_x + self.content_w, y - 3, rgb=(0.04, 0.15, 0.28), width=1)

        y -= 14
        esc_w = (self.content_w - 10) / 2
        # Escopo Positivo
        self.draw_rect(self.margin_x, y - 185, esc_w, 185, fill_rgb=(0.96, 0.99, 0.97), stroke_rgb=(0.2, 0.6, 0.35), line_width=1)
        self.draw_text("ESCOPO POSITIVO (INCLUSO NO PROJETO)", self.margin_x + 8, y - 14, font="F2", size=8, rgb=(0.1, 0.5, 0.25))
        pos_items = [
            "• Topologia simulada completa no Cisco Packet Tracer v8.x.",
            "• 1 Roteador Cisco 1941 e 1 Switch Catalyst 2960-24TT.",
            "• 2 Servidores dedicados (Web/DNS e Syslog) e 4 PCs clientes.",
            "• Cabeamento direto par trançado (FastEthernet e Gigabit).",
            "• Segmentação de VLANs 10, 20 e 30 com portas PortFast.",
            "• Roteamento Router-on-a-Stick via subinterfaces 802.1Q.",
            "• Pools DHCP dedicados com exclusão dos IPs estáticos .1 a .10.",
            "• Serviços de rede: HTTP (porta 80), DNS (porta 53) e Syslog.",
            "• Software Python (monitor_finbank.py) orientado a objetos.",
            "• Verificação de disponibilidade real via ICMP Ping do SO.",
            "• Modo de simulação para injeção forçada de falhas de teste.",
            "• Matriz de criticidade e regra das 3 falhas consecutivas.",
            "• Relatório tabular consolidado com percentual de Uptime %."
        ]
        py = y - 27
        for item in pos_items:
            self.draw_text(item, self.margin_x + 8, py, font="F1", size=7.1, rgb=(0.15, 0.15, 0.15))
            py -= 12

        # Escopo Negativo
        ex2 = self.margin_x + esc_w + 10
        self.draw_rect(ex2, y - 185, esc_w, 185, fill_rgb=(1.0, 0.97, 0.97), stroke_rgb=(0.8, 0.3, 0.3), line_width=1)
        self.draw_text("ESCOPO NEGATIVO (NÃO INCLUSO / LIMITAÇÕES)", ex2 + 8, y - 14, font="F2", size=8, rgb=(0.7, 0.15, 0.15))
        neg_items = [
            "• Interconexão com a Internet externa / operadoras WAN públicas.",
            "• Roteamento dinâmico avançado (OSPF, BGP ou EIGRP).",
            "• Protocolos de redundância de gateway (HSRP, VRRP ou GLBP).",
            "• Banco de dados relacional externo (MySQL/PostgreSQL).",
            "• Autenticação de portas físicas baseada em 802.1X / RADIUS.",
            "• Equipamento físico de firewall dedicado ou IPS/IDS de borda.",
            "• Criptografia e túneis VPN IPsec corporativos interbancários.",
            "• Interface gráfica web (GUI) para o software de monitoramento.",
            "• Envio automatizado de e-mails ou integração com webhooks.",
            "• Monitoramento de consumo de CPU, memória RAM ou disco.",
            "• Cabeamento óptico estruturado de longa distância.",
            "• Telefonia IP (VoIP) ou infraestrutura de rede sem fio (Wi-Fi).",
            "• Gerenciamento remoto out-of-band via rede celular dedicada."
        ]
        ny = y - 27
        for item in neg_items:
            self.draw_text(item, ex2 + 8, ny, font="F1", size=7.1, rgb=(0.25, 0.2, 0.2))
            ny -= 12

        # Caixa de Termo de Handover e Integração de Equipes
        y = y - 195
        self.draw_rect(self.margin_x, y - 35, self.content_w, 35, fill_rgb=(0.95, 0.97, 1.0), stroke_rgb=(0.3, 0.5, 0.8), line_width=0.8)
        self.draw_text("INTEGRAÇÃO ENTRE EQUIPES (HANDOVER TÉCNICO):", self.margin_x + 8, y - 10, font="F2", size=7.8, rgb=(0.05, 0.25, 0.55))
        self.draw_text("O Grupo 01 entrega a rede funcional (.pkt) e a tabela de IPs homologada; o Grupo 02 consome esses endereços no software Python", self.margin_x + 8, y - 20, font="F1", size=7.2, rgb=(0.2, 0.2, 0.2))
        self.draw_text("e implementa o ciclo contínuo de verificações ICMP, cálculos de disponibilidade e relatórios gerenciais.", self.margin_x + 8, y - 29, font="F1", size=7.2, rgb=(0.2, 0.2, 0.2))

        # =========================================================================
        # PÁGINA 3: REQUISITOS FUNCIONAIS E NÃO FUNCIONAIS
        # =========================================================================
        self.new_page()
        self.add_header(3, 4)

        # 1.6 Requisitos Funcionais e Não Funcionais
        y = self.height - 52
        self.draw_text("1.6 REQUISITOS FUNCIONAIS E NÃO FUNCIONAIS", self.margin_x, y, font="F2", size=10, rgb=(0.04, 0.15, 0.28))
        self.draw_line(self.margin_x, y - 3, self.margin_x + self.content_w, y - 3, rgb=(0.04, 0.15, 0.28), width=1)

        # Subseção: Requisitos Funcionais (RF)
        y -= 14
        self.draw_text("REQUISITOS FUNCIONAIS (RF):", self.margin_x, y, font="F2", size=8.5, rgb=(0.04, 0.15, 0.28))

        y -= 12
        # Tabela RF Cabeçalho
        self.draw_rect(self.margin_x, y - 14, self.content_w, 14, fill_rgb=(0.04, 0.15, 0.28))
        self.draw_text("Cód.", self.margin_x + 6, y - 10, font="F2", size=7.2, rgb=(1,1,1))
        self.draw_text("Nome do Requisito", self.margin_x + 40, y - 10, font="F2", size=7.2, rgb=(1,1,1))
        self.draw_text("Descrição Técnica e Operacional", self.margin_x + 190, y - 10, font="F2", size=7.2, rgb=(1,1,1))

        rf_list = [
            ("RF01", "Cadastro de Ativos e Serviços", "Permitir o registro estruturado de dispositivos com ID, nome, IP, setor, serviço e nível de criticidade."),
            ("RF02", "Registro de Verificações", "Gravar a cada ciclo o carimbo de data/hora (timestamp), o identificador do ativo e o resultado (SUCESSO ou FALHA)."),
            ("RF03", "Consulta de Histórico", "Disponibilizar funcionalidade de auditoria para listar o histórico cronológico de coletas de um equipamento."),
            ("RF04", "Detecção de Falhas Consecutivas", "Contabilizar e sinalizar em tempo de execução quando um equipamento acumular falhas consecutivas de resposta."),
            ("RF05", "Cálculo de Uptime Percentual", "Calcular a taxa de disponibilidade percentual: Uptime % = (Total de Sucessos / Total de Testes) * 100."),
            ("RF06", "Emissão de Alertas e Relatórios", "Exibir alertas priorizados no console e gerar relatório consolidado com status, falhas e indicadores."),
            ("RF07", "Roteamento Inter-VLAN (Infra)", "Roteador deve interligar as VLANs 10, 20 e 30 via subinterfaces 802.1Q, garantindo alcance aos servidores."),
            ("RF08", "Concessão DHCP Dinâmica (Infra)", "Serviço DHCP centralizado no Roteador Cisco 1941 concedendo parâmetros de rede aos clientes das VLANs 10 e 20."),
            ("RF09", "Resolução DNS Interna (Infra)", "Servidor DNS local resolvendo o domínio corporativo finbank.local para o endereço IP fixo 192.168.30.10.")
        ]
        rf_y = y - 14
        for i, (code, rname, rdesc) in enumerate(rf_list):
            bg = (0.97, 0.98, 0.99) if i % 2 == 0 else (1.0, 1.0, 1.0)
            self.draw_rect(self.margin_x, rf_y - 13, self.content_w, 13, fill_rgb=bg, stroke_rgb=(0.88, 0.88, 0.88), line_width=0.5)
            self.draw_text(code, self.margin_x + 6, rf_y - 9.5, font="F2", size=6.8, rgb=(0.1, 0.3, 0.6))
            self.draw_text(rname, self.margin_x + 40, rf_y - 9.5, font="F2", size=6.8, rgb=(0.15, 0.15, 0.15))
            self.draw_text(rdesc, self.margin_x + 190, rf_y - 9.5, font="F1", size=6.6, rgb=(0.25, 0.25, 0.25))
            rf_y -= 13

        # Subseção: Requisitos Não Funcionais (RNF)
        y = rf_y - 16
        self.draw_text("REQUISITOS NÃO FUNCIONAIS (RNF):", self.margin_x, y, font="F2", size=8.5, rgb=(0.04, 0.15, 0.28))

        y -= 12
        # Tabela RNF Cabeçalho
        self.draw_rect(self.margin_x, y - 14, self.content_w, 14, fill_rgb=(0.04, 0.15, 0.28))
        self.draw_text("Cód.", self.margin_x + 6, y - 10, font="F2", size=7.2, rgb=(1,1,1))
        self.draw_text("Categoria", self.margin_x + 40, y - 10, font="F2", size=7.2, rgb=(1,1,1))
        self.draw_text("Critério Técnico e Descrição Detalhada", self.margin_x + 160, y - 10, font="F2", size=7.2, rgb=(1,1,1))

        rnf_list = [
            ("RNF01", "Desempenho e Timeout", "Tempo limite máximo de 800ms por teste ICMP; ciclo completo em menos de 5 segundos para não travar a fila."),
            ("RNF02", "Portabilidade / Multiplataforma", "Código Python nativo compatível com Windows (-n) e Linux (-c) com detecção automática via biblioteca platform."),
            ("RNF03", "Segurança e Segregação", "Isolamento total dos domínios de broadcast por VLANs 802.1Q; tráfego de clientes não interfere nas operações."),
            ("RNF04", "Tolerância a Falsos Positivos", "O sistema não alerta pane total diante de apenas 1 perda transitória; requer confirmação por amostragem acumulada."),
            ("RNF05", "Fidelidade e Reprodutibilidade", "100% de compatibilidade com comandos nativos do Cisco IOS v15.x e reprodutibilidade no Packet Tracer v8.x."),
            ("RNF06", "Usabilidade e Legibilidade", "Exibição estruturada em console tabular com indicadores visuais de criticidade e estado operacional ([OK]/[FALHA]).")
        ]
        rnf_y = y - 14
        for i, (code, rcateg, rdesc) in enumerate(rnf_list):
            bg = (0.97, 0.98, 0.99) if i % 2 == 0 else (1.0, 1.0, 1.0)
            self.draw_rect(self.margin_x, rnf_y - 14, self.content_w, 14, fill_rgb=bg, stroke_rgb=(0.88, 0.88, 0.88), line_width=0.5)
            self.draw_text(code, self.margin_x + 6, rnf_y - 10, font="F2", size=6.8, rgb=(0.1, 0.5, 0.35))
            self.draw_text(rcateg, self.margin_x + 40, rnf_y - 10, font="F2", size=6.8, rgb=(0.15, 0.15, 0.15))
            self.draw_text(rdesc, self.margin_x + 160, rnf_y - 10, font="F1", size=6.6, rgb=(0.25, 0.25, 0.25))
            rnf_y -= 14

        # Caixa com fórmula KaTeX explicada
        y = rnf_y - 14
        self.draw_rect(self.margin_x, y - 28, self.content_w, 28, fill_rgb=(0.95, 0.97, 1.0), stroke_rgb=(0.3, 0.5, 0.8), line_width=0.8)
        self.draw_text("MÉTRICA MATEMÁTICA OFICIAL DE DISPONIBILIDADE (UPTIME):", self.margin_x + 8, y - 10, font="F2", size=7.5, rgb=(0.05, 0.25, 0.55))
        self.draw_text("Fórmula: Uptime % = (Total de Verificações com Sucesso / Total de Verificações Registradas) * 100", self.margin_x + 8, y - 20, font="F2", size=7.2, rgb=(0.15, 0.15, 0.15))

        # =========================================================================
        # PÁGINA 4: REGRAS DE NEGÓCIO, ARQUITETURA E TECNOLOGIAS UTILIZADAS
        # =========================================================================
        self.new_page()
        self.add_header(4, 4)

        # 1.7 Regras de Negócio (RN)
        y = self.height - 52
        self.draw_text("1.7 REGRAS DE NEGÓCIO (RN)", self.margin_x, y, font="F2", size=10, rgb=(0.04, 0.15, 0.28))
        self.draw_line(self.margin_x, y - 3, self.margin_x + self.content_w, y - 3, rgb=(0.04, 0.15, 0.28), width=1)

        y -= 12
        rns = [
            ("RN01 — Priorização Hierárquica por Criticidade:", "Ativos CRÍTICOS (R-FINBANK e SRV-WEB-BANCO) e de ALTA criticidade (PC-OPER-01) disparam avisos imediatos de emergência na console."),
            ("RN02 — Gatilho de Indisponibilidade Persistente:", "Alerta de pane definitiva somente é emitido após 3 falhas consecutivas de verificação ICMP, descartando instabilidades esporádicas."),
            ("RN03 — Normalização e Reset do Contador:", "Caso um ativo com falhas consecutivas volte a responder com SUCESSO, seu contador de falhas é zerado imediatamente."),
            ("RN04 — Imutabilidade dos Registros de Auditoria:", "Todas as verificações preservam timestamp, IP e resultado cronológico, compondo histórico imutável durante a sessão."),
            ("RN05 — Reserva Estática de Endereçamento IP:", "Os 10 primeiros IPs (.1 a .10) de cada sub-rede são reservados a gateways e servidores, sendo excluídos dos pools DHCP."),
            ("RN06 — Alocação Restrita de Portas por VLAN:", "Portas FastEthernet 0/1 a 0/5 exclusivas da VLAN 10; 0/6 a 0/10 da VLAN 20; e 0/11 a 0/15 da VLAN 30.")
        ]
        for rntitle, rndesc in rns:
            self.draw_text(rntitle, self.margin_x, y, font="F2", size=7.5, rgb=(0.1, 0.2, 0.45))
            self.draw_text(rndesc, self.margin_x + 195, y, font="F1", size=7.2, rgb=(0.2, 0.2, 0.2))
            y -= 11

        # 1.8 Arquitetura e Tecnologias Utilizadas
        y -= 8
        self.draw_text("1.8 ARQUITETURA E TECNOLOGIAS UTILIZADAS", self.margin_x, y, font="F2", size=10, rgb=(0.04, 0.15, 0.28))
        self.draw_line(self.margin_x, y - 3, self.margin_x + self.content_w, y - 3, rgb=(0.04, 0.15, 0.28), width=1)

        y -= 12
        # Diagrama Esquemático em ASCII compacto
        diag_lines = [
            "  +---------------------------------------------------------------------------------------------------------------+",
            "  |                                   R-FINBANK (Roteador Cisco 1941)                                             |",
            "  |                Gateways: 192.168.10.1 (VLAN 10) | 192.168.20.1 (VLAN 20) | 192.168.30.1 (VLAN 30)             |",
            "  +-------------------------------------------------------+-------------------------------------------------------+",
            "                                                          | Gig0/0 [Enlace Tronco 802.1Q]",
            "                                                          | Gig0/1",
            "  +-------------------------------------------------------+-------------------------------------------------------+",
            "  |                                  SW-FINBANK (Switch Catalyst 2960-24TT)                                       |",
            "  +-----------------------+-------------------------------+-------------------------------+-----------------------+",
            "                          | Fa0/1 e Fa0/2                 | Fa0/6 e Fa0/7                 | Fa0/11 e Fa0/12",
            "  +-----------------------v-------+       +---------------v---------------+       +-------v-----------------------+",
            "  |       SETOR ATENDIMENTO       |       |       OPERACOES & ADMIN       |       |     SERVIDORES & DATA CTR     |",
            "  |           (VLAN 10)           |       |           (VLAN 20)           |       |           (VLAN 30)           |",
            "  | [PC-ATEND-01] 192.168.10.11   |       | [PC-OPER-01]  192.168.20.11   |       | [SRV-WEB-BANCO] 192.168.30.10 |",
            "  | [PC-ATEND-02] 192.168.10.12   |       | [PC-ADMIN-01] 192.168.20.12   |       | [SRV-MONITOR]   192.168.30.20 |",
            "  +-------------------------------+       +-------------------------------+       +-------------------------------+"
        ]
        self.draw_rect(self.margin_x, y - 96, self.content_w, 96, fill_rgb=(0.98, 0.98, 0.99), stroke_rgb=(0.8, 0.85, 0.9), line_width=0.8)
        dy = y - 9
        for dline in diag_lines:
            self.draw_text(dline, self.margin_x + 6, dy, font="F3", size=5.8, rgb=(0.1, 0.15, 0.25))
            dy -= 6.2

        y -= 104
        # Tabela de Ativos e Endereçamento
        self.draw_rect(self.margin_x, y - 12, self.content_w, 12, fill_rgb=(0.04, 0.15, 0.28))
        self.draw_text("Dispositivo", self.margin_x + 6, y - 9, font="F2", size=6.8, rgb=(1,1,1))
        self.draw_text("Endereço IPv4", self.margin_x + 95, y - 9, font="F2", size=6.8, rgb=(1,1,1))
        self.draw_text("Gateway Padrão", self.margin_x + 180, y - 9, font="F2", size=6.8, rgb=(1,1,1))
        self.draw_text("VLAN / Setor", self.margin_x + 265, y - 9, font="F2", size=6.8, rgb=(1,1,1))
        self.draw_text("Criticidade", self.margin_x + 360, y - 9, font="F2", size=6.8, rgb=(1,1,1))
        self.draw_text("Serviço / Função", self.margin_x + 430, y - 9, font="F2", size=6.8, rgb=(1,1,1))

        ativos = [
            ("R-FINBANK", "192.168.10/20/30.1", "— (Gateway Core)", "Core / Geral", "CRÍTICA", "Roteamento 802.1Q e DHCP Pools"),
            ("SRV-WEB-BANCO", "192.168.30.10", "192.168.30.1", "VLAN 30 (Servidores)", "CRÍTICA", "Web Banking HTTP (80) & DNS"),
            ("SRV-MONITOR", "192.168.30.20", "192.168.30.1", "VLAN 30 (Servidores)", "NORMAL", "Servidor Syslog / Coletor de Logs"),
            ("PC-OPER-01", "192.168.20.11", "192.168.20.1", "VLAN 20 (Operações)", "ALTA", "Terminal de Caixa Financeiro"),
            ("PC-ADMIN-01", "192.168.20.12", "192.168.20.1", "VLAN 20 (Admin)", "NORMAL", "Estação de Gestão Administrativa"),
            ("PC-ATEND-01", "192.168.10.11", "192.168.10.1", "VLAN 10 (Atendimento)", "NORMAL", "Estação de Atendimento ao Cliente"),
            ("PC-ATEND-02", "192.168.10.12", "192.168.10.1", "VLAN 10 (Atendimento)", "NORMAL", "Estação de Atendimento ao Cliente")
        ]
        ay = y - 12
        for i, (at_nome, at_ip, at_gw, at_vlan, at_crit, at_serv) in enumerate(ativos):
            bg = (0.97, 0.98, 0.99) if i % 2 == 0 else (1.0, 1.0, 1.0)
            self.draw_rect(self.margin_x, ay - 11, self.content_w, 11, fill_rgb=bg, stroke_rgb=(0.88, 0.88, 0.88), line_width=0.5)
            self.draw_text(at_nome, self.margin_x + 6, ay - 8, font="F2", size=6.5, rgb=(0.15, 0.15, 0.15))
            self.draw_text(at_ip, self.margin_x + 95, ay - 8, font="F3", size=6.2, rgb=(0.1, 0.25, 0.55))
            self.draw_text(at_gw, self.margin_x + 180, ay - 8, font="F1", size=6.2, rgb=(0.3, 0.3, 0.3))
            self.draw_text(at_vlan, self.margin_x + 265, ay - 8, font="F1", size=6.2, rgb=(0.2, 0.2, 0.2))
            
            crit_col = (0.8, 0.1, 0.1) if at_crit == "CRÍTICA" else ((0.7, 0.4, 0.0) if at_crit == "ALTA" else (0.1, 0.5, 0.2))
            self.draw_text(at_crit, self.margin_x + 360, ay - 8, font="F2", size=6.2, rgb=crit_col)
            self.draw_text(at_serv, self.margin_x + 430, ay - 8, font="F1", size=6.2, rgb=(0.2, 0.2, 0.2))
            ay -= 11

        y = ay - 10
        # Tecnologias e Protocolos Resumo
        self.draw_rect(self.margin_x, y - 32, self.content_w, 32, fill_rgb=(0.96, 0.98, 1.0), stroke_rgb=(0.35, 0.5, 0.8), line_width=0.8)
        self.draw_text("PILHA DE TECNOLOGIAS E PROTOCOLOS APLICADOS:", self.margin_x + 8, y - 10, font="F2", size=7.2, rgb=(0.05, 0.25, 0.55))
        self.draw_text("• Camada 2: IEEE 802.1Q (Tronco dot1Q), STP PortFast | Camada 3 e 4: IPv4 (/24), ICMP Echo, TCP (80), UDP (53, 67, 68, 514)", self.margin_x + 8, y - 19, font="F1", size=6.8, rgb=(0.2, 0.2, 0.2))
        self.draw_text("• Serviços L7: HTTP (Web Banking), DNS (finbank.local), DHCP Server, Syslog | Softwares: Cisco Packet Tracer v8.x & Python 3.x", self.margin_x + 8, y - 28, font="F1", size=6.8, rgb=(0.2, 0.2, 0.2))

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
    out_pdf = r"C:\Users\jamerson.albuquerque\.gemini\antigravity\scratch\finbank_digital\FinBank_Digital_Documentacao_Tecnica.pdf"
    gerador = DocumentacaoTecnicaPDF(out_pdf)
    gerador.build_pdf()
    print("PDF da Documentação Técnica gerado com sucesso em:", out_pdf)
