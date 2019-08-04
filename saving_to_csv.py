#saving to csv

n_pd.to_csv('nodes.csv', sep=',', encoding='utf-8', index=False)
n_tags_pd.to_csv('nodes_tags.csv', sep=',', encoding='utf-8', index=False)
w_pd.to_csv('ways.csv', sep=',', encoding='utf-8', index=False)
w_nodes_pd.to_csv('ways_nodes.csv', sep=',', encoding='utf-8', index=False)
w_tags_pd.to_csv('ways_tags.csv', sep=',', encoding='utf-8', index=False)