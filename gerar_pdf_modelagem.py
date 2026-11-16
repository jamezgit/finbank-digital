import os
import sys

class ModelagemSolucaoPDF:
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
        self.draw_text("FINBANK DIGITAL  •  PROJETO 02 — TÓPICO 2: MODELAGEM DA SOLUÇÃO", self.margin_x + 8, self.height - 23, font="F2", size=7.5, rgb=(1,1,1))
        self.draw_text("SOFTWARE EM PYTHON & INFRAESTRUTURA DE REDE", self.width - self.margin_x - 195, self.height - 23, font="F2", size=7.5, rgb=(0.35, 0.85, 0.70))
        
        # Footer
        self.draw_line(self.margin_x, 26, self.width - self.margin_x, 26, rgb=(0.8,0.8,0.8), width=0.8)
        self.draw_text("Documentação Técnica de Engenharia: Fluxogramas, Pseudocódigo e Integração ICMP | FinBank Digital", self.margin_x, 16, font="F1", size=7.5, rgb=(0.4,0.4,0.4))
        self.draw_text(f"Página {page_num} de {total_pages}", self.width - self.margin_x - 55, 16, font="F2", size=7.5, rgb=(0.2,0.2,0.2))

    def build_pdf(self):
        # =========================================================================
        # PÁGINA 1: VISÃO GERAL E FLUXOGRAMA DO ALGORITMO
        # =========================================================================
        self.new_page()
        self.add_header(1, 4)

        # 1. Bloco de Título Principal
        y = self.height - 52
        self.draw_rect(self.margin_x, y - 56, self.content_w, 56, fill_rgb=(0.95, 0.97, 1.0), stroke_rgb=(0.75, 0.82, 0.95), line_width=1)
        self.draw_text("PROJETO 02 — FINBANK DIGITAL: MODELAGEM DA SOLUÇÃO", self.margin_x + 12, y - 18, font="F2", size=13, rgb=(0.04, 0.15, 0.28))
        self.draw_text("Tópico 2: Representação Técnica, Fluxogramas, Pseudocódigo e Integração de Rede", self.margin_x + 12, y - 33, font="F1", size=9.5, rgb=(0.25, 0.35, 0.50))
        self.draw_text("ALGORITMO DE MONITORAMENTO EM PYTHON 3 & ENLACES ROUTER-ON-A-STICK (802.1Q)", self.margin_x + 12, y - 47, font="F2", size=8, rgb=(0.05, 0.55, 0.35))

        # 2.1 Visão Geral da Modelagem
        y -= 68
        self.draw_text("2.1 VISÃO GERAL DA MODELAGEM TÉCNICA", self.margin_x, y, font="F2", size=10, rgb=(0.04, 0.15, 0.28))
        self.draw_line(self.margin_x, y - 3, self.margin_x + self.content_w, y - 3, rgb=(0.04, 0.15, 0.28), width=1)

        y -= 14
        p1 = "A modelagem técnica do sistema compreende a articulação entre o software de monitoramento autônomo (desenvolvido em"
        p2 = "Python 3) e a infraestrutura física/lógica segmentada (simulada no Cisco Packet Tracer). O algoritmo atua como uma sonda de"
        p3 = "rede periódica que analisa a transitabilidade de pacotes ICMP através das VLANs, gerenciando estados operacionais e calculando SLAs."
        for line in [p1, p2, p3]:
            self.draw_text(line, self.margin_x, y, font="F1", size=7.8, rgb=(0.2, 0.2, 0.2))
            y -= 11

        # 2.2 Fluxograma do Algoritmo de Monitoramento
        y -= 8
        self.draw_text("2.2 FLUXOGRAMA DO ALGORITMO DE MONITORAMENTO", self.margin_x, y, font="F2", size=10, rgb=(0.04, 0.15, 0.28))
        self.draw_line(self.margin_x, y - 3, self.margin_x + self.content_w, y - 3, rgb=(0.04, 0.15, 0.28), width=1)

        y -= 13
        self.draw_text("O fluxo operacional a seguir descreve a lógica de decisão, desde o disparo do teste até o escalonamento de alarmes:", self.margin_x, y, font="F1", size=7.6, rgb=(0.25, 0.25, 0.25))

        y -= 10
        # Box do Fluxograma ASCII
        self.draw_rect(self.margin_x, y - 315, self.content_w, 315, fill_rgb=(0.98, 0.98, 0.99), stroke_rgb=(0.75, 0.8, 0.9), line_width=0.8)
        
        fluxo_lines = [
            "                                   [ INÍCIO DO CICLO DE VERIFICAÇÃO ]",
            "                                                    |",
            "                                   [ Carregar Ativos Cadastrados (RF01) ]",
            "                                                    |",
            "                      +-----------------------------v-----------------------------+",
            "                      | Para CADA dispositivo cadastrado na agência:              |",
            "                      +-----------------------------+-----------------------------+",
            "                                                    |",
            "                                       [ Modo de Execução? ]",
            "                                        /                 \\",
            "                          (Modo Real)  /                   \\  (Modo Simulado)",
            "                                      v                     v",
            "                     [ Disparar ICMP Ping (800ms) ]   [ Forçar Status Simulado ]",
            "                                      \\                     /",
            "                                       \\                   /",
            "                                        v                 v",
            "                                     [ Resposta Obtida com Sucesso? ]",
            "                                        /                        \\",
            "                           (SIM)       /                          \\       (NÃO)",
            "                                      v                            v",
            "                         +-------------------------+  +-----------------------------------+",
            "                         | Status: 'SUCESSO' [OK]  |  | Status: 'FALHA' [OFFLINE]         |",
            "                         | falhas_consecutivas = 0 |  | falhas_consecutivas += 1 (RF04)   |",
            "                         +------------+------------+  +-----------------+-----------------+",
            "                                      |                                 |",
            "                                      |                    [ Ativo CRÍTICO ou ALTA? (RN01) ]",
            "                                      |                     /                           \\",
            "                                      |             (SIM)  /                             \\  (NÃO)",
            "                                      |                   v                               v",
            "                                      |     [ Emite ALERTA PRIORITÁRIO ]                  |",
            "                                      |                   |                               |",
            "                                      |                   +--------------+----------------+",
            "                                      |                                  |",
            "                                      |                    [ falhas_consecutivas >= 3? (RN02) ]",
            "                                      |                     /                           \\",
            "                                      |             (SIM)  /                             \\  (NÃO)",
            "                                      |                   v                               v",
            "                                      |     [ Emite ALERTA DE INDISPONIBILIDADE ]         |",
            "                                      |                   |                               |",
            "                                      +-------------------+---------------+---------------+",
            "                                                                          |",
            "                                      [ Gravar no Histórico: Data/Hora, ID, Status (RF02) ]",
            "                                                                          |",
            "                                 [ Restam dispositivos no ciclo? ] -------+ (SIM)",
            "                                                 | (NÃO)",
            "                                                 v",
            "                         [ Calcular Disponibilidade Uptime % = (Sucessos / Total) * 100 ]",
            "                                                 |",
            "                              [ Gerar Relatório Consolidado de Painel (RF06) ]",
            "                                                 |",
            "                                        [ FIM DO CICLO ]"
        ]
        fy = y - 9
        for fline in fluxo_lines:
            self.draw_text(fline, self.margin_x + 8, fy, font="F3", size=5.4, rgb=(0.1, 0.15, 0.25))
            fy -= 6.5

        # =========================================================================
        # PÁGINA 2: PSEUDOCÓDIGO DAS PRINCIPAIS FUNCIONALIDADES (PARTE 1)
        # =========================================================================
        self.new_page()
        self.add_header(2, 4)

        # 2.3 Pseudocódigo das Principais Funcionalidades
        y = self.height - 52
        self.draw_text("2.3 PSEUDOCÓDIGO DAS PRINCIPAIS FUNCIONALIDADES (PARTE 1)", self.margin_x, y, font="F2", size=10, rgb=(0.04, 0.15, 0.28))
        self.draw_line(self.margin_x, y - 3, self.margin_x + self.content_w, y - 3, rgb=(0.04, 0.15, 0.28), width=1)

        y -= 13
        # Módulo 1: Estrutura de Dados e Cadastro
        self.draw_text("2.3.1 MÓDULO 1: ESTRUTURAS DE DADOS E CADASTRO DE ATIVOS (RF01)", self.margin_x, y, font="F2", size=8.5, rgb=(0.1, 0.25, 0.55))
        y -= 9
        code_mod1 = [
            "ESTRUTURA RegistroVerificacao:",
            "    data_hora : TEXTO                   // Data e hora do teste no formato AAAA-MM-DD HH:MM:SS",
            "    resultado : TEXTO                   // Armazena 'SUCESSO' ou 'FALHA'",
            "FIM_ESTRUTURA",
            "",
            "CLASSE Dispositivo:",
            "    ATRIBUTOS: id, nome, ip, setor, servico, criticidade, historico, falhas_consecutivas",
            "    MÉTODO Inicializar(id_d, nome_d, ip_d, setor_d, servico_d, criticidade_d):",
            "        id <- id_d; nome <- nome_d; ip <- ip_d; setor <- setor_d; servico <- servico_d",
            "        criticidade <- ConverterParaMaiusculo(criticidade_d) // 'CRITICO', 'ALTA', 'NORMAL'",
            "        historico <- LISTA_VAZIA()",
            "        falhas_consecutivas <- 0",
            "    FIM_MÉTODO",
            "FIM_CLASSE"
        ]
        self.draw_rect(self.margin_x, y - 96, self.content_w, 96, fill_rgb=(0.97, 0.98, 0.99), stroke_rgb=(0.8, 0.85, 0.9), line_width=0.8)
        cy = y - 9
        for cline in code_mod1:
            self.draw_text(cline, self.margin_x + 8, cy, font="F3", size=6.5, rgb=(0.1, 0.15, 0.25))
            cy -= 6.6

        # Módulo 2: Driver de Verificação ICMP de Baixo Nível
        y -= 110
        self.draw_text("2.3.2 MÓDULO 2: DRIVER DE VERIFICAÇÃO ICMP DE BAIXO NÍVEL (RNF01 / RNF02)", self.margin_x, y, font="F2", size=8.5, rgb=(0.1, 0.25, 0.55))
        y -= 9
        code_mod2 = [
            "FUNÇÃO ExecutarPingICMP(endereco_ip : TEXTO) RETORNA BOOLEANO:",
            "    // RNF01: Limite máximo de espera configurado em 800ms por host",
            "    // RNF02: Detecção automática da plataforma para compatibilidade Windows e Linux",
            "    SE SistemaOperacional() = 'WINDOWS' ENTÃO",
            "        comando <- ['ping', '-n', '1', '-w', '800', endereco_ip]",
            "    SENÃO",
            "        comando <- ['ping', '-c', '1', '-W', '1', endereco_ip]",
            "    FIM_SE",
            "    TENTE",
            "        retorno <- ExecutarProcessoOculto(comando)",
            "        RETORNE (retorno.codigo_saida == 0) // Código 0 indica recebimento de Echo Reply",
            "    EXCEÇÃO",
            "        RETORNE FALSO",
            "    FIM_TENTE",
            "FIM_FUNÇÃO"
        ]
        self.draw_rect(self.margin_x, y - 102, self.content_w, 102, fill_rgb=(0.97, 0.98, 0.99), stroke_rgb=(0.8, 0.85, 0.9), line_width=0.8)
        cy = y - 9
        for cline in code_mod2:
            self.draw_text(cline, self.margin_x + 8, cy, font="F3", size=6.5, rgb=(0.1, 0.15, 0.25))
            cy -= 6.6

        # Módulo 3: Ciclo Central de Monitoramento e Regras de Alerta
        y -= 116
        self.draw_text("2.3.3 MÓDULO 3: CICLO DE MONITORAMENTO E REGRAS DE NEGÓCIO (RF02/RF04/RN01/RN02)", self.margin_x, y, font="F2", size=8.5, rgb=(0.1, 0.25, 0.55))
        y -= 9
        code_mod3 = [
            "PROCEDIMENTO ExecutarCicloDeMonitoramento(simular : BOOLEANO, id_falha : TEXTO):",
            "    PARA CADA disp EM lista_dispositivos FAÇA:",
            "        // 1. Determinação de conectividade (Real vs. Simulado)",
            "        SE simular = VERDADEIRO ENTÃO",
            "            status <- (disp.id != id_falha) // Injeção de pane forçada",
            "        SENÃO",
            "            status <- ExecutarPingICMP(disp.ip)",
            "        FIM_SE",
            "        // 2. Registro no histórico cronológico e tratamento de falhas (RF02, RN03, RN04)",
            "        data_atual <- ObterTimestampAtual()",
            "        SE status = VERDADEIRO ENTÃO",
            "            AdicionarHistorico(disp, { data: data_atual, status: 'SUCESSO' })",
            "            disp.falhas_consecutivas <- 0 // Reset imediato no primeiro sucesso (RN03)",
            "        SENÃO",
            "            AdicionarHistorico(disp, { data: data_atual, status: 'FALHA' })",
            "            disp.falhas_consecutivas <- disp.falhas_consecutivas + 1 // Acumulador (RF04)",
            "            // 3. Aplicação de Regras de Alerta",
            "            SE disp.criticidade EM ['CRITICO', 'ALTA'] ENTÃO",
            "                DispararAlerta('[PRIORIDADE MÁXIMA] Ativo CRÍTICO sem resposta: ' + disp.nome) // RN01",
            "            FIM_SE",
            "            SE disp.falhas_consecutivas >= 3 ENTÃO",
            "                DispararAlerta('[INDISPONIBILIDADE PERSISTENTE] 3 falhas consecutivas em ' + disp.nome) // RN02",
            "            FIM_SE",
            "        FIM_SE",
            "    FIM_PARA",
            "FIM_PROCEDIMENTO"
        ]
        self.draw_rect(self.margin_x, y - 180, self.content_w, 180, fill_rgb=(0.97, 0.98, 0.99), stroke_rgb=(0.8, 0.85, 0.9), line_width=0.8)
        cy = y - 9
        for cline in code_mod3:
            self.draw_text(cline, self.margin_x + 8, cy, font="F3", size=6.4, rgb=(0.1, 0.15, 0.25))
            cy -= 6.6

        # =========================================================================
        # PÁGINA 3: PSEUDOCÓDIGO (PARTE 2) E DIAGRAMA DE ARQUITETURA
        # =========================================================================
        self.new_page()
        self.add_header(3, 4)

        # 2.3.4 e 2.3.5
        y = self.height - 52
        self.draw_text("2.3 PSEUDOCÓDIGO DAS PRINCIPAIS FUNCIONALIDADES (PARTE 2)", self.margin_x, y, font="F2", size=10, rgb=(0.04, 0.15, 0.28))
        self.draw_line(self.margin_x, y - 3, self.margin_x + self.content_w, y - 3, rgb=(0.04, 0.15, 0.28), width=1)

        y -= 13
        self.draw_text("2.3.4 MÓDULO 4: CÁLCULO DE DISPONIBILIDADE PERCENTUAL - UPTIME (RF05)", self.margin_x, y, font="F2", size=8.5, rgb=(0.1, 0.25, 0.55))
        y -= 9
        code_mod4 = [
            "FUNÇÃO CalcularDisponibilidadeUptime(disp : Dispositivo) RETORNA REAL:",
            "    total_testes <- TamanhoLista(disp.historico)",
            "    SE total_testes = 0 ENTÃO",
            "        RETORNE 100.0 // Ativo recém cadastrado inicia com 100% de disponibilidade nominal",
            "    FIM_SE",
            "    total_sucessos <- ContarOcorrencias(disp.historico, 'SUCESSO')",
            "    uptime_pct <- (total_sucessos / total_testes) * 100.0",
            "    RETORNE ArredondarCasasDecimais(uptime_pct, 2)",
            "FIM_FUNÇÃO"
        ]
        self.draw_rect(self.margin_x, y - 68, self.content_w, 68, fill_rgb=(0.97, 0.98, 0.99), stroke_rgb=(0.8, 0.85, 0.9), line_width=0.8)
        cy = y - 9
        for cline in code_mod4:
            self.draw_text(cline, self.margin_x + 8, cy, font="F3", size=6.5, rgb=(0.1, 0.15, 0.25))
            cy -= 6.6

        y -= 80
        self.draw_text("2.3.5 MÓDULO 5: EMISSÃO DE RELATÓRIO CONSOLIDADO E AUDITORIA (RF03 / RF06)", self.margin_x, y, font="F2", size=8.5, rgb=(0.1, 0.25, 0.55))
        y -= 9
        code_mod5 = [
            "PROCEDIMENTO GerarRelatorioConsolidado():",
            "    ExibirCabecalhoRelatorio('RELATÓRIO CONSOLIDADO DE DISPONIBILIDADE - FINBANK DIGITAL')",
            "    PARA CADA disp EM lista_dispositivos FAÇA:",
            "        pct <- CalcularDisponibilidadeUptime(disp)",
            "        SE disp.falhas_consecutivas >= 3 ENTÃO",
            "            estado <- 'PERSISTENTE (' + ConverterTexto(disp.falhas_consecutivas) + ' falhas)'",
            "        SENÃO SE disp.falhas_consecutivas > 0 ENTÃO",
            "            estado <- 'Intermitente (' + ConverterTexto(disp.falhas_consecutivas) + ' falha)'",
            "        SENÃO",
            "            estado <- 'Estável (0 falhas)'",
            "        FIM_SE",
            "        ExibirLinhaFormatada(disp.id, disp.nome, disp.setor, disp.criticidade, pct, estado)",
            "    FIM_PARA",
            "FIM_PROCEDIMENTO"
        ]
        self.draw_rect(self.margin_x, y - 98, self.content_w, 98, fill_rgb=(0.97, 0.98, 0.99), stroke_rgb=(0.8, 0.85, 0.9), line_width=0.8)
        cy = y - 9
        for cline in code_mod5:
            self.draw_text(cline, self.margin_x + 8, cy, font="F3", size=6.4, rgb=(0.1, 0.15, 0.25))
            cy -= 6.6

        # 2.4 Diagrama Simplificado da Arquitetura
        y -= 112
        self.draw_text("2.4 DIAGRAMA SIMPLIFICADO DA ARQUITETURA DA SOLUÇÃO", self.margin_x, y, font="F2", size=10, rgb=(0.04, 0.15, 0.28))
        self.draw_line(self.margin_x, y - 3, self.margin_x + self.content_w, y - 3, rgb=(0.04, 0.15, 0.28), width=1)

        y -= 13
        diag_lines = [
            "  +---------------------------------------------------------------------------------------------------------------+",
            "  |                                   CAMADA DE APLICAÇÃO: PYTHON MONITOR (CLI)                                   |",
            "  |       • Classes: MonitorFinBank & Dispositivo      • Injeção de Ping ICMP (800ms)      • Relatórios Uptime %  |",
            "  +-------------------------------------------------------+-------------------------------------------------------+",
            "                                                          | Chamadas nativas de sistema (subprocess)",
            "                                                          v",
            "  +---------------------------------------------------------------------------------------------------------------+",
            "  |                                   CAMADA DE TRANSPORTE & ENLACE: PILHA TCP/IP                                 |",
            "  |       • Gerador de Quadros ICMP Echo Request (Tipo 8)       • Captura de Resposta Echo Reply (Tipo 0)         |",
            "  +-------------------------------------------------------+-------------------------------------------------------+",
            "                                                          | Injeção através da Placa de Rede / Interface Virtual",
            "                                                          v",
            "  +-------------------------------------------------------+-------------------------------------------------------+",
            "  |                                   R-FINBANK (Roteador Cisco 1941)                                             |",
            "  |       • Subinterface Gig0/0.10: 192.168.10.1 (VLAN 10)      • Pools DHCP de Atendimento e Operações           |",
            "  |       • Subinterface Gig0/0.20: 192.168.20.1 (VLAN 20)      • Roteamento Router-on-a-Stick dot1Q              |",
            "  |       • Subinterface Gig0/0.30: 192.168.30.1 (VLAN 30)      • Gateway Central da Agência                      |",
            "  +-------------------------------------------------------+-------------------------------------------------------+",
            "                                                          | Enlace Tronco IEEE 802.1Q (Gig0/0 a Gig0/1)",
            "  +-------------------------------------------------------+-------------------------------------------------------+",
            "  |                                  SW-FINBANK (Switch Catalyst 2960-24TT)                                       |",
            "  +-----------------------+-------------------------------+-------------------------------+-----------------------+",
            "                          | Portas Fa0/1 e Fa0/2          | Portas Fa0/6 e Fa0/7          | Portas Fa0/11 e Fa0/12",
            "                          v                               v                               v",
            "  +-------------------------------+       +---------------+---------------+       +---------------+---------------+",
            "  |       SETOR ATENDIMENTO       |       |       OPERAÇÕES & ADMIN       |       |     SERVIDORES DATA CENTER    |",
            "  |           (VLAN 10)           |       |           (VLAN 20)           |       |           (VLAN 30)           |",
            "  | [PC-ATEND-01] 192.168.10.11   |       | [PC-OPER-01]  192.168.20.11   |       | [SRV-WEB-BANCO] 192.168.30.10 |",
            "  | [PC-ATEND-02] 192.168.10.12   |       | [PC-ADMIN-01] 192.168.20.12   |       | [SRV-MONITOR]   192.168.30.20 |",
            "  +-------------------------------+       +-------------------------------+       +-------------------------------+"
        ]
        self.draw_rect(self.margin_x, y - 162, self.content_w, 162, fill_rgb=(0.98, 0.98, 0.99), stroke_rgb=(0.8, 0.85, 0.9), line_width=0.8)
        dy = y - 9
        for dline in diag_lines:
            self.draw_text(dline, self.margin_x + 6, dy, font="F3", size=5.5, rgb=(0.1, 0.15, 0.25))
            dy -= 6.3

        # =========================================================================
        # PÁGINA 4: DESCRIÇÃO DA INTEGRAÇÃO DO ALGORITMO COM A INFRAESTRUTURA
        # =========================================================================
        self.new_page()
        self.add_header(4, 4)

        # 2.5 Descrição da Integração entre o Algoritmo e a Infraestrutura
        y = self.height - 52
        self.draw_text("2.5 DESCRIÇÃO DA INTEGRAÇÃO ENTRE O ALGORITMO E A INFRAESTRUTURA DE REDE", self.margin_x, y, font="F2", size=10, rgb=(0.04, 0.15, 0.28))
        self.draw_line(self.margin_x, y - 3, self.margin_x + self.content_w, y - 3, rgb=(0.04, 0.15, 0.28), width=1)

        y -= 14
        topicos_integracao = [
            ("1. INJEÇÃO E DESPACHO DE PACOTES ICMP PELO ALGORITMO", [
                "• A integração direta ocorre através do método ping_host(ip), que invoca o executável ping nativo do sistema operacional.",
                "• Utiliza a biblioteca subprocess.run() com redirecionamento de streams (stdout/stderr = DEVNULL) para manter a console limpa.",
                "• Parâmetros de tempo limite rígidos: -w 800 (Windows) e -W 1 (Linux). Isso assegura que se um dispositivo estiver desligado",
                "  ou com cabo rompido, o software aguarda no máximo 800 milissegundos, impedindo o congelamento da aplicação."
            ], (0.96, 0.98, 1.0), (0.2, 0.4, 0.7)),

            ("2. ROTEAMENTO E TRÂNSITO INTER-VLAN (ROUTER-ON-A-STICK 802.1Q)", [
                "• Quando o monitor testa um ativo fora da sua rede local (ex: testar PC-OPER-01 em 192.168.20.11 a partir da VLAN 30):",
                "  1. O pacote Echo Request sai pela interface e é encaminhado ao Gateway Padrão 192.168.30.1.",
                "  2. O Switch Catalyst 2960 tagueia o quadro com a VLAN 30 e o envia pela porta Gig0/1 (Tronco dot1Q).",
                "  3. O Roteador Cisco 1941 recebe na Gig0/0.30, consulta a tabela de roteamento interna e o comuta para a Gig0/0.20.",
                "  4. O Roteador retagueia o pacote como VLAN 20 e o envia de volta ao switch, que entrega na porta de acesso do PC.",
                "  5. O caminho inverso é percorrido pelo Echo Reply. Se o ciclo completar, o returncode é 0 (ONLINE [OK])."
            ], (0.97, 0.99, 0.97), (0.1, 0.5, 0.3)),

            ("3. TRATAMENTO DE ESTADOS EM TEMPO REAL E MITIGAÇÃO DE FALSOS POSITIVOS", [
                "• Falsos Positivos Mitigados: Perdas transitórias de 1 único pacote ICMP não geram pânico na equipe técnica. Apenas se",
                "  a pane persistir por 3 ciclos consecutivos de varredura, o sistema emite o alarme [INDISPONIBILIDADE PERSISTENTE] (RN02).",
                "• Alarme Imediato para Ativos Vitais: Dispositivos cadastrados como CRÍTICO (Gateway R-FINBANK e Servidor Web) disparam",
                "  imediatamente o alerta [PRIORIDADE MÁXIMA] no primeiro fracasso de comunicação, acelerando a resposta da TI (RN01).",
                "• Auto-recuperação Dinâmica: Assim que a porta do switch for reativada ou o cabo for reconectado no Packet Tracer, o teste",
                "  subsequente detecta sucesso e reseta instantaneamente o acumulador de falhas seguidas para 0 (RN03)."
            ], (1.0, 0.98, 0.94), (0.7, 0.4, 0.1)),

            ("4. MODO DE SIMULAÇÃO CONTROLADA PARA DEMONSTRAÇÕES E HOMOLOGAÇÃO", [
                "• O software possui o recurso simular=True com injeção de ID alvo (ex: id_falha='SRV01').",
                "• Esse mecanismo permite simular com exatidão matemática o comportamento de rompimento de cabo e queda de serviços",
                "  em apresentações acadêmicas ou testes isolados, validando o cálculo de Uptime % sem necessidade de desligar ativos reais."
            ], (0.98, 0.98, 0.98), (0.3, 0.3, 0.3))
        ]

        for ititle, ilines, ifill, istroke in topicos_integracao:
            h_box = len(ilines) * 11 + 22
            self.draw_rect(self.margin_x, y - h_box, self.content_w, h_box, fill_rgb=ifill, stroke_rgb=istroke, line_width=0.8)
            self.draw_text(ititle, self.margin_x + 8, y - 12, font="F2", size=7.8, rgb=istroke)
            ly = y - 23
            for line in ilines:
                self.draw_text(line, self.margin_x + 8, ly, font="F1", size=6.8, rgb=(0.15, 0.15, 0.15))
                ly -= 10.5
            y -= (h_box + 8)

        # Caixa Conclusiva de Homologação
        y -= 2
        self.draw_rect(self.margin_x, y - 32, self.content_w, 32, fill_rgb=(0.95, 0.98, 1.0), stroke_rgb=(0.25, 0.45, 0.8), line_width=1)
        self.draw_text("CONCLUSÃO DA MODELAGEM TÉCNICA:", self.margin_x + 8, y - 10, font="F2", size=7.8, rgb=(0.1, 0.25, 0.55))
        self.draw_text("A modelagem atende 100% aos requisitos de software e infraestrutura, garantindo integração contínua entre a camada lógica", self.margin_x + 8, y - 19, font="F1", size=7.2, rgb=(0.2, 0.2, 0.2))
        self.draw_text("em Python 3 e os segmentos de rede do FinBank Digital simulados no Cisco Packet Tracer.", self.margin_x + 8, y - 28, font="F1", size=7.2, rgb=(0.2, 0.2, 0.2))

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
    out_pdf = r"C:\Users\jamerson.albuquerque\.gemini\antigravity\scratch\finbank_digital\FinBank_Digital_Modelagem_Solucao.pdf"
    gerador = ModelagemSolucaoPDF(out_pdf)
    gerador.build_pdf()
    print("PDF da Modelagem da Solucao gerado com sucesso em:", out_pdf)
