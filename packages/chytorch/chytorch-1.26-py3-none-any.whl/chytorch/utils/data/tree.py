# -*- coding: utf-8 -*-
#
#  Copyright 2022 Ramil Nugmanov <nougmanoff@protonmail.com>
#  This file is part of chytorch.
#
#  chytorch is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, see <https://www.gnu.org/licenses/>.
#
from collections import deque
from itertools import permutations
from random import sample
from torch import IntTensor, zeros, Size, float32, LongTensor
from torch.nn.utils.rnn import pack_sequence, PackedSequence
from torch.utils.data import Dataset
from torch.utils.data._utils.collate import default_collate_fn_map
from torchtyping import TensorType
from typing import Sequence, List, Dict
from ._types import DataTypeMixin, NamedTuple


class RecurrentTreeDataPoint(NamedTuple):
    inputs: List[TensorType['reagent', int]]
    targets: List[TensorType['reagent', 'target', float]]


class RecurrentTreeDataBatch(NamedTuple, DataTypeMixin):
    inputs: PackedSequence
    targets: PackedSequence
    idx: TensorType['batch', int]


def collate_recurrent_tree(batch) -> RecurrentTreeDataBatch:
    """
    Prepares batches of trees.
    """
    inputs = []
    targets = []
    idx = []
    for n, (inp, tgs) in enumerate(batch):
        inputs.extend(inp)
        targets.extend(tgs)
        idx.extend([n] * len(inp))
    inputs = pack_sequence(inputs, enforce_sorted=False)
    targets = pack_sequence(targets, enforce_sorted=False)
    return RecurrentTreeDataBatch(inputs, targets, LongTensor(idx))


default_collate_fn_map[RecurrentTreeDataPoint] = collate_recurrent_tree  # add auto_collation to the DataLoader


class RecurrentTreeDataset(Dataset):
    def __init__(self, data: Sequence[List[List[str]]], *, max_size: int = 1000, dictionary: Dict[str, int] = None):
        """
        Prepare combinatorial tree of reagents.

        Example:

        Possible reagents of single reaction

        [[solv1, cat1, base1],
         [solv1, cat1, base2],
         [cat2]]

         Will be converted to the next tree:

         [[sos] > [solv1, cat1, base1, base2, cat2],  # predict all possible first reagents

          [sos, solv1] > [cat1, base1, base2],  # predict all possible second reagents for the given first
          [sos, cat1] > [solv1, base1, base2],
          [sos, base1] > [solv1, cat1],
          [sos, base2] > [solv1, cat1],
          [sos, cat2] > [eos],

          [sos, solv1, cat1] > [base1, base2],  # predict all possible second reagents for the given first two
          [sos, solv1, base1] > [cat1],
          [sos, solv1, base2] > [cat1],
          [sos, cat1, solv1] > [base1, base2],
          [sos, cat1, base1] > [solv1],
          [sos, cat1, base2] > [solv1],
          [sos, base1, solv1] > [cat1],
          [sos, base1, cat1] > [solv1],
          [sos, base2, solv1] > [cat1],
          [sos, base2, cat1] > [solv1],

          [sos, solv1, cat1, base1] > [eos],  # predict completeness of the reagents list
          [sos, solv1, cat1, base2] > [eos],
          [sos, solv1, base1, cat1] > [eos],
          [sos, solv1, base2, cat1] > [eos],
          [sos, cat1, solv1, base1] > [eos],
          [sos, cat1, solv1, base2] > [eos],
          [sos, cat1, base1, solv1] > [eos],
          [sos, cat1, base2, solv1] > [eos],
          [sos, base1, solv1, cat1] > [eos],
          [sos, base1, cat1, solv1] > [eos],
          [sos, base2, solv1, cat1] > [eos],
          [sos, base2, cat1, solv1] > [eos]]
        """
        self.data = data
        self.max_size = max_size
        if dictionary is not None:
            self.dictionary = dictionary
        else:
            self.dictionary = dictionary = {'<SOS>': 0, '<EOS>': 1}
            for conditions in data:
                for condition in conditions:
                    for reagent in condition:
                        if reagent not in dictionary:
                            dictionary[reagent] = len(dictionary)

    def __getitem__(self, item: int) -> RecurrentTreeDataPoint:
        tl = len(self.dictionary) - 1
        tree = self._tree(item)
        depth = self._depth(tree)

        inputs = []
        targets = []
        for seq in depth:
            inputs.append(IntTensor([x for x, _ in seq]))

            tv = zeros(len(seq), tl, dtype=float32)
            for n, (_, ts) in enumerate(seq):
                for t in ts:
                    tv[n, t - 1] = 1.
            targets.append(tv)
        return RecurrentTreeDataPoint(inputs, targets)

    def _tree(self, item):
        dictionary = self.dictionary

        tree = {0: {}}  # in the beginning was the word and the word was SOS
        for i, conditions in enumerate(self.data[item]):
            for reagents in permutations(conditions):
                current = tree[0]
                for reagent in reagents:
                    reagent = dictionary[reagent]
                    if reagent not in current:
                        current[reagent] = current = {}
                    else:
                        current = current[reagent]
                current[1] = i
        return tree

    def _depth(self, tree):
        sequences = []
        stack = deque([(0, 0, tree[0], False)])  # root always has target reagents
        path = []
        while stack:
            d, ck, cl, dead = stack.pop()
            if isinstance(cl, int):
                if dead:
                    sequences.append(path.copy())
                continue
            elif len(path) > d:
                path = path[:d]

            path.append((ck, list(cl)))
            d += 1
            for nk, nl in cl.items():
                stack.append((d, nk, nl, len(cl) == 1))
        if len(sequences) > self.max_size:
            return sample(sequences, self.max_size)
        return sequences

    def __len__(self):
        return len(self.data)

    def size(self, dim):
        if dim == 0:
            return len(self)
        elif dim is None:
            return Size((len(self),))
        raise IndexError


__all__ = ['RecurrentTreeDataset', 'RecurrentTreeDataPoint', 'RecurrentTreeDataBatch', 'collate_recurrent_tree']
