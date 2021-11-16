'''
Bibliotecas utilizadas
'''
import pandas as pd
import matplotlib.pyplot as plt
import re
import numpy as np

'''
Funções Complementares 
'''

def limpezaFinal(txt):
  chars = "=*|>!:,[]'\()" 
  for chars in chars:
    txt = txt.replace(chars, '')
  txt = txt.replace('"', ' ') 
  txt = txt.replace('n', ' ') 
  return txt



class CENIPA_API:
	'''
	Esta superclasse representa um extrator com finalidade de utilizar dados públicos para entender características e correlações aeronáuticas da aviação civil brasileira nos últimos 10 anos
	'''
	def __init__(self):
		'''
		Inicializador 
  		'''
		path = './Data/df_final_aeronautico.csv'
		self.df = pd.read_csv(path, sep=';')
		
	def get_table(self):
		'''
		Essa função tem o objetivo de retornar e mostrar o Dataset dentro do terminal
  		'''
		return self.df

	def get_acidente(self):
		'''
		Essa função tem o objetivo de retornar um dataset com as colunas relevantes para analise sobre os acidentes
		'''
		cols=['aeronave_tipo_veiculo', 'aeronave_fabricante','aeronave_modelo','aeronave_motor_tipo','aeronave_assentos','aeronave_ano_fabricacao','aeronave_registro_segmento','aeronave_voo_origem','aeronave_voo_destino','aeronave_fase_operacao','codigo_ocorrencia','ocorrencia_cidade','ocorrencia_uf','ocorrencia_hora','fator_aspecto','fator_condicionante','ocorrencia_tipo']
		self.df_acidente = self.df[cols]
		return self.df_acidente       

	def get_fator_contribuinte(self):
		'''
        Essa função tem o objetivo de retornar um dataset com os fatores contribuintes para o acidente
        '''
		cols=['aeronave_ano_fabricacao','aeronave_fabricante','fator_nome','fator_aspecto','fator_condicionante','fator_area','ocorrencia_tipo','ocorrencia_tipo_categoria']
		self.df_contribuinte = self.df[cols]
		return self.df_contribuinte

	def get_aeronave(self):
		'''
        Essa função tem o objetivo de um dataset para a analise das fatores das aeronaves
        '''
		cols=['aeronave_tipo_veiculo','aeronave_fabricante','aeronave_modelo','aeronave_tipo_icao','aeronave_motor_tipo','aeronave_ano_fabricacao','aeronave_pais_fabricante','aeronave_pais_registro','aeronave_registro_categoria','aeronave_registro_segmento','aeronave_voo_origem','aeronave_voo_destino','aeronave_fase_operacao','aeronave_tipo_operacao','aeronave_nivel_dano']
		self.df_aero = self.df[cols]
		return self.df_aero

	def get_recomendacao(self):
		'''
		Essa função tem objetivo de retornar um dataset para a analise das recomendações do casos 
        '''
		cols = ['recomendacao_dia_encaminhamento', 'recomendacao_conteudo', 'recomendacao_status','recomendacao_destinatario_sigla','recomendacao_destinatario'] 
		self.df_recom = self.df[cols]
		return self.df_recom


class Insights(CENIPA_API): 
	'''
	Essa classe representa uma variedade de insights retirados e pensados a partir do dataframe de acidentes aeronáuticos apresentado na classe CENIPA_API
	'''
	def moda_coluna(self, col): 
		'''
		Essa função tem o objetivo de retornar o valor mais recorrente em uma coluna do df
		'''
		try:
			result = self.df[col].value_counts()
		except KeyError:
			raise ColunaInexistente('Essa coluna não existe')

		restr = str(result)
		res = re.search(r'\w[^\n]+',restr)
		reestr = str(res) 
		a = re.findall(r"\='[^\'']+",reestr)
		astr = str(a)
		self.resultado = limpezaFinal(astr)        
		return self.resultado

	def mediana_coluna(self, col):
		'''
		Essa função tem o objetivo de retornar a mediana de uma coluna do dataset
		'''
		result = self.df[col].median()
		restr = str(result)
		res = re.search(r'\w[^\n]+',restr)
		reestr = str(res)
		a = re.findall(r"\='[^\'']+",reestr)
		astr = str(a)
		self.resultado = limpezaFinal(astr)
		return self.resultado

	def media_coluna(self,col):
		'''
		Essa função tem o objetivo de retornar a média de uma coluna do dataset
		'''
		try:
			self.result = self.df[col].mean()
		except ValueError:
		    raise ColunaNaoCalculavel('Essa coluna não é de um tipo calculável.')
		return self.result
        
	def variancia_coluna(self,col):
		'''
		Essa função tem o objetivo de retornar a variancia de uma coluna do dataset
		'''
		try:
			self.result = np.var(self.df[col])
		except ValueError:
			raise ColunaNaoCalculavel('Essa coluna não é de um tipo calculável.')
		return self.result
 
	def desvio_padrao_coluna(df):
		'''
		Essa função tem o objetivo de retornar o desvio padrão de uma coluna do dataset
		'''
		try:
			self.result = self.df[col].std()
		except ValueError:
			raise ColunaNaoCalculavel('Essa coluna não é de um tipo calculável.')
		return self.result
 
	def gravidade_acidentes(self): 
		'''
		Essa função tem o objetivo de a partir de gerar o número de mortes totais e alguns gráficos com insights sobrer nível de dano, fatalidade e classificação da ocorrência
  		'''
		df_ta = self.df[['aeronave_nivel_dano', 'ocorrencia_classificacao', 'aeronave_fatalidades_total']]
		num_mortes = df_ta['aeronave_fatalidades_total'].sum()
		print(f'Houveram \033[91m{num_mortes}\033[0m mortes neste período de 10 anos de análise de ocorrências')
  
		fig, ax = plt.subplots(figsize=(10,10), subplot_kw=dict(aspect='equal'))
		labels = ['Dano substancial','Destruída','Dano leve','Nenhum dano']
		sizes = [df_ta['aeronave_nivel_dano'].value_counts()[0], df_ta['aeronave_nivel_dano'].value_counts()[1], df_ta['aeronave_nivel_dano'].value_counts()[2], df_ta['aeronave_nivel_dano'].value_counts()[3]]
		colors = ['darkorange','gold','tomato','lightgreen']
		wedges, texts, pct = ax.pie(sizes, startangle=90, colors=colors, pctdistance=1.1, autopct=lambda p : '{:.2f}%\n({:.0f})'.format(p,p * sum(sizes)/100))
		plt.setp(pct, size=18)
		plt.rcParams['font.size'] = 13
		plt.legend(labels, title= 'Legenda de nível:')
		ax.set_title('Porcentagem por nível de dano')
		plt.show()	
  
		fig, ax = plt.subplots(figsize=(10,10), subplot_kw=dict(aspect='equal'))
		labels = ['Dano substancial','Dano leve','Destruída','Nenhum dano']
		sizes = [df_ta.loc[df_ta['aeronave_nivel_dano'] == 'SUBSTANCIAL', 'aeronave_fatalidades_total'].sum(), df_ta.loc[df_ta['aeronave_nivel_dano'] == 'LEVE', 'aeronave_fatalidades_total'].sum(), df_ta.loc[df_ta['aeronave_nivel_dano'] == 'DESTRUÍDA', 'aeronave_fatalidades_total'].sum(), df_ta.loc[df_ta['aeronave_nivel_dano'] == 'NENHUM', 'aeronave_fatalidades_total'].sum()] 
		colors = ['deepskyblue','darkblue','lightblue','dodgerblue']
		explode = (0, 0, 0.1, 0) 
		wedges, texts, pct = ax.pie(sizes, explode=explode, startangle=90, colors=colors, pctdistance=1.1, autopct=lambda p : '{:.2f}%\n({:.0f})'.format(p,p * sum(sizes)/100))
		plt.setp(pct, size=18)
		plt.rcParams['font.size'] = 13
		plt.legend(labels, title= 'Legenda de nível:')
		ax.set_title('Porcentagem por quantidade de fatalidade em cada nível de dano')
		plt.show()
  
		fig, ax = plt.subplots(figsize=(10,10), subplot_kw=dict(aspect='equal'))
		labels = ['Acidente','Incidente','Incidente grave']
		sizes = [df_ta['ocorrencia_classificacao'].value_counts()[0], df_ta['ocorrencia_classificacao'].value_counts()[1], df_ta['ocorrencia_classificacao'].value_counts()[2]]
		colors = ['darkorange','lightgreen','gold']
		wedges, texts, pct = ax.pie(sizes, startangle=90, colors=colors, pctdistance=1.1, autopct=lambda p : '{:.2f}%\n({:.0f})'.format(p,p * sum(sizes)/100))
		plt.setp(pct, size=18)
		plt.rcParams['font.size'] = 13
		plt.legend(labels, title= 'Legenda de nível:')
		ax.set_title('Porcentagem por classificação da ocorrência')
		plt.show()	 
		
	def top_aeronaves(self): #FAZER
		'''
		Essa função tem o objetivo de 
  		'''
		df['aeronave_registro_categoria']
		pass

	def tipo_aeronave(self):#FAZER
		'''
		Essa função tem o objetivo de 
  		'''
		df['aeronave_registro_segmento']
		pass

	def top_fatores_contribuintes(self):#FAZER
		'''
		Essa função tem o objetivo de 
  		'''
		df['fator_nome', 'fator_aspecto','fator_condicionante','fator_area']
		pass

	def ocorrencia_tipo(self): #FAZER
		'''
		Essa função tem o objetivo de 
  		'''
		df['ocorrencia_tipo','ocorrencia_tipo_categoria']
		pass

	def ocorrencia_estados(self, nome_UF): 
		'''
		Essa função tem o objetivo de filtrar ocorrências pela sigla dos estados
  		'''
		estado = self.df.loc[(self.df['ocorrencia_uf']==nome_UF.upper())]
		if len(estado)==0:
			raise ExceçãoEstadoInexistente('Não há ocorrências para esse estado')
		return estado
		
	def ocorrencia_cidade(self, nome_cidade): 
		'''
		Essa função tem o objetivo de filtrar ocorrências pelo nome de cidades
		'''
		cidade = self.df.loc[(self.df['ocorrencia_cidade']==nome_cidade.upper())]
		if len(cidade)==0:
			raise ExceçãoCidadeInexistente('Não há ocorrências para essa cidade')
		return cidade

	def informacoes_acidentes(self): 
		'''
		Essa função tem o objetivo de retornar informações sobre a gravidade e detalhes de fatalidade do acidente
  		'''
		return self.df[['aeronave_nivel_dano', 'ocorrencia_classificacao', 'aeronave_fatalidades_total']]

	def ocorrencia_MesHora(self): #FAZER
		'''
		Essa função tem o objetivo de 
  		'''
		df['ocorrencia_dia','ocorrencia_hora']
		pass

class ColunaInexistente(Exception):
    pass

class ColunaNaoCalculavel(Exception):
    pass


'''
Utilize o espaço abaixo para rodar as funções que deseja utilizar, não se esqueça de chamar a classe desejada antes de usufruir da função dentro da mesma
'''
