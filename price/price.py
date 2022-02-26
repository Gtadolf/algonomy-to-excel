import pandas as pd
import json
from io import BytesIO
import gzip
import requests
import urllib3
import tkinter as tk

url_auth = 'https://gateway.richrelevance.com/streaming-{streaming_type}/v1/oauth2/token'
grant_type = 'client_credentials'
client_id = 'd987346d6347894b'
client_secret = 'uqlsl9q6emti9ketdaid98rkdm'   
payload_product = '{"{code_product}":{"overrides": {"region": { "{campania}":{"properties": {"product_saleprice_b": {precio}, "sale_price": {precio}}}} }}}'
url_ingest_products = 'https://gateway.richrelevance.com/streaming-ingest/v1/e1b75ced78fdfe64/product?snapshotId=1001&force=true'
access_token_ingest=''
access_token_view=''

def execution():
    global access_token_ingest, access_token_view
    print('========= Conectando con Algonomy =========')
    access_token_ingest = get_auth('ingest')['access_token']
    access_token_view = get_auth('view')['access_token']
    df_products = pd.read_excel('..\products_rr.xlsm', sheet_name='Price')
    print(df_products)
    cambio_precio(df_products)

def get_auth(streaming_type):
    urllib3.disable_warnings()
    data = {'grant_type': grant_type,
            'client_id': client_id, 'client_secret': client_secret}
    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    url_auth_streaming = url_auth.replace('{streaming_type}', streaming_type)
    resp = requests.post(url_auth_streaming, params=data, headers=header, verify=False)
    return json.loads(resp.text)

def zip_payload(payload):
    btsio = BytesIO()
    g = gzip.GzipFile(fileobj=btsio, mode='w')
    g.write(bytes(payload, 'utf8'))
    g.close()
    return btsio.getvalue()

def path_ingest_product(payload, product_code):
    header = {
        'Authorization': 'Bearer ' + access_token_ingest,
        'Content-Type': 'application/json; charset=utf-8',
        'Content-Encoding': 'gzip'
    }
    payload = zip_payload(payload)

    try:

        resp = requests.patch(url_ingest_products, data=payload, headers=header, verify=False)
        response_json = json.loads(resp.text)
    except Exception as error:
        print('Error:', error)
        print('response json:', product_code, ": ", resp.text)
        response_json = {"statusTracker": {"trackingInstant": "2020-10-09T22:32:58.364014700Z",
                                           "trackingId": "66666666-0a7f-11eb-b4ff-ffffff", "message": resp.text}}

    return response_json

def cambio_precio(df_products):
    for i in range(len(df_products)):
        payload = payload_product.replace('{code_product}', str(df_products['sku'][i])).replace('{campania}', df_products['campania'][i]).replace('{precio}', str(df_products['precio'][i]))
        print('Product: ', 'sku: ' + str(df_products['sku'][i]) + ', campaign: ' + df_products['campania'][i] +  ', sale_price: '+ str(df_products['precio'][i]))
        path_ingest_product(payload, df_products['sku'][i])

ventana=tk.Tk()
ventana.title("Cambio de Precio")
ventana.geometry('400x200')
etiqueta1=tk.Label(ventana,text="Confirmar cambio de precio")
etiqueta1.pack(fill=tk.X)

boton=tk.Button(ventana,text="Confirmar",command=execution)
boton.place(x=150, y=50, width=100, height=30)
ventana.mainloop()
