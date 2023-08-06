from typing import Any, List, Optional, Callable

from datasets import Dataset
from transformers import PreTrainedTokenizerBase
from transformers.data import DataCollatorWithPadding

from ...core import TransformerDataModule


class SentenceEmbeddingDataModule(TransformerDataModule):
    """Defines the ``LightningDataModule`` for Sentence Embedding Datasets."""

    def process_data(self, dataset: Dataset, stage: Optional[str] = None) -> Dataset:
        input_feature_fields = [k for k, v in dataset["train"].features.items() if k not in ["label", "idx"]]
        dataset = SentenceEmbeddingDataModule.preprocess(
            dataset,
            tokenizer=self.tokenizer,
            input_feature_fields=input_feature_fields,
            padding=False,
            truncation=True,
            max_length=self.max_length,
        )
        cols_to_keep = [
            x for x in ["input_ids", "attention_mask", "token_type_ids"] if x in dataset["train"].features
        ]
        dataset.set_format("torch", columns=cols_to_keep)
        return dataset

    @staticmethod
    def convert_to_features(
        example_batch: Any, _, tokenizer: PreTrainedTokenizerBase, input_feature_fields: List[str], **tokenizer_kwargs
    ):
        # Either encode single sentence or sentence pairs
        if len(input_feature_fields) > 1:
            texts_or_text_pairs = list(
                zip(example_batch[input_feature_fields[0]], example_batch[input_feature_fields[1]])
            )
        else:
            texts_or_text_pairs = example_batch[input_feature_fields[0]]
        # Tokenize the text/text pairs
        return tokenizer(texts_or_text_pairs, **tokenizer_kwargs)

    @staticmethod
    def preprocess(ds: Dataset, **fn_kwargs) -> Dataset:
        ds = ds.map(
            # todo: change this to self.convert_to_features for users to override
            SentenceEmbeddingDataModule.convert_to_features,
            batched=True,
            with_indices=True,
            fn_kwargs=fn_kwargs,
        )
        return ds

    @property
    def collate_fn(self) -> Optional[Callable]:
        return DataCollatorWithPadding(self.tokenizer)
