#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#%% imports
import os
import sys
import argparse
import numpy as np
import pandas as pd
from pandas.core.common import flatten  # para extrair entradas unicas de 'amenidadess'
import glob
import geopy
from geopy.extra.rate_limiter import RateLimiter

#%% 
BDDIR_DEFAULT = r'../bd'
MASCARA_PARCIAL_DEFAULT = r'zap_*.csv'
DEBUG = True

def parse_all_args():  # argparse
    parser = argparse.ArgumentParser(
        description = 'Análise de BD do scraper de ofertas de imóveis.',
    )

    parser.add_argument('--dir', dest='bddir', action='store', default = BDDIR_DEFAULT,
                        help='diretório no qual se encontram as bases raspadas dos sites de anúncios de imóveis')

    parser.add_argument('--bd', dest='mascara_parcial', action='store', default = MASCARA_PARCIAL_DEFAULT,
                        help='máscara dos arquivos csv que contém os dados raspados dos sites de anúncios de imóveis')
    
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')

    args = parser.parse_args()

    args = args.bddir, args.mascara_parcial

    return args

def carregar_dataframe_inicial(bddir, mascara_parcial):
    # telefones são strings!
    cols_tels = ['contato_fones', 'contato_whatsapp']
    dtypes = { tel: str for tel in cols_tels }
    dates_cols = ['atualizado_em']

    # carregar todos os CSV na pasta relevante que começam por 'zap_'

    mascara = os.path.join(os.path.abspath(bddir), mascara_parcial)

    bd_csvs = glob.glob(mascara)
    bd_lstdfs = [ pd.read_csv(bd_csv, dtype = dtypes, parse_dates = dates_cols) for bd_csv in bd_csvs ]

    portaldf_raw = pd.concat(bd_lstdfs, axis = 0)

    return portaldf_raw

# funções do pipeline de limpeza

# 1. determinando indice
def setar_indice(df, indice = ['origem', 'id']):
    df = df.copy()
    df.set_index(keys = indice, drop = True, inplace = True)
    return df

# 2. eliminar duplicatas
def eliminar_duplicatas(df, subset = ['atualizado_em']):
    index_cols = list(df.index.names)
    subset_real = index_cols + subset
    df = df.copy()

    # não conseguimos dropar duplicatas baseados no índice
    df2 = df.reset_index().drop_duplicates(subset = subset_real)

    # retornamos ao indice original
    df3 = df2.set_index(index_cols, drop = True)

    return df3

# 3. adicionar data de atualização ao índice (de forma a garantir que seja único)
def add_indice(df, cols = ['atualizado_em']):
    df = df.copy()

    df2 = df.set_index(cols, append = True, drop = True)

    return df2

# 4. fillna
def preencher_vazios(df, cols_fillna = ['nsuites', 'nvagas'], astype = np.int8):
    df = df.copy()
    df[cols_fillna] = df[cols_fillna].fillna(0)
    df[cols_fillna] = df[cols_fillna].astype(astype)
    return df

# 5. preencher lat e long faltantes
def preencher_latlong(df):
    df = df.copy()

    # funcoes para construcao de queries

    def construir_dict_rua(df_ends):
        query_dict = df_ends.apply(lambda linha: {
            'street': linha['endereco_rua'],
            'city': linha['endereco_cidade'],
            'state': linha['endereco_estado'],
            'country': linha['endereco_pais']
        }, axis = 1)
        return query_dict

    def construir_dict_cep(df_ends):
        query_dict = df_ends.apply(lambda linha: {
            'postalcode': linha['endereco_cep'],
            'country': linha['endereco_pais']
        }, axis = 1)

        return query_dict
    
    # filtrando o df para só incluir entradas com latitude e longitude nulas
    df_ends_full = df[[c for c in df if c.startswith('endereco')]].copy()
    df_ends_dbl = df_ends_full.loc[df_ends_full.endereco_latitude.isna()]

    # preencher as entradas faltantes com base no CEP:
    df_ends_dbl2 = df_ends_dbl.groupby('endereco_cep').transform('first')
    df_ends_dbl2['endereco_cep'] = df_ends_dbl['endereco_cep']

    # deduplicar com a coluna CEP. depois preencheremos as duplicatas
    # o objetivo é minimizar as chamadas de API
    df_ends = df_ends_dbl2.drop_duplicates(
        subset = ['endereco_pais', 'endereco_estado', 'endereco_cidade', 'endereco_rua'],
    )

    # construir a query com base nos enderecos
    # caso não exista alguma informação, construir a query com base no cep

    queries = construir_dict_rua(df_ends).where(   # endereco completo...
                    df_ends.endereco_rua.notna(),  # ...onde a rua estiver preenchida...
                    construir_dict_cep(df_ends))   # .. caso contrario CEP

    # construir a função geocode
    geocoder = geopy.Nominatim(user_agent = 'imoveis-bot', timeout = 5)
    geocode_rl = RateLimiter(geocoder.geocode, min_delay_seconds = 1)

    # Series com locator com longitude e latitude
    if not DEBUG:
        locators = queries.apply(geocode_rl)
    else:
        locators = pd.Series(None, index = queries.index, dtype = 'float64')

    # extrair latitude e longitude

    def apply_locator_item(locator):
        if np.isnan(locator):
            return {'endereco_latitude': np.nan, 'endereco_longitude': np.nan}
        else:
            return {
                'endereco_latitude': locator.latitude,
                'endereco_longitude': locator.longitude
            }

    latlong = (locators
        .apply(apply_locator_item)
        .apply(pd.Series)  # para transformar em um DataFrame
    )

    # juntar as lats e longs obtidas no df principal
    # após essa operação, vai faltar repetir essas lats e longs para as entradas
    # repetidas que removemos
    latlong_full_na = df_ends_dbl2[latlong.columns].where(df_ends_dbl2[latlong.columns].notna(), latlong)
    df_ends_dbl2[latlong.columns] = latlong_full_na

    # repetindo para entradas repetidas que tiramos anteriormente
    df_ends_final = df_ends_dbl2.copy()
    df_ends_final[latlong.columns] = df_ends_dbl2.groupby('endereco_cep')[latlong.columns].transform('first')

    # integrando o df com enderecos ao df principal
    latlong_final = df[latlong.columns].where(df[latlong.columns].notna(), df_ends_final[latlong.columns])
    df[latlong.columns] = latlong_final

    return df

# (CORTADO DO PIPE) dropar coluna de amenidades do df principal
def dropar_cols(df, cols):
    df = df.copy()
    df = df.drop(columns = cols)
    return df

# n-2. eliminar colunas
def escolher_colunas(df, 
            cols_manter = [
                'endereco_bairro', 'endereco_rua', 'endereco_complemento',
                'endereco_latitude', 'endereco_longitude',
                'area', 'desc',
                'nquartos', 'nbanheiros', 'nsuites', 'nvagas',
                'metro_trem', 'onibus', 'cafes',
                'preco', 'iptu', 'despesa_mes', 'despesa_ano',
                'link'
            ]
        ):
    df = df.copy()

    df = df.drop(columns = set(df.columns) - set(cols_manter))

    return df

# n-1. associar amenidades
def associar_amenidades(df, df_amenidades, 
                        amenidades_cols = ['PLAYGROUND', 'BALCONY', 'CLOSET']):
    df = df.copy()

    df = df.join(df_amenidades[amenidades_cols], how = 'left')

    return df

# n. ordenar linhas
def sort_linhas(df, key = ['area', 'nsuites', 'nquartos', 'preco', 'iptu']):
    df = df.copy()

    df = df.sort_values(key, ascending = False)

    return df

# extra: one-hot encoding de colunas com csv
def extrair_ohe_csv(df, col, sep = ','):
    df = df.copy()

    try:
        col_gen = flatten(df[col].str.split(sep))
    except AttributeError: # coluna não tem nenhuma string. Vamos retornar um DF vazio
        return pd.DataFrame([], index = df.index)

    col_set_nan = set(col_gen)
    col_set = { col.strip() for col in col_set_nan if col == col }  # checando por nans em strings.

    coldf = pd.DataFrame({
        colitem: (df[col]
                    .str.contains(colitem)
                    .where(df[col].notna(), False)
                ) for colitem in col_set})
    
    return coldf

def pipeline(portaldf_raw):

    # primeiro, acertamos o indice do dataframe principal
    portaldf_indice = (portaldf_raw
        .pipe(setar_indice)
        .pipe(eliminar_duplicatas)
        .pipe(add_indice, cols = ['atualizado_em'])
    )

    # processamento de pontos de interesse

    onibus = extrair_ohe_csv(portaldf_indice, col = 'onibus')
    metro_trem = extrair_ohe_csv(portaldf_indice, col = 'metro_trem')
    farmacias = extrair_ohe_csv(portaldf_indice, col = 'farmacias')
    pois = extrair_ohe_csv(portaldf_indice, col = 'pois')

    # processamento de amenidades
    amenidades = extrair_ohe_csv(portaldf_indice, col = 'amenidades')

    extras = (onibus, metro_trem, farmacias, pois, amenidades)

    # prosseguimento do pipeline de limpeza
    portaldf_timeseries = (portaldf_indice
        .pipe(preencher_vazios)
        .pipe(preencher_latlong)
        .pipe(escolher_colunas)
        .pipe(associar_amenidades, df_amenidades = amenidades)
        .pipe(sort_linhas)
    )

    # dois csvs: serie temporal (evolução nos precos das ofertas) e ultima listagem de cada imovel
    atualizacao_mais_recente = (portaldf_timeseries
        .reset_index()
        .groupby(['origem', 'id'])['atualizado_em']
        .transform(lambda dt_atualizacao: dt_atualizacao == dt_atualizacao.max())
    ) 
    atualizacao_mais_recente.index = portaldf_timeseries.index

    portaldf = portaldf_timeseries[atualizacao_mais_recente].copy()

    return portaldf, portaldf_timeseries, extras

def salvar_csv(portaldf, portaldf_timeseries, bddir):
    # determinar nomes de arquivo
    csv_salvar_fn_timeseries = os.path.join(os.path.abspath(bddir), r'processado', r'imoveis_timeseries.csv')
    csv_salvar_fn_listagens = os.path.join(os.path.abspath(bddir), r'processado', r'imoveis.csv')

    # escrever os csv
    portaldf_timeseries.to_csv(csv_salvar_fn_timeseries)
    portaldf.to_csv(csv_salvar_fn_listagens)

#%% go!
def main(bddir, mascara_parcial):
    portaldf_raw = carregar_dataframe_inicial(bddir = bddir, mascara_parcial = mascara_parcial)
    portaldf, portaldf_timeseries, extras = pipeline(portaldf_raw = portaldf_raw)

    onibus, metro_trem, farmacias, pois, amenidades = extras

    salvar_csv(portaldf, portaldf_timeseries, bddir = bddir)

    return portaldf, portaldf_timeseries, onibus, metro_trem, farmacias, pois, amenidades

if __name__ == '__main__':
    
    if sys.argv[0] == 'analise.py':  # rodar via script cli
        bddir, mascara_parcial = parse_all_args()
    else:  # rodar via jupyter/notebook
        bddir = BDDIR_DEFAULT
        mascara_parcial = MASCARA_PARCIAL_DEFAULT

    # go!
    allvars = main(bddir = bddir, mascara_parcial = mascara_parcial)
    portaldf, portaldf_timeseries, onibus, metro_trem, farmacias, pois, amenidades = allvars
