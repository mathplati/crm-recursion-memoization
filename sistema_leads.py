import os
os.system("cls")

from typing import List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class Lead:
    id: int
    nome: str
    telefone: str
    email: str
    cpf: str

    def normalizado(self):
        return (
            self.nome.lower().strip(),
            ''.join(filter(str.isdigit, self.telefone)),
            self.email.lower().strip(),
            ''.join(filter(str.isdigit, self.cpf)),
        )


@dataclass
class Horario:
    inicio: datetime
    fim: datetime

    def slots(self, duracao: int = 30) -> List[Tuple[datetime, datetime]]:
        atual = self.inicio
        delta = timedelta(minutes=duracao)
        s = []
        while atual + delta <= self.fim:
            prox = atual + delta
            s.append((atual, prox))
            atual = prox
        return s


def verificar_duplicidade_recursiva(novo, cadastros, idx=0, novo_norm=None):
    if idx >= len(cadastros):
        return False, None, []

    if novo_norm is None:
        novo_norm = novo.normalizado()

    atual = cadastros[idx]
    nome_n, tel_n, email_n, cpf_n = novo_norm
    nome_a, tel_a, email_a, cpf_a = atual.normalizado()

    campos = []

    if cpf_n and cpf_n == cpf_a:
        campos.append('cpf')

    if email_n and email_n == email_a:
        campos.append('email')

    if tel_n and tel_n == tel_a:
        if set(nome_n.split()) & set(nome_a.split()):
            campos.extend(['telefone', 'nome'])

    if campos:
        return True, atual, campos

    return verificar_duplicidade_recursiva(novo, cadastros, idx + 1, novo_norm)


class VerificadorMemoizado:
    def __init__(self):
        self.cache = {}
        self.comparacoes = 0
        self.cache_hits = 0

    def _chave(self, l1, l2):
        return tuple(sorted((l1.normalizado(), l2.normalizado())))

    def verificar(self, novo, cadastros, idx=0, novo_norm=None):
        if idx >= len(cadastros):
            return False, None, []

        if novo_norm is None:
            novo_norm = novo.normalizado()

        atual = cadastros[idx]
        chave = self._chave(novo, atual)

        if chave in self.cache:
            self.cache_hits += 1
            dup, campos = self.cache[chave]
            if dup:
                return True, atual, campos
        else:
            self.comparacoes += 1
            nome_n, tel_n, email_n, cpf_n = novo_norm
            nome_a, tel_a, email_a, cpf_a = atual.normalizado()

            campos = []

            if cpf_n and cpf_n == cpf_a:
                campos.append('cpf')

            if email_n and email_n == email_a:
                campos.append('email')

            if tel_n and tel_n == tel_a:
                if set(nome_n.split()) & set(nome_a.split()):
                    campos.extend(['telefone', 'nome'])

            dup = bool(campos)
            self.cache[chave] = (dup, campos)

            if dup:
                return True, atual, campos

        return self.verificar(novo, cadastros, idx + 1, novo_norm)


def otimizar_agenda(slots, n, pref=None, memo=None, idx=0):
    if memo is None:
        memo = {}

    chave = (idx, n)
    if chave in memo:
        return memo[chave]

    if n == 0:
        return {'slots': [], 'score': 0}

    if idx >= len(slots):
        return {'slots': [], 'score': float('-inf')}

    sem = otimizar_agenda(slots, n, pref, memo, idx + 1)
    com = otimizar_agenda(slots, n - 1, pref, memo, idx + 1)

    inicio = slots[idx][0]
    score = 100

    if pref:
        score -= abs((inicio - pref).total_seconds() / 60) * 0.5

    if inicio.hour < 10:
        score += 10

    if com['score'] != float('-inf'):
        com_result = {
            'slots': [slots[idx]] + com['slots'],
            'score': score + com['score']
        }
    else:
        com_result = {'slots': [], 'score': float('-inf')}

    result = com_result if com_result['score'] > sem['score'] else sem

    memo[chave] = result
    return result


def main():
    print("=" * 60)
    print("SISTEMA DE GESTAO DE LEADS E AGENDAMENTO")
    print("=" * 60)

    cadastros = [
        Lead(1, "Joao Silva", "(11) 98765-4321", "joao@email.com", "123.456.789-00"),
        Lead(2, "Maria Santos", "(21) 91234-5678", "maria@email.com", "987.654.321-00"),
    ]

    print("\n[TAREFA 1] Verificacao Recursiva:")
    print("-" * 50)

    testes = [
        Lead(3, "Joao S.", "(11) 99999-9999", "novo@email.com", "123.456.789-00"),
        Lead(4, "Joao Silva", "(11) 98765-4321", "outro@email.com", "000.000.000-00"),
        Lead(5, "Carlos Novo", "(41) 98888-7777", "carlos@email.com", "111.222.333-44"),
    ]

    for lead in testes:
        dup, exist, campos = verificar_duplicidade_recursiva(lead, cadastros)
        status = "DUPLICADO" if dup else "NOVO"
        print(f"  {lead.nome:15} -> {status}")
        if dup:
            print(f"     Igual a: {exist.nome} (campos: {campos})")

    print("\n[TAREFA 2] Memoizacao:")
    print("-" * 50)

    vm = VerificadorMemoizado()
    leads_t2 = [
        Lead(6, "Teste A", "(11) 11111-1111", "a@a.com", "111.111.111-11"),
        Lead(7, "Teste B", "(22) 22222-2222", "b@b.com", "222.222.222-22"),
        Lead(8, "Teste A", "(11) 11111-1111", "a@a.com", "111.111.111-11"),
    ]

    for lead in leads_t2:
        vm.verificar(lead, cadastros)

    total = vm.comparacoes + vm.cache_hits
    print(f"  Comparacoes: {vm.comparacoes}")
    print(f"  Cache hits: {vm.cache_hits}")
    print(f"  Eficiencia: {vm.cache_hits/total*100:.1f}%")

    print("\n[TAREFA 3] Otimizacao de Agenda:")
    print("-" * 50)

    base = datetime(2026, 4, 3, 8, 0)
    h = Horario(base, base + timedelta(hours=4))
    s = h.slots()

    print(f"  Horario: 08:00 - 12:00")
    print(f"  Slots: {len(s)} (30min)")
    print(f"  Consultas: 3")
    print(f"  Preferencia: 10:00")

    resultado = otimizar_agenda(s, 3, base + timedelta(hours=2))

    print(f"\n  Resultado:")
    for i, slot in enumerate(resultado['slots'], 1):
        print(f"    {i}. {slot[0].strftime('%H:%M')} - {slot[1].strftime('%H:%M')}")

    print(f"\n  Score: {resultado['score']:.1f}")

    print("\n" + "=" * 60)
    print("Sistema funcionando corretamente!")
    print("=" * 60)


if __name__ == "__main__":
    main()
