import pandas as pd

df = pd.read_csv('covid-stringency-index.csv', sep=';', encoding = 'utf8')
print(df.head())
_ = df.groupby(["Entity"]).apply(lambda x: x.to_csv(fr"Stringency{x.name}.csv", index=False, encoding="utf-8"))
