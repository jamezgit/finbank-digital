#!/usr/bin/env python3
"""
FinBank Digital - Sistema Educacional de Monitoramento de Rede
Projeto 02 - Infraestrutura e Monitoramento de Redes
Requisitos Funcionais: RF01 a RF06
"""

import sys
import time
import platform
import subprocess
from datetime import datetime

class Dispositivo:
    def __init__(self, id_disp, nome, ip, setor, servico, criticidade):
        self.id = id_disp
        self.nome = nome
        self.ip = ip
        self.setor = setor
        self.servico = servico
        self.criticidade = criticidade.upper()  # 'CRITICO', 'ALTA' ou 'NORMAL'
        self.historico = []  # Lista de registros: {'data': ..., 'status': 'SUCESSO'/'FALHA'}
        self.falhas_consecutivas = 0

    def registrar_verificacao(self, status):
        agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        resultado = "SUCESSO" if status else "FALHA"
        self.historico.append({
            "data": agora,
            "status": resultado
        })
        if status:
            self.falhas_consecutivas = 0
        else:
            self.falhas_consecutivas += 1

    def calcular_disponibilidade(self):
        if not self.historico:
            return 100.0
        sucessos = sum(1 for reg in self.historico if reg["status"] == "SUCESSO")
        return round((sucessos / len(self.historico)) * 100, 2)


class MonitorFinBank:
    def __init__(self):
        self.dispositivos = {}
        self.carregar_topologia_padrao()

    def carregar_topologia_padrao(self):
        # RF01 - Cadastro de dispositivos e serviços
        dados = [
            Dispositivo("R01", "R-FINBANK", "192.168.30.1", "Core / Gateway", "Roteamento 802.1Q", "CRITICO"),
            Dispositivo("SRV01", "SRV-WEB-BANCO", "192.168.30.10", "Servidores", "HTTP Web / DNS", "CRITICO"),
            Dispositivo("SRV02", "SRV-MONITOR", "192.168.30.20", "Servidores", "Syslog / Eventos", "NORMAL"),
            Dispositivo("PC01", "PC-ATEND-01", "192.168.10.11", "Atendimento", "Estacao Cliente", "NORMAL"),
            Dispositivo("PC02", "PC-OPER-01", "192.168.20.11", "Operacoes", "Terminal Financeiro", "ALTA"),
            Dispositivo("PC03", "PC-ADMIN-01", "192.168.20.12", "Administracao", "Gestao Operacional", "NORMAL")
        ]
        for d in dados:
            self.dispositivos[d.id] = d

    def cadastrar_dispositivo(self, id_disp, nome, ip, setor, servico, criticidade):
        if id_disp in self.dispositivos:
            print(f"[ERRO] Dispositivo ID {id_disp} ja existente.")
            return
        self.dispositivos[id_disp] = Dispositivo(id_disp, nome, ip, setor, servico, criticidade)
        print(f"[SUCESSO] Dispositivo '{nome}' registrado.")

    def ping_host(self, ip):
        param = "-n" if platform.system().lower() == "windows" else "-c"
        comando = ["ping", param, "1", "-w", "800", ip]
        try:
            res = subprocess.run(comando, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return res.returncode == 0
        except Exception:
            return False

    def executar_verificacao(self, simular=False, id_falha=None):
        print("\n" + "="*75)
        modo = f"SIMULADO (Falha forçada no ativo: {id_falha})" if simular else "REAL (ICMP Ping)"
        print(f"CICLO DE VERIFICAÇÃO DE DISPONIBILIDADE - MODO: {modo}")
        print("="*75)

        for id_d, disp in self.dispositivos.items():
            if simular:
                status = False if id_d == id_falha else True
            else:
                status = self.ping_host(disp.ip)

            disp.registrar_verificacao(status)
            status_txt = "ONLINE [OK]" if status else "OFFLINE [FALHA]"
            print(f"[{disp.criticidade:<7}] {disp.nome:<16} ({disp.ip:<15}) -> {status_txt}")

            # Regras de Negócio: Criticidade e Falha Persistente (3 consecutivas)
            if not status:
                if disp.criticidade in ["CRITICO", "ALTA"]:
                    print(f"  >>> [ALERTA DE PRIORIDADE MÁXIMA] Ativo CRÍTICO ({disp.nome}) sem comunicação!")
                
                if disp.falhas_consecutivas >= 3:
                    print(f"  >>> [ALERTA DE INDISPONIBILIDADE PERSISTENTE] {disp.nome} acumulou {disp.falhas_consecutivas} falhas consecutivas!")

    def consultar_historico(self, id_disp):
        disp = self.dispositivos.get(id_disp)
        if not disp:
            print(f"[ERRO] Dispositivo '{id_disp}' nao encontrado.")
            return
        
        print(f"\n" + "-"*65)
        print(f"HISTÓRICO DE VERIFICAÇÕES: {disp.nome} ({disp.ip}) - Setor: {disp.setor}")
        print(f"Criticidade: {disp.criticidade} | Serviço: {disp.servico}")
        print("-"*65)
        if not disp.historico:
            print("Nenhum registro encontrado.")
            return
        
        for idx, reg in enumerate(disp.historico, 1):
            print(f"Check #{idx:<2} | Data/Hora: {reg['data']} | Resultado: {reg['status']}")

    def gerar_relatorio_geral(self):
        print("\n" + "="*85)
        print("RELATÓRIO CONSOLIDADO DE DISPONIBILIDADE - FINBANK DIGITAL")
        print("="*85)
        print(f"{'ID':<6}{'Dispositivo':<16}{'Setor':<16}{'Criticidade':<13}{'Disponibilidade':<18}{'Status Falhas'}")
        print("-"*85)
        for disp in self.dispositivos.values():
            pct = f"{disp.calcular_disponibilidade()}%"
            if disp.falhas_consecutivas >= 3:
                status_f = f"PERSISTENTE ({disp.falhas_consecutivas} falhas)"
            elif disp.falhas_consecutivas > 0:
                status_f = f"Intermitente ({disp.falhas_consecutivas} falha)"
            else:
                status_f = "Estável (0 falhas)"
            print(f"{disp.id:<6}{disp.nome:<16}{disp.setor:<16}{disp.criticidade:<13}{pct:<18}{status_f}")
        print("="*85)


def main():
    monitor = MonitorFinBank()
    while True:
        print("\n==============================================")
        print("   FINBANK DIGITAL - MONITOR DE REDE")
        print("==============================================")
        print("1. Executar Verificação Real (Ping na Rede)")
        print("2. Simular Verificação com Falha (Teste de Alerta)")
        print("3. Consultar Histórico por Equipamento (RF03)")
        print("4. Exibir Relatório e Disponibilidade % (RF05/RF06)")
        print("5. Cadastrar Novo Dispositivo (RF01)")
        print("0. Sair")
        
        op = input("\nEscolha uma opcao: ").strip()
        if op == "1":
            monitor.executar_verificacao(simular=False)
        elif op == "2":
            print("\nAtivos disponíveis para simulação:", list(monitor.dispositivos.keys()))
            alvo = input("Digite o ID do dispositivo que deve falhar (ex: SRV01): ").strip().upper()
            monitor.executar_verificacao(simular=True, id_falha=alvo)
        elif op == "3":
            id_d = input("Digite o ID do dispositivo: ").strip().upper()
            monitor.consultar_historico(id_d)
        elif op == "4":
            monitor.gerar_relatorio_geral()
        elif op == "5":
            id_d = input("ID (ex: PC04): ")
            nome = input("Nome do Equipamento: ")
            ip = input("Endereço IP: ")
            setor = input("Setor: ")
            servico = input("Serviço: ")
            crit = input("Criticidade (CRITICO / ALTA / NORMAL): ")
            monitor.cadastrar_dispositivo(id_d, nome, ip, setor, servico, crit)
        elif op == "0":
            print("\nEncerrando sistema de monitoramento.")
            sys.exit(0)
        else:
            print("[AVISO] Opção inválida!")

if __name__ == "__main__":
    main()
