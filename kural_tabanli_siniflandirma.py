#####################################################################################################
#Kural Tabanlı Sınıflandırma
#####################################################################################################
#1.Veri Setinin Yüklenmesi
#2.Veri Setine Genel Bakış
#3.Veri Manipülasyonu
#4.Persona Oluşturulması
#5.Sonuç


#Bu çalışmanın Kaggle linki:
# https://www.kaggle.com/tugrulyilmaz/kural-tabanli-siniflandirma


#######################################################################################################
#1.Veri Setinin Yüklenmesi
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
#pd.set_option("display.max_rows",None)
pd.set_option("display.expand_frame_repr",False)
import warnings
warnings.filterwarnings("ignore")

df=pd.read_csv("/kaggle/input/insurance/insurance.csv")


#######################################################################################################
#2.Veri Setine Genel Bakış
from gerekli_fonksiyonlar import *

cat_cols,num_cols=control_df(df)

for col in cat_cols:
    cat_analysis(df,col)


#######################################################################################################
#3. Veri Manipülasyonu

# "age" değişkeni belirtilen yaş aralıklarına göre sınıflandırılıyor.
df["age_cat"]=pd.cut(df["age"],[0,22,30,45,70],labels=["0_22","22_30","30_45","45_70"])

#yeni df için ortalama ücretlerin grafik üzerinde gösterilmesi
gg(df,"charges")

#Persona sınıflandırmamızı "smoker","region","children","age_cat" değişkenlerine göre oluşturacağız.
#Bu yüzden bu değişkenlere göre kırılımların ücret ortalamalarını incelemekte fayda var.4

agg_df=df.groupby(["smoker","region","children","age_cat"]).agg({"charges":"mean"}).sort_values("charges",ascending=False)
print(agg_df)

#Burada görülüyor ki oluşturduğumuz senaryoda bazı değerler için elimizde hiç örnek yok.
# Bu örnekler için değer ataması yapmamız gerekiyor.

agg_df=agg_df.reset_index()
print(agg_df.shape)

# Eksik veriler için ayrı bir dataframe oluşturuldu.
missing_values=agg_df[agg_df["charges"].isnull()]
print(missing_values.tail(10))

compare_draw(df,"region","charges")
al=missing_fill(agg_df)
# Eksik değerleri doldurmak için şöyle bir yöntem seçtim.
# Bölgelere ait ücret ortalaması grafiğini hatırlarsak
# "northwest" ile "southwest" bölgesi ve "northeast" ile "southeast" bölgesi birbirine
# benzer davranışlar sergiliyor.Bu yüzden eksik verileri doldurmak için bu bölgelerin
# birbirinde karşılık gelen koşullarından fayda sağladım.

# Eksik değerler için tahminlerimiz bir değişkene atandı.
al=missing_fill(agg_df)

# Üzerinde çalıştığımız df içindeki eksik değerler yerine atandı.
agg_df.loc[al.index.values]=al

control_df(agg_df)


#######################################################################################################
#4.Persona Oluşturulması
#Bu kısımda verilerimiz persona dataframe şekline çeviriliecektir.

zz=[]
for i in range(len(agg_df)):
    tl=agg_df["region"][i] + "_" + str(agg_df["children"][i]) + "_" + agg_df["smoker"][i] + "_" + agg_df["age_cat"][i]
    zz.append(tl.upper())

persona_df=pd.concat([pd.DataFrame(zz),agg_df["charges"]],axis=1)
persona_df.columns=["level_based","charges"]

persona_df=persona_df.groupby("level_based").agg({"charges":"mean"}).sort_values("charges",ascending=False)
persona_df=persona_df.reset_index()
persona_df.shape

persona_df["SEGMENT"]=pd.qcut(persona_df["charges"],6,["F","E","D","C","B","A"])
persona_df=persona_df.reset_index()

#Oluşturduğumuz persona dataframe'ine göz atalım.
print(persona_df.head())

#######################################################################################################
#Sonuç

user("southwest",5,"no",60)
