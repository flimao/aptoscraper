#!/usr/bin/env python3 
# -*- coding: utf-8 -*-

#%% imports
import requests
import time
import json
import os

import locale
locale.setlocale(locale.LC_ALL, '') # this sets locale to the current Operating System value

#%% CONSTS

DIR = r'../../../'
JSON = r'rascunhos/zap.json'
fullpath = os.path.join(os.path.abspath(DIR), JSON)

#%% params

query = 'lagoa rio'
parametros_busca = {
    'precomin': 300000,
    'precomax': 1500000,
    'nquartos': 3,
    'nbanheiros': 2,
    'areamin': 100,
    'areamax': 200,
    'tipo': 'compra',  # valores possíveis: 'venda', 'compra', 'aluguel'
    'nres': 200
} 

#%% definições de funções

def fmt_moeda(valor, grouping = True, symbol = True, *args, **kwargs):
    return locale.currency(valor, grouping = grouping, symbol = symbol, *args, **kwargs)

def qstr_locacoes(query):

    querystring_locacoes = { 
        "businessType": "SALE",
        "fields": "neighborhood,city,street,account",
        "includeFields": "address.street,address.neighborhood,address.city,address.state,address.zone,address.locationId,address.point,url,advertiser.name,uriCategory.page", 
        "listingType": "USED", 
        "portal": "ZAP",
        "size": "6",
        "unitTypes": "UnitType_NONE",
        "q": query
        }
    
    return querystring_locacoes

def qstr_listagem(locacoes, nres = 200, *args, **kwargs):
    
    matchscores = { kindres['maxScore']: kindkey for kindkey, kindres in locacoes.items() }

    maiorscore = max(matchscores.keys())

    res_mais_provavel = locacoes[matchscores[maiorscore]]['result']['locations'][0]

    print(f'Locação mais provável: {res_mais_provavel}')

    tipo_loc = matchscores[maiorscore]
    tipo_pag = res_mais_provavel['uriCategory']['page']
    estado = res_mais_provavel['address']['state']
    cidade = res_mais_provavel['address']['city']
    zona = res_mais_provavel['address']['zone']
    bairro = res_mais_provavel['address']['neighborhood']
    rua = res_mais_provavel['address']['street']
    locationID = res_mais_provavel['address']['locationId']
    lat = str(res_mais_provavel['address']['point']['lat'])
    lon = str(res_mais_provavel['address']['point']['lon'])

    querystring_listagem = {
        "business": "SALE",
        "categoryPage": tipo_pag,
        "parentId": "null",
        "listingType": "USED",
        "addressCountry": "",
        "addressState": estado,
        "addressCity": cidade,
        "addressZone": zona,
        "addressNeighborhood": bairro,
        "addressStreet": rua,
        "addressAccounts": "",
        "addressType": tipo_loc,
        "addressLocationId": locationID,
        "addressPointLat": lat, "addressPointLon": lon,
        "size": str(nres),
        "from": "0", 
        "page": "1",
        "includeFields": "search(result(listings(listing(displayAddressType,amenities,usableAreas,"\
            "constructionStatus,listingType,description,title,stamps,createdAt,floors,unitTypes,"\
            "nonActivationReason,providerId,propertyType,unitSubTypes,unitsOnTheFloor,legacyId,id,portal,"\
            "unitFloor,parkingSpaces,updatedAt,address,suites,publicationType,externalId,bathrooms,"\
            "usageTypes,totalAreas,advertiserId,advertiserContact,whatsappNumber,bedrooms,acceptExchange,"\
            "pricingInfos,showPrice,resale,buildings,capacityLimit,status),account(id,name,logoUrl,"\
            "licenseNumber,showAddress,legacyVivarealId,legacyZapId,minisite),medias,accountLink,link)),"
            "totalCount),expansion(search(result(listings(listing(displayAddressType,amenities,usableAreas,"\
            "constructionStatus,listingType,description,title,stamps,createdAt,floors,unitTypes,"\
            "nonActivationReason,providerId,propertyType,unitSubTypes,unitsOnTheFloor,legacyId,id,portal,"\
            "unitFloor,parkingSpaces,updatedAt,address,suites,publicationType,externalId,bathrooms,usageTypes,"\
            "totalAreas,advertiserId,advertiserContact,whatsappNumber,bedrooms,acceptExchange,pricingInfos,"\
            "showPrice,resale,buildings,capacityLimit,status),account(id,name,logoUrl,licenseNumber,"\
            "showAddress,legacyVivarealId,legacyZapId,minisite),medias,accountLink,link)),totalCount)),"\
            "nearby(search(result(listings(listing(displayAddressType,amenities,usableAreas,constructionStatus,"\
            "listingType,description,title,stamps,createdAt,floors,unitTypes,nonActivationReason,providerId,"\
            "propertyType,unitSubTypes,unitsOnTheFloor,legacyId,id,portal,unitFloor,parkingSpaces,updatedAt,"\
            "address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,"\
            "advertiserContact,whatsappNumber,bedrooms,acceptExchange,pricingInfos,showPrice,resale,buildings,"\
            "capacityLimit,status),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,"\
            "legacyZapId,minisite),medias,accountLink,link)),totalCount)),page,fullUriFragments,"\
            "developments(search(result(listings(listing(displayAddressType,amenities,usableAreas,"\
            "constructionStatus,listingType,description,title,stamps,createdAt,floors,unitTypes,"\
            "nonActivationReason,providerId,propertyType,unitSubTypes,unitsOnTheFloor,legacyId,id,portal,"\
            "unitFloor,parkingSpaces,updatedAt,address,suites,publicationType,externalId,bathrooms,usageTypes,"\
            "totalAreas,advertiserId,advertiserContact,whatsappNumber,bedrooms,acceptExchange,pricingInfos,"\
            "showPrice,resale,buildings,capacityLimit,status),account(id,name,logoUrl,licenseNumber,"\
            "showAddress,legacyVivarealId,legacyZapId,minisite),medias,accountLink,link)),totalCount)),"\
            "superPremium(search(result(listings(listing(displayAddressType,amenities,usableAreas,"\
            "constructionStatus,listingType,description,title,stamps,createdAt,floors,unitTypes,"\
            "nonActivationReason,providerId,propertyType,unitSubTypes,unitsOnTheFloor,legacyId,id,portal,"\
            "unitFloor,parkingSpaces,updatedAt,address,suites,publicationType,externalId,bathrooms,usageTypes,"\
            "totalAreas,advertiserId,advertiserContact,whatsappNumber,bedrooms,acceptExchange,pricingInfos,"\
            "showPrice,resale,buildings,capacityLimit,status),account(id,name,logoUrl,licenseNumber,showAddress,"\
            "legacyVivarealId,legacyZapId,minisite),medias,accountLink,link)),totalCount)),"\
            "owners(search(result(listings(listing(displayAddressType,amenities,usableAreas,constructionStatus,"\
            "listingType,description,title,stamps,createdAt,floors,unitTypes,nonActivationReason,providerId,"\
            "propertyType,unitSubTypes,unitsOnTheFloor,legacyId,id,portal,unitFloor,parkingSpaces,"\
            "updatedAt,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,"\
            "advertiserId,advertiserContact,whatsappNumber,bedrooms,acceptExchange,pricingInfos,showPrice,"\
            "resale,buildings,capacityLimit,status),account(id,name,logoUrl,licenseNumber,showAddress,"\
            "legacyVivarealId,legacyZapId,minisite),medias,accountLink,link)),totalCount))",
        "cityWiseStreet": "1",
        "developmentsSize": "3",
        "superPremiumSize": "3"
    }

    try:
        querystring_listagem.update( { 'priceMin': str(kwargs['precomin']) })
    except KeyError:
        pass

    try:
        querystring_listagem.update( { 'priceMax': str(kwargs['precomax']) })
    except KeyError:
        pass

    try:
        querystring_listagem.update( { 'bathrooms': str(kwargs['nbanheiros']) })
    except KeyError:
        pass

    try:
        querystring_listagem.update( { 'bedrooms': str(kwargs['nquartos']) })
    except KeyError:
        pass

    try:
        querystring_listagem.update( { 'parkingSpaces': str(kwargs['nvagas']) })
    except KeyError:
        pass

    try:
        querystring_listagem.update( { 'usableAreasMin': str(kwargs['areamin']) })
    except KeyError:
        pass

    try:
        querystring_listagem.update( { 'usableAreasMax': str(kwargs['areamax']) })
    except KeyError:
        pass
    
    try:
        querystring_listagem.update( { 'business': conversaotipo(tipo, raiseKeyError = True) })
    except KeyError:
        pass


    return querystring_listagem

def conversaotipo(tipo, raiseKeyError = False):
    conversaodict = {
        'venda': 'SALE',
        'compra': 'SALE',
        'aluguel': 'RENTAL'
    }

    if raiseKeyError:
        return conversaodict[tipo.lower()].upper()
    else:
        return conversaodict.get(tipo.lower(), '').upper()

#%% HTTP request ou leitura de json + preproc
headers = {
    "authority": "glue-api.zapimoveis.com.br",
    "sec-ch-ua": "^\^Opera^^;v=^\^77^^, ^\^Chromium^^;v=^\^91^^, ^\^",
    "x-domain": "www.zapimoveis.com.br",
    "accept": "application/json, text/plain, */*",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36 OPR/77.0.4054.277"
}

url_locacoes = "https://glue-api.zapimoveis.com.br/v3/locations"

url_listagem = "https://glue-api.zapimoveis.com.br/v2/listings"

try:
    with open(fullpath, 'r', encoding = 'utf-8') as zapjson:
        listings = json.load(zapjson)

except FileNotFoundError:  # arquivo não existe. Vamos criar um
    with requests.Session() as sessao:

        pagina_inicial = sessao.get('https://www.zapimoveis.com.br/')

        querystring_locacoes = qstr_locacoes(query = query)

        resposta_locacoes = sessao.request("GET", url_locacoes, headers=headers, params=querystring_locacoes)

        querystring_listagens = qstr_listagem(resposta_locacoes.json(), **parametros_busca)

        resposta_listagens = sessao.request("GET", url_listagem, headers=headers, params=querystring_listagens)

        listagens = resposta_listagens.json()

    with open(fullpath, 'w', encoding = 'utf-8') as zapjson:
        writestr = json.dumps(listagens)
        zapjson.write(writestr)

# agora que já temos listagens...

endereco_campos = {
    'zipCode': 'cep', 
    'country': 'pais', 
    'stateAcronym': 'estado', 
    'city': 'cidade', 
    'neighborhood': 'bairro', 
    'street': 'rua',
    'complement': 'complemento'
}    
print(f"{len(listagens['search']['result']['listings']) = }")

i = 1
for res in listagens['search']['result']['listings'][:20]:
    id = res['listing']['externalId']
    origem = res['listing']['portal']
    impulsao = res['listing']['publicationType']

    areasuteis = res['listing']['usableAreas']
    # if len(areasuteis) == 1:
    #     continue
    areautil = areasuteis[0]

    desc = res['listing']['description']
    atualizadoe_em = res['listing']['updatedAt']
    endereco = { c_pt: res['listing']['address'].get(c_en, '') for c_en, c_pt in endereco_campos.items() }
    amenidades = res['listing']['amenities']
    
    try:
        vagas = res['listing']['parkingSpaces'][0]
    except IndexError:
        vagas = 0
    
    pois = res['listing']['address'].get('poisList', [])

    # comodos
    comodos_conversao = {
        'qts': 'bedrooms',
        'banheiros': 'bathrooms',
        'suites': 'suites'
    }
    comodos = {}
    
    for c_pt, c_en in comodos_conversao.items():
        comodos[c_pt] = 0
        try:
            comodos[c_pt] = res['listing'][c_en][0]
        except IndexError:
            pass

    
    # contatos
    contatos = res['listing'].get('advertiserContact', {})
    contatos['zapzap'] = res['listing'].get('whatsappNumber', '')
    contatos['nome'] = res['account'].get('name', '')

    # precos
    todosprecos = res['listing']['pricingInfos']
    
    # vamos procurar se uma das precificações corresponde ao tipo que queremos
    for precos in todosprecos:
        if precos['businessType'] == conversaotipo(tipo = tipo):
            break
    else:  # não encontramos. passa para o próximo
        continue

    # lenprecos = len(precos)
    # if lenprecos == 1:
    #     continue
    
    preco_fmt = {
        'porano': 0,
        'pormes': 0,
        'preco': None,
        'iptu': None
    }

    for k, v in precos.items():
        
        try:
            if k == 'price':
                preco_fmt['preco'] = float(v)
            elif 'iptu' in k.lower():
                preco_fmt['iptu'] = float(v)
            elif k.startswith('yearly'):
                preco_fmt['porano'] += float(v)
            elif k.startswith('monthly'):
                preco_fmt['pormes'] += float(v)
        except ValueError:
            continue
    
    despesapormes = preco_fmt['pormes'] + preco_fmt['porano'] / 12
    if tipo.lower() in ('venda', 'compra'):
        
        precostr = [ f"Preço: {fmt_moeda(preco_fmt['preco'])} + {fmt_moeda(despesapormes)} / mês" ]
        if preco_fmt['iptu'] is not None:
            precostr[0] += f" + {fmt_moeda(preco_fmt['iptu'])} IPTU"
    
    else:
        precostr = [ f"Preço: {fmt_moeda(despesapormes)} / mês" ]
        if preco_fmt['iptu'] is not None:
            precostr[0] += f" + {fmt_moeda(preco_fmt['iptu'])} IPTU"

        garantia = precos['rentalInfo']['warranties']
        precostr.append(f'    Garantias: {garantia}')
    
    link_rel = res['link']['href']
    
    linkfull = r"https://www.zapimoveis.com.br"
    if not link_rel.startswith(r'/'):
        linkfull += r'/'

    link = rf'{linkfull}{link_rel}'

    print(f'{i: 4n}. {id = } ({origem = }, {impulsao = })')
    print(f'      Área: {areautil} m²')
    print(f'      Descrição: {desc[:50]}')
    print(f'      Cômodos: {comodos}')
    print(f'      Vagas de garagem: {vagas}')
    for linha in precostr:
        print(f'      {linha}')
    #print(f'      Preço: {precos}')
    print(f'      Amenidades: {amenidades}')
    print(f'      Endereço: {endereco}')
    print(f'      Pontos de Interesse: {pois}')
    print(f'      Contato: {contatos}')
    print(f'      Link: {link}')
    print('')

    i += 1

# %%
