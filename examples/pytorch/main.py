#!/usr/bin/env python

import argparse
import time

import progressbar
import torch
import torchvision

from dataset import PencroftDataset


def train(source, use_pytorch_loader=False, workers=1, use_resnet50=False):
    start_time = time.time()

    if use_pytorch_loader:
        dataset = torchvision.datasets.ImageFolder(
            source,
            torchvision.transforms.Compose([
                torchvision.transforms.CenterCrop(224),
                torchvision.transforms.ToTensor(),
            ])
        )
    else:
        dataset = PencroftDataset(source)
        if workers > 1:
            dataset.loader.make_mp_safe()

    loader = torch.utils.data.DataLoader(
        dataset,
        batch_size=32, shuffle=True, num_workers=workers, pin_memory=True)

    if use_resnet50:
        model = torchvision.models.resnet50()
    else:
        class Model(torch.nn.Module):
            def __init__(self):
                super(Model, self).__init__()
                self.fc = torch.nn.Linear(224 * 224 * 3, 1000)

            def forward(self, x):
                x = x.view(x.size(0), -1)
                return self.fc(x)
        model = Model()

    model = torch.nn.DataParallel(model).cuda()

    criterion = torch.nn.CrossEntropyLoss().cuda()
    optimizer = torch.optim.SGD(model.parameters(), 0.1)

    bar = progressbar.ProgressBar()
    for data, label in bar(loader):
        data = torch.autograd.Variable(data).cuda()
        label = torch.autograd.Variable(label).cuda(async=True)
        output = model(data)
        loss = criterion(output, label)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    print('Finished in %f seconds.' % (time.time() - start_time,))


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Train on one epoch of DATA')
    parser.add_argument('source')
    parser.add_argument('--pytorch_loader', action='store_true')
    parser.add_argument('--workers', type=int, default=1)
    parser.add_argument('--use_resnet50', action='store_true')
    args = parser.parse_args()
    train(
        args.source,
        use_pytorch_loader=args.pytorch_loader,
        workers=args.workers,
        use_resnet50=args.use_resnet50,
    )
