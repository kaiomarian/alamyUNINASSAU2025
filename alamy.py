# Importações da biblioteca Kivy
import kivy
from kivy.app import App                        # Base para criar aplicativos
from kivy.uix.floatlayout import FloatLayout    # Layout livre, onde os elementos são posicionados por coordenadas relativas
from kivy.uix.textinput import TextInput        # Campo de entrada de texto
from kivy.uix.label import Label                # Componente para exibir textos
from kivy.uix.gridlayout import GridLayout      # Layout em grade, útil para exibir listas
from kivy.utils import get_color_from_hex       # Converte cores hexadecimais para formato do Kivy
from kivy.core.window import Window             # Permite modificar a janela do app (cor de fundo, tamanho etc.)

# Classe principal do aplicativo
class orcamentofam(App):
    def build(self):
        # Inicialização de variáveis
        self.qnt_familiares = 0              # Quantidade de familiares
        self.familiares_info = []            # Lista que guarda os dados de cada familiar
        self.pessoa_atual = 1                # Índice do familiar que está sendo preenchido
        self.etapa = 'inicio'                # Etapa atual do preenchimento (controle de fluxo)

        self.total_despesas = 0              # Número de despesas do familiar atual
        self.despesa_atual = 1               # Qual despesa está sendo preenchida agora

        # Layout principal do app
        self.layoutprincipal = FloatLayout()

        # Campo de entrada de texto inicial
        self.entrada = TextInput(
            hint_text='Quantos familiares você tem?',                     # Texto de dica no campo
            hint_text_color=get_color_from_hex('2E522C'),                # Cor do hint text
            background_color=get_color_from_hex('BAFFC0'),               # Cor de fundo do campo
            foreground_color=get_color_from_hex('000000'),              # Cor do texto digitado
            multiline=False,                                            # Apenas uma linha
            size_hint=(0.9, 0.22),                                       # Tamanho relativo
            pos_hint={'center_x': 0.5, 'center_y': 0.85}                # Posição relativa na tela
        )
        self.entrada.bind(on_text_validate=self.proxima_etapa)           # Quando o usuário aperta "Enter", chama proxima_etapa
        self.layoutprincipal.add_widget(self.entrada)                    # Adiciona o campo ao layout principal

        # Área onde será exibida a matriz com dados dos familiares
        self.matriz = GridLayout(cols=1, size_hint=(0.9, 0.55), pos_hint={'center_x': 0.5, 'y': 0.05})
        self.layoutprincipal.add_widget(self.matriz)

        # Configuração visual da janela
        Window.clearcolor = get_color_from_hex('#DEFFDA')               # Cor de fundo da janela
        Window.size = (700, 600)                                        # Tamanho da janela

        return self.layoutprincipal

    # Função chamada quando o usuário aperta "Enter"
    def proxima_etapa(self, instance):
        texto = self.entrada.text.strip()  # Pega o texto digitado e remove espaços extras

        # ETAPA 1: Quantidade de familiares
        if self.etapa == 'inicio':
            try:
                self.qnt_familiares = int(texto)                        # Converte entrada para inteiro
                self.entrada.text = ''                                  # Limpa o campo
                self.etapa = 'despesas'                                 # Vai para próxima etapa
                self.entrada.hint_text = 'Quantas despesas o familiar %i tem?' % self.pessoa_atual
            except ValueError:
                self.entrada.text = ''
                self.entrada.hint_text = 'Insira um número válido. \nuse pontos (.) para números decimáis'

        # ETAPA 2: Número de despesas do familiar atual
        elif self.etapa == 'despesas':
            try:
                self.total_despesas = int(texto)
                self.entrada.text = ''
                self.familiares_info.append({'despesas': [], 'salario': 0})  # Adiciona dicionário para o familiar atual
                self.despesa_atual = 1
                self.etapa = 'valores_despesas'
                self.entrada.hint_text = 'Valor da despesa %i do familiar %i?' % (self.despesa_atual, self.pessoa_atual)
            except ValueError:
                self.entrada.text = ''
                self.entrada.hint_text = 'Insira um número válido. \nuse pontos (.) para números decimáis'

        # ETAPA 3: Valores de cada despesa
        elif self.etapa == 'valores_despesas':
            try:
                valor = float(texto)
                self.entrada.text = ''
                self.familiares_info[self.pessoa_atual - 1]['despesas'].append(valor)  # Adiciona valor na lista de despesas

                if self.despesa_atual < self.total_despesas:
                    self.despesa_atual += 1
                    self.entrada.hint_text = 'Valor da despesa %i do familiar %i?' % (self.despesa_atual, self.pessoa_atual)
                else:
                    self.etapa = 'salario'
                    self.entrada.hint_text = 'Salário do familiar %i?' % self.pessoa_atual
            except ValueError:
                self.entrada.text = ''
                self.entrada.hint_text = 'Insira um valor numérico para a despesa %i. \nuse pontos (.) para números decimáis' % self.despesa_atual

        # ETAPA 4: Salário do familiar
        elif self.etapa == 'salario':
            try:
                salario = float(texto)
                self.entrada.text = ''
                self.familiares_info[self.pessoa_atual - 1]['salario'] = salario

                if self.pessoa_atual < self.qnt_familiares: #checa se ainda tem pessoas sobrando
                    self.pessoa_atual += 1
                    self.etapa = 'despesas'
                    self.entrada.hint_text = 'Quantas despesas o familiar %i tem?' % self.pessoa_atual
                else:
                    self.etapa = 'resultado'
                    self.calc_orcamento()  # Quando termina todos os familiares, calcula o orçamento
            except ValueError:
                self.entrada.text = ''
                self.entrada.hint_text = 'Insira um valor numérico para o salário. \nuse pontos (.) para números decimáis'

    # Função que calcula orçamento total
    def calc_orcamento(self):
        total_salario = sum(fam['salario'] for fam in self.familiares_info)          # Soma dos salários
        total_despesas = sum(sum(fam['despesas']) for fam in self.familiares_info)   # Soma de todas as despesas de td mundo
        orcamento = total_salario - total_despesas                               # orçamento final

        self.entrada.text = ''
        self.entrada.hint_text = 'Orçamento total: R$ %.2f' % orcamento
        self.entrada.focus = True

        self.mostrar_matriz()  # Chama função para mostrar tabela de dados

    # Função que mostra os dados na matriz (tabela)
    def mostrar_matriz(self):
        self.matriz.clear_widgets()  # Remove widgets antigos da tela

        # Determina qual familiar teve mais despesas para padronizar a exibição
        max_despesas = max(len(fam['despesas']) for fam in self.familiares_info)

        # Criação do cabeçalho
        cabecalho = 'Familiar'
        for i in range(1, max_despesas + 1):
            cabecalho += ' | Despesa %i' % i
        cabecalho += ' | Salário'
        self.matriz.add_widget(Label(text=cabecalho,
                                      size_hint_y=None,
                                      height=30,
                                      color = get_color_from_hex("#375A39")))

        # Adiciona cada linha com os dados dos familiares
        for i, familiar in enumerate(self.familiares_info, start=1):
            despesas = familiar['despesas'][:]
            while len(despesas) < max_despesas:
                despesas.append(0.0)  # Preenche com zero se tiver menos despesas que o máximo

            linha = '   %i' % i
            for valor in despesas:
                linha += '       | %.2f' % valor
            linha += '   | %.2f' % familiar['salario']
            self.matriz.add_widget(Label(text=linha,
                                          size_hint_y=None,
                                            height=25,
                                            color = get_color_from_hex('#375A39')))


# Executa o aplicativo
if __name__ == '__main__':
    orcamentofam().run()
