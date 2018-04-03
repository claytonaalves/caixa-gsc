# encoding: utf8
import warnings
warnings.simplefilter("ignore")


import logging.config

logging.config.dictConfig({
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(name)s: %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'zeep.transports': {
            'level': 'DEBUG',
            'propagate': True,
            'handlers': ['console'],
        },
    }
})

from datetime import datetime

from zeep import xsd

from requests import Session

from zeep import Client
from zeep.transports import Transport
from zeep.wsse.username import UsernameToken

from config import Config

DATE_FORMAT = "%Y%m%d%H%M%S"

class Empresa:
    id = 'XXX000000012345'
    nome = 'EMPRESA DE TESTES'


class Chamado:
    id = '1'
    descricao = ''
    previsao_atendimento = None
    responsavel = ''
    req = ''
    wo = ''
    descricao_retorno = ''


def create_transport():
    session = Session()
    session.verify = False
    return Transport(session=session)


def create_header():
    header = xsd.Element(
        'AuthenticationInfo',
        xsd.ComplexType([
            xsd.Element('userName', xsd.String()),
            xsd.Element('password', xsd.String())
        ])
    )
    return header(userName=Config.username,
                  password=Config.password)


def create_client():
    transport = create_transport()
    url = Config.url
    return Client(url, transport=transport)


def getlist_abertura():
    header_value = create_header()
    client = create_client()
    return client.service.GetList_Abertura(Config.cpy, Config.token, "", "", "", _soapheaders=[header_value])


def getlist_reiteracao():
    header_value = create_header()
    client = create_client()
    return client.service.GetList_Reiteracao(Config.cpy, Config.token, _soapheaders=[header_value])


def set_aceite_recusa(empresa, chamado, tipo_retorno):
    data_atual = datetime.now().strftime(DATE_FORMAT)
    header_value = create_header()
    client = create_client()
    response = client.service.SetAceiteRecusa(
        arquivoxml={
            'info_arquivo': {
                'tipoarquivo': '2', # 2 = Aceite/Recusa
                'datahorageracaoarquivo': data_atual,
                'comunicacao': '2' # 2 = webservice
            },
            'info_fornecedor': {
                'idfornecedor': empresa.id,
                'nomefornecedor': empresa.nome
            },
            'retorno': {
                'codigodobanco': '104',
                'chamado_fornecedor': chamado.id,
                'previsaoatendimento': chamado.previsao_atendimento.strftime(DATE_FORMAT),
                'responsavelatendimento': chamado.responsavel,
                'tipo_retorno': tipo_retorno, # 1=aceite; 2=recusa
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


def envia_aceite(empresa, chamado):
    return set_aceite_recusa(empresa, chamado, '1')


def envia_recusa(empresa, chamado):
    return set_aceite_recusa(empresa, chamado, '2')


def envia_atualizacao(empresa, chamado, tipo='1'):
    data_atual = datetime.now().strftime(DATE_FORMAT)
    header_value = create_header()
    client = create_client()
    response = client.service.SetAtualizacao(
        arquivoxml={
            'info_arquivo': {
                'tipoarquivo': '3', # 3 = Atualizacao
                'datahorageracaoarquivo': data_atual,
                'comunicacao': '2' # 2 = webservice
            },
            'info_fornecedor': {
                'idfornecedor': empresa.id,
                'nomefornecedor': empresa.nome
            },
            'retorno': {
                'codigodobanco': '104',
                'chamado_fornecedor': chamado.id,
                'tipo_retorno': tipo, # 1 = Atualizacao, 2 = Agendamento
                'descricao': chamado.descricao, # limite de 240 caracteres
                'chamado_caixa': {
                    'no_req': chamado.req,
                    'no_wo': chamado.wo,
                    #'no_inc': '',
                    #'no_crq': '',
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
    retorno = getlist_reiteracao()
