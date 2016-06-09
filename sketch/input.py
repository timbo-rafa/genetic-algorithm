from ga import Chromosome
import numpy as np
c1 = Chromosome(10)
c1.path.sort()
c2 = Chromosome(10)
c2.path.sort(reverse=True)
gene_mask = np.random.rand(10) > 0.5
sel1 = []
pos1 = []
pos2 = []
for idx, b in enumerate(gene_mask):
    if b:
        sel1.append(c1[idx])
    else:
        pos1.append(idx)
        pos2.append(c2.path.index(c1[idx]))

pos2.sort()
swappedpos = [i for i in np.where(gene_mask)]
