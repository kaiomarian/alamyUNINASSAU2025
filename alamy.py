import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.utils import get_color_from_hex
from kivy.core.window import Window
class orcamentofam(App):
    def build(self):
        self.qnt_familiares = 0
        self.familiares_info = []
        self.pessoa_atual = 1
        self.etapa = 'inicio'

        self.total_despesas = 0
        self.despesa_atual = 1

        self.layoutprincipal = FloatLayout()

        self.entrada = TextInput(
            hint_text='Quantos familiares você tem?',
            hint_text_color=get_color_from_hex('2E522C'),
            background_color=get_color_from_hex('BAFFC0'),
            foreground_color=get_color_from_hex('000000'),
            multiline=False,
            size_hint=(0.9, 0.22),
            pos_hint={'center_x': 0.5, 'center_y': 0.85}
        )
        self.entrada.bind(on_text_validate=self.proxima_etapa)
        self.layoutprincipal.add_widget(self.entrada)

        Window.clearcolor = get_color_from_hex('#DEFFDA')
        Window.size = (300, 300)
        return self.layoutprincipal

    def proxima_etapa(self, instance):
        texto = self.entrada.text.strip()

        if self.etapa == 'inicio':
            try:
                self.qnt_familiares = int(texto)
                self.entrada.text = ''
                self.etapa = 'despesas'
                self.entrada.hint_text = 'Quantas despesas o familiar %i tem?' % self.pessoa_atual
            except ValueError:
                self.entrada.text = ''
                self.entrada.hint_text = 'Insira um número válido de familiares.'

        elif self.etapa == 'despesas':
            try:
                self.total_despesas = int(texto)
                self.entrada.text = ''
                self.familiares_info.append({'despesas': [], 'salario': 0})
                self.despesa_atual = 1
                self.etapa = 'valores_despesas'
                self.entrada.hint_text = 'Valor da despesa %i do familiar %i?' % (
                    self.despesa_atual, self.pessoa_atual)
            except ValueError:
                self.entrada.text = ''
                self.entrada.hint_text = 'Insira um número válido de despesas.'

        elif self.etapa == 'valores_despesas':
            try:
                valor = float(texto)
                self.entrada.text = ''
                self.familiares_info[self.pessoa_atual - 1]['despesas'].append(valor)

                if self.despesa_atual < self.total_despesas:
                    self.despesa_atual += 1
                    self.entrada.hint_text = 'Valor da despesa %i do familiar %i?' % (
                        self.despesa_atual, self.pessoa_atual)
                else:
                    self.etapa = 'salario'
                    self.entrada.hint_text = 'Salário do familiar %i?' % self.pessoa_atual
            except ValueError:
                self.entrada.text = ''
                self.entrada.hint_text = 'Insira um valor numérico para a despesa %i.' % self.despesa_atual

        elif self.etapa == 'salario':
            try:
                salario = float(texto)
                self.entrada.text = ''
                self.familiares_info[self.pessoa_atual - 1]['salario'] = salario

                if self.pessoa_atual < self.qnt_familiares:
                    self.pessoa_atual += 1
                    self.etapa = 'despesas'
                    self.entrada.hint_text = 'Quantas despesas o familiar %i tem?' % self.pessoa_atual
                else:
                    self.etapa = 'resultado'
                    self.calc_orcamento()
            except ValueError:
                self.entrada.text = ''
                self.entrada.hint_text = 'Insira um valor numérico para o salário.'

        self.entrada.focus = True

    def calc_orcamento(self):
        total_salario = sum(p['salario'] for p in self.familiares_info)
        total_despesas = sum(sum(p['despesas']) for p in self.familiares_info)
        orcamento = total_salario - total_despesas

        self.entrada.text = ''
        self.entrada.hint_text = 'Orçamento total: R$ %.2f' % orcamento
        self.entrada.focus = True


if __name__ == '__main__':
    orcamentofam().run()
