import matplotlib.pyplot as plt
import psutil
from aizynthfinder.aizynthfinder import AiZynthFinder
from aizynthfinder.context.scoring.scorers import StateScorer

# 初始化 AiZynthFinder
filename = "config.yml"
finder = AiZynthFinder(filename)

# 选择库存、扩展策略和过滤策略
finder.stock.select("zinc")
finder.expansion_policy.select("uspto")
finder.filter_policy.select("uspto")

# 设置目标 SMILES
# finder.target_smiles = "COc1cc(C=CC(=O)O)cc(OC)c1OC"
finder.target_smiles = "Cc1cccc(c1N(CC(=O)Nc2ccc(cc2)c3ncon3)C(=O)C4CCS(=O)(=O)CC4)C"

# 打印当前进程使用的内存
print(psutil.Process().memory_info().rss / (1024 * 1024), "MB")

# 执行树搜索
finder.tree_search()
finder.build_routes()

# 创建 StateScorer
scorer = StateScorer(finder.config)

# 收集所有反应路径及其得分
route_scores = []
for route_dict in finder.routes:
    reaction_tree = route_dict['reaction_tree']
    score = scorer(reaction_tree)
    route_scores.append(score)

# 打印每个路径的得分，这里应该显示不同的得分
for idx, score in enumerate(route_scores):
    print(f"Score for route {idx}: {score}")

first_route_info = finder.routes[0]
print("First route metadata:", first_route_info['route_metadata'])
print("First route score already calculated:", first_route_info['score'])

plt.imshow(finder.routes.make_images()[0])
plt.show()

plt.imshow(finder.routes.reaction_trees[0].to_image())
plt.show()

tree = finder.routes.reaction_trees[0]
print(tree.to_dict())
