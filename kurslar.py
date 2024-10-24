import pandas as pd

# fileni yuklayapti
file = 'files/data.xls'
raw_data = pd.read_excel(file)

# Table holatiga keltiryapti
df = pd.DataFrame(raw_data)

# date columni valuelarini date tipiga o'tkizyapti
df['date'] = pd.to_datetime(df['date'])

# date va currency larini index sifatida belgilayapti
df.set_index(['date', 'currency'], inplace=True)

# barcha date larni list qilib olyapti
all_dates = pd.date_range(start=df.index.get_level_values('date').min(), 
                          end=df.index.get_level_values('date').max())

# datani datelarga solishtirib chiqyapti
idx = pd.MultiIndex.from_product([all_dates, df.index.get_level_values('currency').unique()],
                                 names=['date', 'currency'])

# qaytadan tartiblayapti
df_full = df.reindex(idx)

# rate valuelarini olib kelyapti
df_full['rate'] = df_full['rate'].groupby(level='currency').ffill()

# unit valuelarini olib kelyapti
df_full['unit'] = df_full['unit'].groupby(level='currency').ffill()

# indekslarni ochiryapti
df_filled = df_full.reset_index()

# missing datelarni qoyib chiqyapti
df_filled['date'] = df_filled['date'].dt.date

# excelga export qilyapti
output_file = 'output9.xlsx'
df_filled.to_excel(output_file, index=False)

# export natijasini korsatyapti
print(f'Data successfully exported to {output_file}')
