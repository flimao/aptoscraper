#!/usr/bin/env python3 
# -*- coding: utf-8 -*-

#%% imports
import requests
import time

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

    print(res_mais_provavel)

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

    return querystring_listagem

headers = {
    "authority": "glue-api.zapimoveis.com.br",
    "sec-ch-ua": "^\^Opera^^;v=^\^77^^, ^\^Chromium^^;v=^\^91^^, ^\^",
    "x-domain": "www.zapimoveis.com.br",
    "accept": "application/json, text/plain, */*",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36 OPR/77.0.4054.277"
}

query = 'niterói mariz e barros'
preco_ate = 1500000

url_locacoes = "https://glue-api.zapimoveis.com.br/v3/locations"

url_listagem = "https://glue-api.zapimoveis.com.br/v2/listings"

with requests.Session() as sessao:

    pagina_inicial = sessao.get('https://www.zapimoveis.com.br/')

    querystring_locacoes = qstr_locacoes(query = query)

    resposta_locacoes = sessao.request("GET", url_locacoes, headers=headers, params=querystring_locacoes)

    querystring_listagens = qstr_listagem(resposta_locacoes.json(), nres = 3, preco_ate = preco_ate)

    resposta_listagens = sessao.request("GET", url_listagem, headers=headers, params=querystring_listagens)

    listagens = resposta_listagens.json()

    #print(querystring_listagens)
    #print(listagens)
  
# %%
