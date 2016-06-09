  def __ordered_crossover_single(self, chr2):
    new_chr = self.copy()
    new_chr2 = chr2.copy()

# pick random elements of element 1
    gene_mask = np.random.rand(len(self.path)) > 0.5
    print("gene_mask={m}".format(m=gene_mask))
    #print(gene_mask)
    gene_idx = np.where(gene_mask)
# get the fixed elements
    fix1 = self[gene_idx]
    not_gene_idx = np.where(np.logical_not(gene_mask))
# get the elements that are gonna swap order
    swap1 = self[not_gene_idx]
# select the fixed elements in chr2(boolean)
    gene2_mask = np.in1d(chr2.path, fix1, assume_unique=True)
    #gene2_idx = np.where(gene2_mask)
# get the fixed elements in chromosome 2
    #fix2 = chr2.path[gene2_idx]
# get the elements that are gonna swap order
    not_gene2_idx = np.where(np.logical_not(gene2_mask))
    swap2 = chr2.path[not_gene2_idx]
# swap first chromosome's selected elements by second chromosome elements
# (reordering by 2nd chromosome)
    new_chr.path[not_gene_idx] = swap2

# swap second chromosome's selected elements by first chromosome elements
# (reordering according to 1st chromosome's order)
    new_chr2.path[not_gene2_idx] = swap1
    return new_chr,new_chr2
