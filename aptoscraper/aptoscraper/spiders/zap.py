import scrapy
import logging

logger = logging.getLogger(__name__)

class ZapSpider(scrapy.Spider):
    name = 'zap'
    allowed_domains = ['zapimoveis.com.br']

    headers = {
        "authority": "glue-api.zapimoveis.com.br",
        "sec-ch-ua": "^\^Opera^^;v=^\^77^^, ^\^Chromium^^;v=^\^91^^, ^\^",
        "x-domain": "www.zapimoveis.com.br",
        "accept": "application/json, text/plain, */*",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36 OPR/77.0.4054.277"
    }

    # This is a built-in Scrapy function that runs first where we'll override the default headers
    # Documentation: https://doc.scrapy.org/en/latest/topics/spiders.html#scrapy.spiders.Spider.start_requests
    def start_requests(self):
        url_locacoes = "https://glue-api.zapimoveis.com.br/v3/locations"

        qstr_locacoes = self.qstr_locacoes(self.busca)

        # montagem de url
        # url = f'{url_locacoes}?'
        # for p, v in qstr_locacoes.items():
        #     url += f'p=v'

        # Set the headers here. The important part is "application/json"


        yield scrapy.http.FormRequest(url_locacoes, method = 'GET',
                     headers = self.__class__.headers, formdata = qstr_locacoes, callback = self.parse_locs)

    def parse_locs(self, response):

        url_listagens = "https://glue-api.zapimoveis.com.br/v2/listings"

        qstr_listagens = self.qstr_listagem(response.json())

        yield scrapy.http.FormRequest(url_listagens, method = 'GET',
                headers = self.__class__.headers, formdata = qstr_listagens, callback = self.parse_listagens)

    def parse_listagens(self, response):
        

    def qstr_locacoes(self, query):

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

    def qstr_listagem(self, locacoes, nres = 200):
        
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
            querystring_listagem.update( { 'priceMin': str(self.precomin) })
        except AttributeError:
            pass

        try:
            querystring_listagem.update( { 'priceMax': str(self.precomax) })
        except AttributeError:
            pass

        try:
            querystring_listagem.update( { 'bathrooms': str(self.nbanheiros) })
        except AttributeError:
            pass

        try:
            querystring_listagem.update( { 'bedrooms': str(self.nquartos) })
        except AttributeError:
            pass

        try:
            querystring_listagem.update( { 'parkingSpaces': str(self.nvagas) })
        except AttributeError:
            pass

        try:
            querystring_listagem.update( { 'usableAreasMin': str(self.areamin) })
        except AttributeError:
            pass

        try:
            querystring_listagem.update( { 'usableAreasMax': str(self.areamax) })
        except AttributeError:
            pass
        
        try:
            tipo = getattr(self, 'tipo', None) 
            if tipo is not None:
                querystring_listagem.update( { 'business': self.conversaotipo(tipo, raiseError = True) })
            else:
                querystring_listagem.update( { 'business': self.conversaotipo(raiseError = True) })
        except AttributeError:
            pass


        return querystring_listagem

    def conversaotipo(tipo = 'compra', raiseError = False):
        conversaodict = {
            'venda': 'SALE',
            'compra': 'SALE',
            'aluguel': 'RENTAL'
        }

        if raiseError:
            return conversaodict[tipo.lower()].upper()
        else:
            return conversaodict.get(tipo.lower(), '').upper()
