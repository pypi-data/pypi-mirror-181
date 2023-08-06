from dataclasses import dataclass, fields
from typing import Union

from unidecode import unidecode

from ..common.tipo_pessoa import TipoPessoa
from ..utils.sanitize import sanitize_cep, sanitize_cnpj, sanitize_cpf


@dataclass
class Pagador:
    """Define a representação de um objeto pagador requerido pela API.

    Parameters
    ----------
    cpfCnpj : str
        CPF (FISICA) ou CNPJ (JURIDICA) da pessoa. Aceita pontuação ('.', '-' e
        '/'). Esta pontuação é removida na validação.

    tipoPessoa: Union[str, TipoPessoa]
        Tipo de pessoa: FISICA ou JURIDICA.

    nome: str
        Nome da pessoa.

        Acentos e demais caracteres são convertidos para ASCII na validação.

        Isto é para evitar conflitos com a API do Inter...

        Caracteres do tipo '&' também não devem ser usados.

    endereco : str
        Endereço da pessoa.

    numero : str, optional
        Número da pessoa, string vazio ('') por valor padrão.

    bairro : str, optional
        Bairro da pessoa, string vazio ('') por valor padrão.

    cidade : str
        Cidade da pessoa.

    uf : str
        UF da pessoa. (Sigla de dois caracteres do estado)

    cep : str
        CEP da pessoa. Aceita pontuação ('-'). Esta pontuação é removida na
        validação.

    email : str, optional
        E-mail da pessoa, string vazio ('') por valor padrão.

    ddd : str, optional
        DDD do telefone da pessoa, string vazio ('') por valor padrão.

    telefone : str, optional
        Telefone da pessoa, string vazio ('') por valor padrão.

    Notes
    -----
    - Validações de tamanho máximo de strings são feita no __post_init__,
    assim como higienização de CPF/CNPJ e CEPS
    """

    cpfCnpj: str
    tipoPessoa: Union[str, TipoPessoa]
    nome: str
    endereco: str
    cidade: str
    uf: str
    cep: str

    numero: str = ""
    complemento: str = ""
    bairro: str = ""
    email: str = ""
    ddd: str = ""
    telefone: str = ""

    def __post_init__(self):
        self.tipoPessoa = TipoPessoa(self.tipoPessoa)

        if self.tipoPessoa == TipoPessoa.FISICA:
            self.cpfCnpj = sanitize_cpf(self.cpfCnpj)
            assert len(self.cpfCnpj) == 11
        else:
            self.cpfCnpj = sanitize_cnpj(self.cpfCnpj)
            assert len(self.cpfCnpj) == 14

        assert self.nome and 1 <= len(self.nome) <= 100
        assert self.endereco and 1 <= len(self.endereco) <= 100
        assert len(self.numero) <= 10
        assert len(self.complemento) <= 30
        assert len(self.bairro) <= 60

        assert self.cidade and len(self.cidade) <= 60
        assert self.uf and len(self.uf) == 2

        self.cep = sanitize_cep(self.cep)
        assert self.cep and len(self.cep) == 8

        assert len(self.email) <= 50
        assert self.ddd == "" or len(self.ddd) == 2
        assert len(self.telefone) <= 9

        # strip accents
        for field in fields(self):
            v = getattr(self, field.name)
            if isinstance(v, str):
                setattr(self, field.name, unidecode(v))
