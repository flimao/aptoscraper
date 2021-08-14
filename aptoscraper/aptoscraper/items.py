# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import Compose, TakeFirst

def fillzero(valor):
    try:
        if len(valor) == 0:
            return [ 0 ]
    except TypeError:  # not iterable
        if not valor:
            return [ 0 ]
    
    return valor

# ZAP Imóveis

def fill_link(link_rel):            
    linkdom = r"https://www.zapimoveis.com.br"
    
    if not link_rel.startswith(r'/'):
        linkdom += r'/'

    return rf'{linkdom}{link_rel}'
    

class ZAPItem(scrapy.Item):
    id = scrapy.Field()
    origem = scrapy.Field()
    impulsao = scrapy.Field()
    area = scrapy.Field()
    desc = scrapy.Field()
    nquartos = scrapy.Field(
        output_processor = TakeFirst()
    )
    nbanheiros = scrapy.Field(
        output_processor = TakeFirst()
    )
    nsuites = scrapy.Field(
        output_processor = TakeFirst()
    )
    nvagas = scrapy.Field(
        output_processor = TakeFirst()
    )
    preco = scrapy.Field(
        output_processor = TakeFirst()
    )
    despesa_mes = scrapy.Field(
        output_processor = TakeFirst()
    )
    despesa_ano = scrapy.Field(
        output_processor = TakeFirst()
    )
    iptu = scrapy.Field(
        output_processor = TakeFirst()
    )
    amenidades = scrapy.Field()
    endereco_cep = scrapy.Field()
    endereco_pais = scrapy.Field()
    endereco_estado = scrapy.Field()
    endereco_cidade = scrapy.Field()
    endereco_bairro = scrapy.Field()
    endereco_rua = scrapy.Field()
    endereco_complemento = scrapy.Field()
    pois = scrapy.Field()
    contato_fones = scrapy.Field()
    contato_whatsapp = scrapy.Field()
    contato_nome = scrapy.Field()
    atualizado_em = scrapy.Field()
    link = scrapy.Field(
        output_processor = Compose(TakeFirst(), fill_link)
    )
    garantias_aluguel = scrapy.Field()

