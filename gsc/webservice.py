# encoding: utf8
import warnings
warnings.simplefilter("ignore")

from datetime import datetime

from requests import Session

from zeep import xsd
from zeep import Client
from zeep.transports import Transport

DATE_FORMAT = "%Y%m%d%H%M%S"


class Webservice:
    URL = "https://sigscint.caixa.gov.br/arsys/WSDL/public/arsapphmp-int.caixa/GSC_RF010_FornecedorExterno_V401_WS"

    def __init__(self, config):
        self.config = config

    def create_header(self):
        header = xsd.Element(
            'AuthenticationInfo',
            xsd.ComplexType([
                xsd.Element('userName', xsd.String()),
                xsd.Element('password', xsd.String())
            ])
        )
        return header(userName=self.config['username'],
                      password=self.config['password'])

    def create_client(self):
        session = Session()
        session.verify = False
        transport = Transport(session=session)
        return Client(self.URL, transport=transport)

    def getlist_abertura(self):
        header_value = self.create_header()
        client = self.create_client()
        return client.service.GetList_Abertura(
            self.config['cpy'],
            self.config['token'],
            "", "", "",
            _soapheaders=[header_value]
        )

    def getlist_reiteracao(self):
        header_value = self.create_header()
        client = self.create_client()
        return client.service.GetList_Reiteracao(
            self.config['cpy'],
            self.config['token'],
            _soapheaders=[header_value]
        )

    def envia_aceite(self, chamado):
        return self.set_aceite_recusa(chamado, '1')

    def envia_recusa(self, chamado):
        return self.set_aceite_recusa(chamado, '2')

    def set_aceite_recusa(self, chamado, tipo_retorno):
        data_atual = datetime.now().strftime(DATE_FORMAT)
        header_value = self.create_header()
        client = self.create_client()
        response = client.service.SetAceiteRecusa(
            arquivoxml={
                'info_arquivo': {
                    'tipoarquivo': '2',  # 2 = Aceite/Recusa
                    'datahorageracaoarquivo': data_atual,
                    'comunicacao': '2'  # 2 = webservice
                },
                'info_fornecedor': {
                    'idfornecedor': self.config['empresa_id'],
                    'nomefornecedor': self.config['empresa_nome']
                },
                'retorno': {
                    'codigodobanco': '104',
                    'chamado_fornecedor': chamado.id,
                    'previsaoatendimento': chamado.previsao_atendimento.strftime(DATE_FORMAT),
                    'responsavelatendimento': chamado.responsavel,
                    'tipo_retorno': tipo_retorno,  # 1=aceite; 2=recusa
                    'descricao': chamado.descricao_retorno,
                    'chamado_caixa': {
                        'no_req': chamado.req,
                        'no_wo': chamado.wo,
                    }
                }
            }
            , _soapheaders=[header_value]
        )
        return response

    def envia_atualizacao(self, chamado, tipo='1'):
        data_atual = datetime.now().strftime(DATE_FORMAT)
        header_value = self.create_header()
        client = self.create_client()
        response = client.service.SetAtualizacao(
            arquivoxml={
                'info_arquivo': {
                    'tipoarquivo': '3',  # 3 = Atualizacao
                    'datahorageracaoarquivo': data_atual,
                    'comunicacao': '2'  # 2 = webservice
                },
                'info_fornecedor': {
                    'idfornecedor': self.config['empresa_id'],
                    'nomefornecedor': self.config['empresa_nome']
                },
                'retorno': {
                    'codigodobanco': '104',
                    'chamado_fornecedor': chamado.id,
                    'tipo_retorno': tipo,  # 1 = Atualizacao, 2 = Agendamento
                    'descricao': chamado.descricao,  # limite de 240 caracteres
                    'chamado_caixa': {
                        'no_req': chamado.req,
                        'no_wo': chamado.wo,
                        # 'no_inc': '',
                        # 'no_crq': '',
                    }
                },
                'agendamento': {
                    'data': chamado.previsao_atendimento.strftime(DATE_FORMAT),
                    'contato': chamado.responsavel,
                    'telefone': chamado.telefone_responsavel
                },
                'atendimento': {
                    'data_inicio': chamado.data_inicio.strftime(DATE_FORMAT),
                    'data_fim': chamado.data_fim.strftime(DATE_FORMAT)
                },
                'servicos': {
                    'codigo1': '1',
                    'descricao1': chamado.descricao_servico,
                    'valor1': chamado.valor_servico
                }
            }
            , _soapheaders=[header_value]
        )
        return response


if __name__ == "__main__":
    pass
