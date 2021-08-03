#!/usr/bin/env python3 
# -*- coding: utf-8 -*-

#%% imports
import requests
import time
import json
import os

#%% CONSTS

DIR = r'../../../'
JSON = r'rascunhos/zap.json'
fullpath = os.path.join(os.path.abspath(DIR), JSON)

#%% HTTP request: url

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
        querystring_listagem.update( { 'priceMax': str(kwargs['preco_ate']) })
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
        'aluguel': 'RENTAL'
    }

    if raiseKeyError:
        return conversaodict[tipo.lower()].upper()
    else:
        return conversaodict.get(tipo.lower(), '').upper()

headers = {
    "authority": "glue-api.zapimoveis.com.br",
    "sec-ch-ua": "^\^Opera^^;v=^\^77^^, ^\^Chromium^^;v=^\^91^^, ^\^",
    "x-domain": "www.zapimoveis.com.br",
    "accept": "application/json, text/plain, */*",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36 OPR/77.0.4054.277"
}

### ----
### params
### ----

query = 'lagoa rio'
preco_ate = 1500000
tipo = 'venda'

### fim params

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

        querystring_listagens = qstr_listagem(resposta_locacoes.json(), 
                                                nres = 300, preco_ate = preco_ate,
                                                tipo = tipo)

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
for res in listagens['search']['result']['listings']:
    id = res['listing']['externalId']



    areasuteis = res['listing']['usableAreas']
    # if len(areasuteis) == 1:
    #     continue
    areautil = areasuteis[0]

    desc = res['listing']['description']
    atualizadoe_em = res['listing']['updatedAt']
    endereco = { c_pt: res['listing']['address'].get(c_en, '') for c_en, c_pt in endereco_campos.items() }
    amenidades = res['listing']['amenities']


    if len(res['listing']['bedrooms']) == 1:
        continue
    
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
    
    porano = 0
    pormes = 0
    for k, v in precos.items():
        
        try:
            if k == 'price':
                preco = float(v)
            elif k.startswith('yearly'):
                porano += float(v)
            elif k.startswith('monthly'):
                pormes += float(v)
        except ValueError:
            continue
        
    despesapormes = pormes + porano / 12
    
    link_rel = res['link']['href']
    
    linkfull = r"https://www.zapimoveis.com.br"
    if not link_rel.startswith(r'/'):
        linkfull += r'/'

    link = rf'{linkfull}{link_rel}'

    print(f'{i: 4n}. {id = }')
    print(f'      Área: {areautil} m²')
    print(f'      Descrição: {desc[:50]}')
    print(f'      Cômodos: {comodos}')
    print(f'      Preço: R$ {preco:.2f} + R$ {despesapormes:.2f} / mês')
    print(f'      Preço: {precos}')
    print(f'      Amenidades: {amenidades}')
    print(f'      Endereço: {endereco}')
    print(f'      Link: {link}')
    print('')

    i += 1
# %%
for a in [1,2,3]:
    if a == 1:
        continue
    print(a)
# %%
