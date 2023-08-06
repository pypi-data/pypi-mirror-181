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
from torch import Tensor, no_grad, sigmoid, ones, tensor
from torch.nn import Module, GRU, Embedding, Linear
from torch.nn.functional import binary_cross_entropy_with_logits
from torch.nn.utils.rnn import PackedSequence
from torchtyping import TensorType
from typing import List, Optional
from ..utils.data import RecurrentTreeDataBatch


class RecurrentTree(Module):
    def __init__(self, size: int, d_model: int = 1024, d_input: int = 256,
                 loss_function=binary_cross_entropy_with_logits):
        """
        :param size: `RecurrentTreeDataset.dictionary` size
        :param d_input: embedding vector size
        :param d_model: hidden vector size
        :param loss_function: loss function used in loss method.
        """
        super().__init__()
        self.embedding = Embedding(size, d_input)  # has useless EOS entry.
        self.gru = GRU(d_input, d_model)
        self.output = Linear(d_model, size - 1)  # SOS excluded from output
        self.loss_function = loss_function
        self.output_size = size - 1

    def forward(self, batch: RecurrentTreeDataBatch,
                hidden: TensorType['batch', 'embedding', float]) -> PackedSequence:
        x, _, idx = batch

        # Ad-hoc: https://discuss.pytorch.org/t/28184/4
        x = PackedSequence(self.embedding(x.data), x.batch_sizes, x.sorted_indices, x.unsorted_indices)  # BxS > BxSxE
        x = self.gru(x, hidden[idx].unsqueeze(0))[0]
        x = PackedSequence(self.output(x.data), x.batch_sizes, x.sorted_indices, x.unsorted_indices)  # BxSxE > BxSxO
        return x

    def loss(self, batch: RecurrentTreeDataBatch,
             hidden: TensorType['batch', 'embedding', float]) -> Tensor:
        return self.loss_function(self.forward(batch, hidden).data, batch[1].data)

    @no_grad()
    def beam_search(self, hidden: TensorType['batch', 'embedding', float], *,
                    recovery: Optional[List[List[int]]] = None,
                    topk: int = 10, depth: int = 4, candidates=40):
        """
        :param hidden: reaction embeddings.
        :param recovery: known part of reagents for recovery. should be the same length for each reaction.
        :param topk: number of reagents combinations.
        :param candidates: looking space for topk. should be between topk and total reagents space.
        :param depth: maximal number of reagents in sets.
        """
        assert topk >= 3, 'At least 3 beams should be generated'
        assert depth >= 2, 'At least 2 tokens should be generated: reagent and EOS'
        assert candidates <= self.output_size, 'number of candidates should be less or equal to the number of outputs'
        b = hidden.size(0)
        if recovery is not None:
            assert len(recovery) == b, 'known reagents list should match reactions count'
            assert all(len(recovery[0]) == len(x) for x in recovery), 'known reagents should be the same length'

        # reshape hidden to fit beams count
        # BxH > Bx1xH > BxKxH > B*KxH > 1xB*KxH
        hid = hidden.unsqueeze(1).expand(-1, topk, -1).flatten(end_dim=1).unsqueeze(0)

        if recovery is None:
            inp = [[0]] * b  # Bx1 [SOS]
        else:
            inp = [[0] + x for x in recovery]  # BxN [SOS, RG1, ...]

        # NxB > NxBxE > 1xBxH > 1xBxT
        x = sigmoid(self.output(self.gru(self.embedding(tensor(inp, device=hidden.device).transpose(0, 1)),
                                         hidden.unsqueeze(0))[1]))
        if recovery is None:
            x[:, :, 0] = 0  # set EOS proba to 0 to prevent [SOS, EOS] output
        else:
            # disable known reagents
            mask = tensor(recovery).unsqueeze(0) - 1  # 1xBxN
            mask_ = ones(1, b, self.output_size, device=hidden.device)  # 1xBxT
            mask_.scatter_(2, mask, 0)
            x = x * mask_

        probs, ti = x.topk(topk)  # 1xBxT > 1xBxK
        probs = probs.permute(1, 2, 0)  # 1xBxK > BxKx1

        # do parallel processing of topK beams
        # topk unique seqs. BxK
        unique = [[frozenset([x - 1 for x in s[1:]] + [x]) for x in x] for x, s in zip(ti.squeeze(0).tolist(), inp)]
        # shift ti indexes. output layer unlike input doesn't code SOS (0).
        inp = [s + [x] for x, s in zip((ti + 1).squeeze(0).tolist(), inp) for x in x]  # B*KxN [SOS, ..., RGx]

        # mask picked to prevent repeats in sequences
        mask = tensor([[list(x) for x in x] for x in unique])  # BxKxN

        # topk results
        if recovery is None:
            found = [[] for _ in range(b)]
        else:  # check completeness of the known reagents
            found = []
            for i, (x, s) in enumerate(zip(ti.squeeze(0).tolist(), recovery)):
                if 0 in x:
                    j = x.index(0)
                    found.append([(s, probs[i, j, 0].item())])
                    probs[i, j, 0] = 0  # disable route
                else:
                    found.append([])

        for d in range(1, depth):
            mask_ = ones(b, topk, self.output_size, device=hidden.device)  # BxKxT
            mask_.scatter_(2, mask, 0)

            x = self.output(self.gru(self.embedding(tensor(inp, device=hidden.device).transpose(0, 1)), hid)[1])
            x = sigmoid(x).view(b, topk, -1) * mask_  # 1xB*KxT > BxKxT

            # select 2*topk for later sets intersection filtering.
            tp, ti = (probs * x).flatten(start_dim=1).topk(candidates)  # BxKx1 > BxKxT > BxK*T > BxC
            row = ti // self.output_size  # current token idx
            col = ti % self.output_size  # next token idx

            n_inp, n_probs, n_unique, mask = [], [], [], []
            # iterate over individual reactions
            for i, (u, f, cs, ns, ps) in enumerate(zip(unique, found, row.tolist(), col.tolist(), tp.tolist())):
                seen = set()
                np, nu, nm = [], [], []
                for c, n, p in zip(cs, ns, ps):
                    if (k := u[c] | {n}) in seen:  # ignore already found set
                        continue
                    seen.add(k)
                    if not n:  # EOS
                        f.append(([x + 1 for x in u[c]], pow(p, 1 / (d + 1))))
                        continue

                    s = inp[i * topk + c].copy()
                    s.append(n + 1)
                    n_inp.append(s)
                    np.append(p)
                    nu.append(k)
                    nm.append(list(k))
                    if len(nm) == topk:
                        break

                n_probs.append(np)
                n_unique.append(nu)
                mask.append(nm)

            #  prepare next iteration
            probs = tensor(n_probs).unsqueeze(-1)  # BxK > BxKx1
            unique = n_unique
            inp = n_inp
            mask = tensor(mask)

        for f, ps, us in zip(found, n_probs, n_unique):  # noqa. n_probs allways available
            # fill unfinished. probably we need to look deeper.
            for p, u in zip(ps, us):
                f.append(([x + 1 for x in u], pow(p, 1 / depth)))

        return [sorted(f, key=lambda x: x[1], reverse=True)[:topk] for f in found]


__all__ = ['RecurrentTree']
