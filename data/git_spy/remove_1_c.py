#%%
with open(r'C:\Users\jokub\Desktop\algoritmai\new\data\git_spy\SPY_FROM_GIT copy.csv') as f:
    lines = f.readlines()

# %%
lines = [x.split(',') for x in lines]
# %%
lines[0].pop(1)
# %%
for i in range(1, len(lines)):
    lines[i].pop(0)

# %%
lines = [",".join(x) for x in lines]
# %%
lines = "".join(lines)
# %%
with open('SPY_FROM_GIT', "w", encoding="utf-8") as f:
    f.write(lines)
# %%
