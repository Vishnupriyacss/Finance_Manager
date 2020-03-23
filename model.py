#!/usr/bin/env python
# coding: utf-8

# In[52]:


from Data_Preposing import *
# import pandas as pd
# import numpy as np
import mysql.connector
from urlextract import URLExtract
import tldextract
mydb = mysql.connector.connect(
       user='root', 
       password='', 
       host='localhost',
       database='finance_manager')


def db_update(vendor):
    vendor_name=vendor

    mycursor_two = mydb.cursor()
    q1=("INSERT into tbl_finance_vendor (id, vendor_name) VALUES ('',%s)")
    v1 =(vendor_name)
    mycursor_two.execute(q1,v1)
    mydb.commit()


mycursor_one = mydb.cursor()
mycursor_one.execute("SELECT description from tbl_finance_statement_line_item LIMIT 5 ")
result=mycursor_one.fetchall()






# m=["MAKEMYTRIP INDIA PVT LTNEW DELHI","PAYTM www.paytm.co","Oravel Stays Priva INR www.oyorooms","Primrose Service Apart Bangalore HQ","Super_PayU MUMBA","LINKEDIN-252*5528243 LINKEDIN.COM"]
# print(len(m))
for k in result:

    i=k[0].lower()
    
    extractor = URLExtract()
    urls = extractor.find_urls(i)
    s=(len(urls))
    if(s==0):
        a=(Data_Preposing(k[0]))
        a.rename(columns={0: 'Words'}, inplace=True)
        model1 = load_model('my_model.h5')
        Y_pred=model1.predict(a)
        y_pred =[]
        for i in Y_pred:
            y_pred.append(np.argmax(i))

        # # print(y_pred)
        z=pd.DataFrame(y_pred)
        z.rename(columns={0: 'Target'},inplace=True)
        z['Target'].replace([0], 'company_name',inplace=True)
        z['Target'].replace([1], 'others',inplace=True)
        z['index']=z.index
        # print(z)
        result = [y.strip() for y in k[0].split(' ')]
        data=pd.DataFrame(result)
        # print(data)
        data["index"]=data.index
        data.rename(columns={0: 'Words'}, inplace=True)
        v=pd.merge(data,z,on="index")
        v.drop(['index'],axis=1,inplace=True)
        l=v[(v.Target == "company_name")]
        comp=l['Words'].values.tolist()
        str1 = ' '.join(comp)
        db_update(str1)
    else:
        url =(', '.join(urls))
        ext = tldextract.extract(url)
        db_update(ext.domain)


# # In[ ]:




