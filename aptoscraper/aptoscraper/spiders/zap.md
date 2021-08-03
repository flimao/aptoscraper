# Anotações para o scraper do ZAP Imóveis

### API REST /v3/locations

* URL: `"https://glue-api.zapimoveis.com.br/v3/locations"`
* Importante usar uma sessão do `requests`. Dessa forma, os cookies serão salvos.
* Headers: 
```python
headers = {
    "authority": "glue-api.zapimoveis.com.br",
    "sec-ch-ua": "^\^Opera^^;v=^\^77^^, ^\^Chromium^^;v=^\^91^^, ^\^",
    "x-domain": "www.zapimoveis.com.br",
    "accept": "application/json, text/plain, */*",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36 OPR/77.0.4054.277"
}
```
* Pedido via URL (GET):
```python
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
```

### API REST /v2/listings

* URL: `"https://glue-api.zapimoveis.com.br/v2/listings"`
* Importante usar uma sessão do `requests`. Dessa forma, os cookies serão salvos.
* Headers: 
```python
headers = {
    "authority": "glue-api.zapimoveis.com.br",
    "sec-ch-ua": "^\^Opera^^;v=^\^77^^, ^\^Chromium^^;v=^\^91^^, ^\^",
    "x-domain": "www.zapimoveis.com.br",
    "accept": "application/json, text/plain, */*",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36 OPR/77.0.4054.277"
}
```
* Pedido via URL (GET):
```python
querystring_listagem = {
    "business": "SALE",
    "categoryPage": 'RESULT',
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
    "addressPointLat": str(lat), "addressPointLon": str(lon),
    "size": str(nres_por_pagina),
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
```

## Código resumido
```python
url_locacoes = "https://glue-api.zapimoveis.com.br/v3/locations"
url_listagem = "https://glue-api.zapimoveis.com.br/v2/listings"

with requests.Session() as sessao:  

    # para o servidor setar os cookies iniciais
    pagina_inicial = sessao.get('https://www.zapimoveis.com.br/')

    # querystring para catar as locações, acima
    querystring_locacoes = qstr_locacoes(query = 'Lagoa rio')
    resposta_locacoes = sessao.request("GET", url_locacoes, headers=headers, params=querystring_locacoes)

    # querystring para, dada a locação mais provável, obter os resultados
    querystring_listagens = qstr_listagem(resposta_locacoes.json(), nres = 3, preco_ate = 900000)
    resposta_listagens = sessao.request("GET", url_listagem, headers=headers, params=querystring_listagens)

    listagens = resposta_listagens.json()

    # profit!

```