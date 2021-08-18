from autoglyphs import mint

with open("seeds.txt", "r") as f:
    seeds = [int(line[:-1]) for line in f]

out_path = "../examples/"
for seed in seeds:
    mint(seed=seed, out_path=out_path)
