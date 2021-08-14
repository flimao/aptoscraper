#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import scrapy
from scrapy.loader import ItemLoader
from aptoscraper.items import ZAPItem

import logging
logger = logging.getLogger(__name__)

class ZAPSpider(scrapy.Spider):
    name = 'zap'
    allowed_domains = ['zapimoveis.com.br']

    headers = {
        "authority": "glue-api.zapimoveis.com.br",
        "sec-ch-ua": "^\^Opera^^;v=^\^77^^, ^\^Chromium^^;v=^\^91^^, ^\^",
        "x-domain": "www.zapimoveis.com.br",
        "accept": "application/json, text/plain, */*",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36 OPR/77.0.4054.277",
        "referer": 'https://www.zapimoveis.com.br/'
    }

    # This is a built-in Scrapy function that runs first where we'll override the default headers
    # Documentation: https://doc.scrapy.org/en/latest/topics/spiders.html#scrapy.spiders.Spider.start_requests
    def start_requests(self):
        url_locacoes = "https://glue-api.zapimoveis.com.br/v3/locations"

        # default nres = 200
        if getattr(self, 'nres', None) is None:
            self.nres = 200
        else:
            self.nres = int(self.nres)

        # default tipo = 'compra'
        self.tipo = getattr(self, 'negocio', 'compra')


        try:
            qstr_locacoes = self.qstr_locacoes(self.busca)
        except AttributeError:  # self.busca não existe porque esquecemos de passar parâmetros
            raise AttributeError('"self.busca" não está definido. Esqueceu de passar os termos de busca via parâmetros do scrapy (-a busca="<termos de busca>")?')

        # montagem de url
        # url = f'{url_locacoes}?'
        # for p, v in qstr_locacoes.items():
        #     url += f'p=v'

        # Set the headers here. The important part is "application/json"


        yield scrapy.http.FormRequest(url_locacoes, method = 'GET',
                     headers = self.__class__.headers, formdata = qstr_locacoes, callback = self.parse_locs)

    def parse_locs(self, response):
        
        self.loc_mais_provavel = self.loc_provavel(response.json())

        yield self.create_page_request(page = 1)

    def create_page_request(self, page = 1):
        
        url_listagens = "https://glue-api.zapimoveis.com.br/v2/listings"

        qstr_listagens = self.qstr_listagem(page = page)

        return scrapy.http.FormRequest(url_listagens, method = 'GET',
                headers = self.__class__.headers, formdata = qstr_listagens, callback = self.parse_listagens)

    def parse_listagens(self, response):     

        listagens = response.json()

        # endereço
        endereco_campos = {
            'zipCode': 'cep', 
            'country': 'pais', 
            'stateAcronym': 'estado', 
            'city': 'cidade', 
            'neighborhood': 'bairro', 
            'street': 'rua',
            'complement': 'complemento'
        } 

        # comodos
        comodos_conversao = {
            'quartos': 'bedrooms',
            'banheiros': 'bathrooms',
            'suites': 'suites'
        }

        pgdict = listagens['page']['uriPagination']
        numero_resultados = len(listagens['search']['result']['listings']) +\
                            len(listagens['superPremium']['search']['result']['listings'])
        pg = int(pgdict['page'])
        total = int(pgdict['total'])
        logger.info(f"Número de resultados (pg {pg}): {numero_resultados}/{total}")

        i = 1
        for destaque in (listagens['superPremium'], listagens):
            for res in destaque['search']['result']['listings']:
                l = ItemLoader(item = ZAPItem())
                
                l.add_value('id', res['listing']['externalId'])
                l.add_value('origem', res['listing']['portal'])
                l.add_value('impulsao', res['listing']['publicationType'])

                # area util
                l.add_value('area', res['listing']['usableAreas'])

                l.add_value('desc', res['listing']['description'])
                l.add_value('atualizado_em', res['listing']['updatedAt'])

                # endereco
                for c_en, c_pt in endereco_campos.items():
                    l.add_value(f'endereco_{c_pt}', res['listing']['address'].get(c_en, ''))
            
                l.add_value('amenidades', res['listing']['amenities'])

                # vagas de garagem
                l.add_value('nvagas', res['listing']['parkingSpaces'])
                
                # pontos de interesse
                l.add_value('pois', res['listing']['address'].get('poisList', []))

                # comodos
                for c_pt, c_en in comodos_conversao.items():
                    l.add_value(f'n{c_pt}', res['listing'][c_en])              
              
                # contatos
                l.add_value('contato_fones', res['listing']['advertiserContact']['phones'])
                l.add_value('contato_whatsapp', res['listing']['whatsappNumber'])
                l.add_value('contato_nome', res['account']['name'])
    

                # precos
                todosprecos = res['listing']['pricingInfos']
                
                # vamos procurar se uma das precificações corresponde ao tipo que queremos
                for precos in todosprecos:
                    if precos['businessType'] == self.conversaotipo(tipo = self.tipo):
                        break
                else:  # não encontramos. passa para o próximo
                    continue
                
            #     preco_fmt = {
            #         'porano': 0,
            #         'pormes': 0,
            #         'preco': None,
            #         'iptu': None
            #     }

            #     for k, v in precos.items():
                    
            #         try:
            #             if k == 'price':
            #                 preco_fmt['preco'] = float(v)
            #             elif 'iptu' in k.lower():
            #                 preco_fmt['iptu'] = float(v)
            #             elif k.startswith('yearly'):
            #                 preco_fmt['porano'] += float(v)
            #             elif k.startswith('monthly'):
            #                 preco_fmt['pormes'] += float(v)
            #         except ValueError:
            #             continue
                
            #     despesapormes = preco_fmt['pormes'] + preco_fmt['porano'] / 12
            #     if tipo.lower() in ('venda', 'compra'):
                    
            #         precostr = [ f"Preço: {fmt_moeda(preco_fmt['preco'])} + {fmt_moeda(despesapormes)} / mês" ]
            #         if preco_fmt['iptu'] is not None:
            #             precostr[0] += f" + {fmt_moeda(preco_fmt['iptu'])} IPTU"
                
            #     else:
            #         precostr = [ f"Preço: {fmt_moeda(despesapormes)} / mês" ]
            #         if preco_fmt['iptu'] is not None:
            #             precostr[0] += f" + {fmt_moeda(preco_fmt['iptu'])} IPTU"

            #         garantia = precos['rentalInfo']['warranties']
            #         precostr.append(f'    Garantias: {garantia}')
                
                l.add_value('link', res['link']['href'])

            #     print(f'{i: 4n}. {id = } ({origem = }, {impulsao = })')
            #     print(f'      Área: {areautil} m²')
            #     print(f'      Descrição: {desc[:50]}')
            #     print(f'      Cômodos: {comodos}')
            #     print(f'      Vagas de garagem: {vagas}')
            #     for linha in precostr:
            #         print(f'      {linha}')
            #     #print(f'      Preço: {precos}')
            #     print(f'      Amenidades: {amenidades}')
            #     print(f'      Endereço: {endereco}')
            #     print(f'      Pontos de Interesse: {pois}')
            #     print(f'      Contato: {contatos}')
            #     print(f'      Link: {link}')
            #     print('')

            #     i += 1
                yield l.load_item()
        
        if numero_resultados > 0:
            yield self.create_page_request(page = pg + 1)

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

    def loc_provavel(self, locacoes):
        
        matchscores = { kindres['maxScore']: kindkey for kindkey, kindres in locacoes.items() }

        maiorscore = max(matchscores.keys())
        tipo_mais_provavel = matchscores[maiorscore]

        loc_mais_provavel = locacoes[tipo_mais_provavel]['result']['locations'][0]
        loc_mais_provavel['tipo'] = tipo_mais_provavel

        #print(f'Locação mais provável: {loc_mais_provavel}')
        return loc_mais_provavel
    
    def qstr_listagem(self, page = 1):
        tipo_loc = self.loc_mais_provavel['tipo']
        tipo_pag = self.loc_mais_provavel['uriCategory']['page']
        estado = self.loc_mais_provavel['address']['state']
        cidade = self.loc_mais_provavel['address']['city']
        zona = self.loc_mais_provavel['address']['zone']
        bairro = self.loc_mais_provavel['address']['neighborhood']
        rua = self.loc_mais_provavel['address']['street']
        locationID = self.loc_mais_provavel['address']['locationId']
        lat = str(self.loc_mais_provavel['address']['point']['lat'])
        lon = str(self.loc_mais_provavel['address']['point']['lon'])

        fromval = self.nres * (int(page) - 1)

        querystring_listagem = {
            "business": 'SALE',
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
            "size": str(self.nres),
            "from": str(fromval), 
            "page": str(page),
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
            querystring_listagem.update( { 'business': self.conversaotipo(tipo = self.tipo, raiseError = True) })
        except AttributeError:
            pass

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

        return querystring_listagem

    def conversaotipo(self, tipo = 'compra', raiseError = False):
        conversaodict = {
            'venda': 'SALE',
            'compra': 'SALE',
            'aluguel': 'RENTAL'
        }

        if raiseError:
            return conversaodict[tipo.lower()].upper()
        else:
            return conversaodict.get(tipo.lower(), '').upper()
