import tkinter as tk
import requests
import json
import pandas as pd

def get_token():
    url = "https://gateway.richrelevance.com/streaming-ingest/v1/oauth2/token?grant_type=client_credentials&client_id=d987346d6347894b&client_secret=uqlsl9q6emti9ketdaid98rkdm"
    payload={}
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload)
    token=json.loads(response.text).get('access_token')
    print('========= Conectando con Algonomy =========')
    return token

def delete_products():
    token=get_token()
    headers = {'Authorization': 'Bearer '+token}
    payload={}
    
    df = pd.read_excel ('..\products_rr.xlsm',sheet_name='delete')
    m = df['SAP'].values.tolist()
    print(df)
    for i in m:
        url = f"https://gateway.richrelevance.com/streaming-ingest/v1/e1b75ced78fdfe64/product/{i}?snapshotId=1001".format(i)
        response = requests.request("DELETE", url, headers=headers, data=payload)
        print(response.text)

ventana=tk.Tk()
ventana.title("Eliminación de Productos")
ventana.geometry('400x200')
etiqueta1=tk.Label(ventana,text="Confirmar eliminación de productos")
etiqueta1.pack(fill=tk.X)

boton=tk.Button(ventana,text="Confirmar",command=delete_products)
boton.place(x=150, y=50, width=100, height=30)
ventana.mainloop()

