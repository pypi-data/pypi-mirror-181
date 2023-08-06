import random
import typing as tp

from datasets import Dataset
from dataclasses import dataclass
from transformers import DataCollatorWithPadding
from .data_utils import SpecialTokens


class REaLTabFormerDataset(Dataset):
    """ REaLTabFormer Dataset
    The REaLTabFormerDataset overwrites the _getitem function of the HuggingFace Dataset
    to use the custom vocab learned from the preprocessed data.

    Attributes:
        vocab (dict): Custom vocab learned from the preprocessed data
    """
    def token2id(self, example, vocab):
        for k in example:
            example[k] = vocab["token2id"].get(example[k], vocab["token2id"]["[UNK]"])

        return example

    def set_vocab(self, vocab):
        """ Set the Tokenizer
        Args:
            vocab: vocab learned from the data
        """
        self.vocab = vocab

    def _getitem(self, key: tp.Union[int, slice, str], decoded: bool = True, **kwargs) -> tp.Union[tp.Dict, tp.List]:
        """ Get Item from Tabular Data
        Get one instance of the tabular data, permuted, converted to text and tokenized.
        """
        # If int, what else?
        row = self._data.fast_slice(key, 1)

        shuffle_idx = list(range(row.num_columns))
        random.shuffle(shuffle_idx)
        return [self.vocab["token2id"][SpecialTokens.BOS]] + [self.vocab["token2id"][i] for i in x] + [self.vocab["token2id"][SpecialTokens.EOS]]

        vocab

        shuffled_text = ", ".join(
            ["%s is %s" % (row.column_names[i], str(row.columns[i].to_pylist()[0]).strip()) for i in shuffle_idx]
        )

        tokenized_text = self.tokenizer(shuffled_text)
        return tokenized_text


@dataclass
class REaLTabFormerDataCollator(DataCollatorWithPadding):
    """ REaLTabFormer Data Collator
    Overwrites the DataCollatorWithPadding to also pad the labels and not only the input_ids
    """
    def __call__(self, features: tp.List[tp.Dict[str, tp.Any]]):
        batch = self.tokenizer.pad(
            features,
            padding=self.padding,
            max_length=self.max_length,
            pad_to_multiple_of=self.pad_to_multiple_of,
            return_tensors=self.return_tensors,
        )
        batch["labels"] = batch["input_ids"].clone()
        return batch