import pandas as pd

catalog = pd.read_csv('catalog.csv')

def remove_digits(s):
    return ''.join([letter for letter in s if not letter.isdigit()])
catalog['Class Number'] = catalog['Class Number'].apply(remove_digits)
catalog.head(5)

group_class = catalog.groupby('Class Number').size()
sorted_counts = group_class.sort_values(ascending=False)
sorted_counts

engl_classes = catalog[catalog['Class Number'].str.strip().str.upper() == 'ENGL']

engl_classes.to_csv('engl_classes.csv', index=False)

catalog['Terms Offered'] = catalog['Terms Offered'].fillna('')
autumn_count = catalog[catalog['Terms Offered'].str.contains('Autumn', na=False)].shape[0]
winter_count = catalog[catalog['Terms Offered'].str.contains('Winter', na=False)].shape[0]
spring_count = catalog[catalog['Terms Offered'].str.contains('Spring', na=False)].shape[0]
print(f"Classes offered in Autumn: {autumn_count}")
print(f"Classes offered in Winter: {winter_count}")
print(f"Classes offered in Spring: {spring_count}")
