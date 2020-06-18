import requests
import pandas
from bs4 import BeautifulSoup

r=requests.get("https://www.magicbricks.com/property-for-rent/residential-real-estate?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Service-Apartment,Residential-House,Villa&Locality=Pari-Chowk,Alpha-1,Alpha-2,Beta-1,Beta-2,Gamma-1,Gamma-2,Chi,Phi,Delta-1,Delta-2,Delta-3,Swarnnagari,Omega&cityName=Greater-Noida")
c=r.content

soup=BeautifulSoup(c,"html.parser")
# print(soup.prettify())

all=soup.find_all("div",{"class":"flex relative clearfix m-srp-card__container"})

l=[]

for i in range(len(all)):
    
    d={}
    
    priceL=list(all[i].find("div",{"class":"m-srp-card__info flex__item"}).find("div",{"class":"m-srp-card__price"}).text.split())
    try:
        d["Rent"]=("Rs " + priceL[1] +" " + priceL[2])
    except:
        d["Rent"]=("Rs " + priceL[1])        
        
    d["Type"] = all[i].find("div",{"class":"m-srp-card__desc flex__item"}).find("div",{"class":"m-srp-card__heading clearfix"}).find("h3").find("span",{"class":"m-srp-card__title"}).find("span",{"class":"m-srp-card__title__bhk"}).text.strip()
    
    f=list(all[i].find("div",{"class":"m-srp-card__desc flex__item"}).find("div",{"class":"m-srp-card__heading clearfix"}).find("h3").find("span",{"class":"m-srp-card__title"}).text.split())
    d["Description"]=' '.join(map(str,f[3:]))
    
    x=all[i].find("div",{"class":"m-srp-card__desc flex__item"}).find("div",{"class":"m-srp-card__collapse js-collapse"}).find("div",{"class":"m-srp-card__summary js-collapse__content"}).find_all("div",{"class":"m-srp-card__summary__item"})
    for i in range(0,len(x)):
        if (x[i].find("div",{"class":"m-srp-card__summary__title"}).text.strip().title()) != "Availability":
            if (x[i].find("div",{"class":"m-srp-card__summary__title"}).text.strip().title()) != "Owner Resides":
                try:
                    d[x[i].find("div",{"class":"m-srp-card__summary__title"}).text.strip().title()]=x[i].find("div",{"class":"m-srp-card__summary__info"}).text

                except:
                    pass
            else:
                pass
        else:
            pass
        
    z=all[i].find("div",{"class":"m-srp-card__desc flex__item"}).find("div",{"class":"m-srp-card__action"}).find("div",{"class":"m-srp-card__advertiser m-srp-card__advertiser--crisil text-right"})
    if z != None:
        d["Agent name"]=z.find("div",{"class":"m-srp-card__advertiser__name"}).text
    else:
        d["Agent name"]="Agent name not available"

    l.append(d)
    
# print(l)   

df=pandas.DataFrame(l)
# df

df.to_csv("RentingHouse.csv")
