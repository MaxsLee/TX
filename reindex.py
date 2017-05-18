import pandas as pd
import numpy as np


# train
df = pd.read_csv(r'F:\WorkSpace\tpai\1\train5_0.txt', header=None, sep=',')
df = pd.DataFrame(df)
df = df.reindex(np.random.permutation(df.index))
df.to_csv(r'F:\WorkSpace\tpai\1\train5.txt', index=False, header=False, encoding='utf-8')

# test
# df = pd.read_csv(r'F:\WorkSpace\tpai\1\test4_0.txt', header=None, sep=',')
# df = pd.DataFrame(df)
# df = df.reindex(np.random.permutation(df.index))
# df.to_csv(r'F:\WorkSpace\tpai\1\test4.txt', index=False, header=False, encoding='utf-8')
