def get_scaling_factor(cell, index, cutoff=0.05):
   '''
   get_scaling_factor takes a cell vector and its index in the gene expression matrix 
   that has been scaled according to single-cell RNA sequencing preprocessing procedure 
   and return the scaling factor for the cell.
   get_scaling_factor: ndarray Nat (Num) -> Num
   '''
   scaling_factor = cell.min()
   cell_recovered = cell / scaling_factor
   if np.abs(cell_recovered - cell_recovered.round()).mean()>cutoff:
      raise ValueError('Cell ' + str(index) + ' has not been processed by our assumption.')
   return 1 / scaling_factor


def unscale(smtx):
  '''
  unscale takes a cell * gene expression matrix that has been scaled cell-wise 
  and returns a recovered count matrix.
  unscale: csr_matrix -> csr_matrix
  '''
  scaling_factors = diags(
      [get_scaling_factor(smtx.getrow(i).data, str(i)) for i in range(smtx.shape[0])]
  )
  counts = scaling_factors * smtx
  return counts.rint()


def denormalize(smtx):
  '''
  denormalize takes a cell * gene expression matrix that has been normalized 
  according to single-cell RNA sequencing preprocessing procedure and 
  returns a recovered count matrix. 
  If the imput matrix is not normalized by first scaling then logarithmization, 
  then the function produces an error indicating so. 
  denormalize: csr_matrix -> csr_matrix
  '''
  smtx.eliminate_zeros()
  try:
      unscale(smtx)
  except:
      ebse = smtx.expm1()
      try:
          unscale(ebse)
      except:
          twobse = smtx.copy()
          twobse.data = 2 ** twobse.data - 1
          try:
              unscale(twobse)
          except:
              tenbase = smtx.copy()
              tenbase.data = 10 ** tenbase.data - 1 
              try:
                  unscale(tenbase)
              except:
                  raise ValueError('The matrix has not been normalized according to the preprocessing procedure in scRNA-seq.')
              else:
                  return unscale(tenbase)
          else:
              return unscale(twobse)
      else:
          return unscale(ebse)
  else:
      return unscale(smtx)


def rank_plot(cell, index, N=10):
  '''
  rank_plot takes a cell vector and its index in the gene expression matrix and 
  produces a plot of the first N most frequent values against their ranks. 
  Such a plot is used for error-checking in the unscaling process.
  '''
  c = pd.Series(cell)
  y = np.array(c.value_counts().sort_index().head(N).index)
  x = np.arange(1, N+1)
  plt.scatter(x, y, label=f'Cell {c_idx}')
  plt.legend()
  plt.xlabel('Rank in cell histogram')
  plt.ylabel('Scaled count');
  plt.xticks(x);


def check_plot(smtx):
  '''
  check_plot takes a recovered count matrix and produce a mean and variance plot
  for each gene. Such a plot is used to double-check if the denormalization
  process has been successful.
  '''
  cmean = np.array(smtx.mean(0))
  cvar = np.array(smtx.power(2).mean(0) - cmean ** 2)

  plt.loglog()
  plt.scatter(cmean, cvar, c='k', marker='.', label='Genes')
  plt.plot([1e-4, 1e3], [1e-4, 1e3], c='r')
  plt.xlim(1e-5);
  plt.ylim(1e-6);
  plt.xlabel('Mean')
  plt.ylabel('Variance')
  plt.title('Recovered counts')
  plt.legend(scatterpoints=3);