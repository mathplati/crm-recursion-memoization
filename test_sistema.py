import unittest
from datetime import datetime, timedelta
from sistema_leads import Lead, Horario, verificar_duplicidade_recursiva, VerificadorMemoizado, otimizar_agenda


class TestTarefa1(unittest.TestCase):
    def setUp(self):
        self.cadastros = [
            Lead(1, "Joao Silva", "(11) 98765-4321", "joao@email.com", "123.456.789-00"),
            Lead(2, "Maria Santos", "(21) 91234-5678", "maria@email.com", "987.654.321-00"),
        ]

    def test_duplicidade_cpf(self):
        novo = Lead(3, "Joao S.", "(11) 99999-9999", "novo@email.com", "123.456.789-00")
        dup, exist, campos = verificar_duplicidade_recursiva(novo, self.cadastros)
        self.assertTrue(dup)
        self.assertEqual(exist.id, 1)
        self.assertIn('cpf', campos)

    def test_duplicidade_telefone_nome(self):
        novo = Lead(3, "Joao Silva", "(11) 98765-4321", "novo@email.com", "000.000.000-00")
        dup, exist, campos = verificar_duplicidade_recursiva(novo, self.cadastros)
        self.assertTrue(dup)
        self.assertIn('telefone', campos)
        self.assertIn('nome', campos)

    def test_sem_duplicidade(self):
        novo = Lead(3, "Carlos Novo", "(41) 98888-7777", "carlos@email.com", "111.222.333-44")
        dup, exist, campos = verificar_duplicidade_recursiva(novo, self.cadastros)
        self.assertFalse(dup)
        self.assertIsNone(exist)

    def test_lista_vazia(self):
        novo = Lead(1, "Teste", "(11) 11111-1111", "teste@email.com", "111.111.111-11")
        dup, exist, campos = verificar_duplicidade_recursiva(novo, [])
        self.assertFalse(dup)


class TestTarefa2(unittest.TestCase):
    def test_cache_funciona(self):
        v = VerificadorMemoizado()
        cadastros = [Lead(1, "Joao", "(11) 98765-4321", "joao@email.com", "123.456.789-00")]
        novo = Lead(2, "Teste", "(11) 11111-1111", "teste@email.com", "111.111.111-11")

        v.verificar(novo, cadastros)
        comp1 = v.comparacoes

        v.verificar(novo, cadastros)
        comp2 = v.comparacoes

        self.assertEqual(comp1, comp2)
        self.assertGreater(v.cache_hits, 0)

    def test_chave_simetrica(self):
        v = VerificadorMemoizado()
        a = Lead(1, "A", "(11) 11111-1111", "a@a.com", "111.111.111-11")
        b = Lead(2, "B", "(22) 22222-2222", "b@b.com", "222.222.222-22")

        k1 = v._chave(a, b)
        k2 = v._chave(b, a)
        self.assertEqual(k1, k2)


class TestTarefa3(unittest.TestCase):
    def test_agenda_basica(self):
        base = datetime(2026, 4, 3, 8, 0)
        h = Horario(base, base + timedelta(hours=4))
        slots = h.slots()

        res = otimizar_agenda(slots, 3)
        self.assertEqual(len(res['slots']), 3)

    def test_respeita_limite(self):
        base = datetime(2026, 4, 3, 8, 0)
        h = Horario(base, base + timedelta(hours=1))
        slots = h.slots()

        res = otimizar_agenda(slots, 10)
        self.assertLessEqual(len(res['slots']), 2)

    def test_preferencia(self):
        base = datetime(2026, 4, 3, 8, 0)
        h = Horario(base, base + timedelta(hours=4))
        slots = h.slots()

        pref = base + timedelta(hours=2)
        res = otimizar_agenda(slots, 2, pref)

        self.assertEqual(len(res['slots']), 2)


if __name__ == '__main__':
    unittest.main(verbosity=2)
    
