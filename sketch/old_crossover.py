    for idx, b in enumerate(gene_mask):
      if b:
        new_chr.path.append(self[idx])
      else:
        sel2.append(self[idx])
        pos1.append(idx)
        np.append(pos2, np.where(chr2==self[idx]))
        #pos2.append(chr2.path.index(self[idx]))
    pos2.sort()
    for pi1, p2 in enumerate(pos2):
      new_chr.path.insert(pos1[pi1], chr2[p2])
      new_chr2.path.pop(p2)
      new_chr2.path.insert(p2,sel2.pop(0))

