from aizynthfinder.utils.test_model import condition_pred

ans = condition_pred('COC(OC)OC.Cc1cccc(C)c1N(CC(=O)Nc1ccc(C(N)=NO)cc1)C(=O)C1CCS(=O)(=O)CC1>>Cc1cccc(C)c1N(CC(=O)Nc1ccc(-c2ncon2)cc1)C(=O)C1CCS(=O)(=O)CC1')
print(ans)