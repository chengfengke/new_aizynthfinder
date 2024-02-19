from aizynthfinder.chem import Molecule
from rdkit import Chem
from rdkit.Chem.Draw import MolToImage


class ReactionTree:
    def __init__(self, _type=None, hide=None, smiles=None, is_chemical=None, in_stock=None, children=()):
        self._type = _type
        self.hide = hide
        self.smiles = smiles
        self.is_chemical = bool(is_chemical) if is_chemical is not None else None
        self.in_stock = bool(in_stock) if in_stock is not None else None
        self.children = list(children)

    @classmethod
    def from_dict(cls, dic):
        children_data = dic.get('children', [])
        children = [cls.from_dict(child) for child in children_data] if children_data else []
        return cls(
            _type=dic.get('type'),
            hide=dic.get('hide'),
            smiles=dic.get('smiles'),
            is_chemical=dic.get('is_chemical'),
            in_stock=dic.get('in_stock'),
            children=children
        )

    def print_tree_txt(self, indent=0):
        if self._type is not None:
            print(' ' * indent + f"_type: {self._type}")
        if self.hide is not None:
            print(' ' * indent + f"hide: {self.hide}")
        if self.smiles is not None:
            print(' ' * indent + f"smiles: {self.smiles}")
        if self.is_chemical is not None:
            print(' ' * indent + f"is_chemical: {self.is_chemical}")
        if self.in_stock is not None:
            print(' ' * indent + f"in_stock: {self.in_stock}")
        for child in self.children:
            child.print_tree(indent + 4)

    @classmethod
    def _get_img_from_smiles(smile):
        mol = Chem.MolFromSmiles(Molecule(smiles=smile).smiles)
        return MolToImage(mol)

    # def print_tree_img(self):
    #     if self is None:
    #         return
    #     q = queue.Queue()
    #     q.put(self)
    #     q.put(None)
    #     level = 1
    #     while not q.empty():
    #         node = q.get()
    #         if node is None:
    #             break
    #         while node is not None:
    #             plt.imshow(ReactionTree._get_img_from_smiles(node.smiles))
    #             plt.title('' + str(level) + ':' + node.smiles)
    #             plt.show()

