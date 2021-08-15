# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders import ItemLoader
from itemloaders.processors import MapCompose, Compose, TakeFirst, Join
import re

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
    onibus = scrapy.Field()
    metro_trem = scrapy.Field()
    cafes = scrapy.Field()
    farmacias = scrapy.Field()
    pois = scrapy.Field()
    contato_fones = scrapy.Field()
    contato_whatsapp = scrapy.Field()
    contato_nome = scrapy.Field()
    atualizado_em = scrapy.Field()
    link = scrapy.Field(
        output_processor = Compose(TakeFirst(), fill_link)
    )
    garantias_aluguel = scrapy.Field()

def dictify(chavevalor_str_lst):
    
    try:
        chave, valor = re.search(r'(\w\w):(.+)', chavevalor_str_lst).groups()
    except:
        raise

    return { chave: valor }

def concat_str_dict(dict_lst):
    retdict = dict()
    for d in dict_lst:
        for k, v in d.items():
            l = retdict.get(k, [])
            l.append(v)
            retdict[k] = l

    return retdict

def processa_chaves(poidictfull):
    tipos_conhecidos = {
        'BS': 'onibus',
        'TS': 'metro_trem',
        'CS': 'cafes',
        'PH': 'farmacias'
    }

    retdict = { 'pois': [] }

    for k, v in poidictfull.items():
        if k in tipos_conhecidos:
            retdict[tipos_conhecidos[k]] = poidictfull[k]
        
        else:
            for poi in v:
                retdict['pois'].append(f'{k}:{poi}')

    return retdict

class POILoader(ItemLoader):
    default_output_processor = Join(',')

    pois_out = Compose(MapCompose(dictify), concat_str_dict, processa_chaves)