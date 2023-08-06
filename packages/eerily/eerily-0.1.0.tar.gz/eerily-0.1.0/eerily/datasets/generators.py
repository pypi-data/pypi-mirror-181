import torch
from torch.utils.data import Dataset


class SinTimeSeriesDataset(Dataset):
    def __init__(self, sequence_length, input_length, prediction_length, nodes) -> None:
        super().__init__()

        self.sequence_length = sequence_length
        self.prediction_length = prediction_length
        self.input_length = input_length

        assert self.sequence_length > self.prediction_length
        self.nodes = nodes

        self._gen_data()

    def _gen_data(self):

        series = []
        for i in range(self.nodes):
            series.append(torch.sin(torch.linspace(i, self.sequence_length + i, self.sequence_length + 1)))

        self.data = torch.stack(series)

    def _slice(self, index):
        return (
            self.data[:, index : index + self.input_length],
            self.data[
                :,
                index + self.input_length : index + self.input_length + self.prediction_length,
            ],
        )

    def __len__(self):
        return self.sequence_length - self.input_length

    def __getitem__(self, index):
        return self._slice(index)


if __name__ == "__main__":

    d = SinTimeSeriesDataset(100, 5, 1, 3)

    print(d.data.shape)

    print(d[0][0].shape, d[0][1].shape)
    print(d[0])
