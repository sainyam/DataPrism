import pandas as pd

def check_constr(c1,c2,df):
    val_map={}
    for index,row in df.iterrows():
        if row[c1] in val_map.keys():
            if val_map[row[c1]]==row[c2]:
                continue
            else:
                val_map[row[c1]]="wrong"
        else:
            val_map[row[c1]]=row[c2]
            
    iter=0
    for c in val_map.keys():
        if val_map[c]=="wrong":
            continue
        else:
            iter+=1
    #print (val_map)
    return iter*1.0/len(list(val_map.keys()))


def return_malfunction(df):
    print (check_constr('ZipCode','State',df),check_constr('CountyName','State',df),check_constr('ZipCode','CountyName',df))
    total=(check_constr('ZipCode','State',df)+check_constr('CountyName','State',df)+check_constr('ZipCode','CountyName',df))/3
    return 1-total#check_constr('ZipCode','State',df)

def run(data, threshold, bugs):
    df = pd.read_csv(data)
    violation = return_malfunction(df)
    print(violation, "#######################")
    return violation <= threshold, violation

if __name__ == "__main__":
	#df=pd.read_csv('clean.csv')
	df=pd.read_csv('hospital_100.csv')
	print (return_malfunction(df))
