# import implicit
# from scipy.sparse import coo_matrix
# import numpy as np
# import pandas as pd
# from . import models


"""
TO DO: finish up on pro services search recommendation algorithim
"""

# def run2():
#     query = models.ServiceSearchHistory.objects.all().values('user','professional_service','search_count')
#     data = pd.DataFrame.from_records(query)
#     data['user'] = data['user'].astype("category")
#     data['professional_service'] = data['professional_service'].astype("category")
#
#     # create a sparse matrix of all the users/search History  (i,j,v) format
#     stars = coo_matrix(
#                         (
#                             np.ones(data.shape[0]), #data
#                                (
#                                 data['user'].cat.codes.copy(), #row
#                                 data['professional_service'].cat.codes.copy() #column
#                                 )
#                             )
#                         )
#
#     # initialize model
#     model = implicit.als.AlternatingLeastSquares(factors=50)
#
#     # train the model on a sparse matrix of item/user/confidence weights
#     model.fit(stars)
#
#     # recommend items for a user
#     user_items = stars.T.tocsr()
#
#     recommendations = model.recommend(1, user_items)
#
#     return(recommendations)
#

"""
ends here
"""
