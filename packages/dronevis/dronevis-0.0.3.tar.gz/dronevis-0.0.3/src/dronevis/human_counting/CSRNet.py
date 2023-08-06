import torch.nn as nn
from torchvision import models

print("RUNNING ...")


class CSRNet(nn.Module):
    def __init__(self, load_weights=False):
        super(CSRNet, self).__init__()
        self.seen = 0
        self.frontend_feat = [
            64,  64, "M",
            128, 128, "M",
            256, 256, 256, "M",
            512, 512, 512,
        ]
        self.backend_feat = [512, 512, 512, 256, 128, 64]
        self.frontend = self.make_layers(self.frontend_feat)
        self.backend = self.make_layers(
            self.backend_feat, in_channels=512, dilation=True
        )
        self.output_layer = nn.Conv2d(64, 1, kernel_size=1)
        if not load_weights:
            mod = models.vgg16(weights=models.VGG16_Weights.IMAGENET1K_V1)
            self._initialize_weights()
            for i in range(len(self.frontend.state_dict().items())):
                list(self.frontend.state_dict().items())[i][1].data[:] = list(
                    mod.state_dict().items()
                )[i][1].data[:]

    def forward(self, x):
        x = self.frontend(x)
        x = self.backend(x)
        x = self.output_layer(x)
        return x

    def _initialize_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.normal_(m.weight, std=0.01)
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.BatchNorm2d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)

    def make_layers(self, cfg, in_channels=3, batch_norm=False, dilation=False):
        if dilation:
            d_rate = 2
        else:
            d_rate = 1
        layers = []
        for v in cfg:
            if v == "M":
                layers += [nn.MaxPool2d(kernel_size=2, stride=2)]
            else:
                conv2d = nn.Conv2d(
                    in_channels, v, kernel_size=3, padding=d_rate, dilation=d_rate
                )
                if batch_norm:
                    layers += [conv2d, nn.BatchNorm2d(v), nn.ReLU(inplace=True)]
                else:
                    layers += [conv2d, nn.ReLU(inplace=True)]
                in_channels = v
        return nn.Sequential(*layers)


if __name__ == "__main__":
    from torchvision import transforms
    import torch
    from PIL import Image
    import matplotlib.pyplot as plt
    import numpy as np

    transform = transforms.Compose(
        [
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )
    model = CSRNet()
    model = model.cuda()
    checkpoint = torch.load("./best_model.pth.tar")
    model.load_state_dict(checkpoint["state_dict"])
    img_paths = [f"{i}.jpeg" for i in range(5, 6)]
    from matplotlib import cm as c

    print("Predicting ...")
    for img_path in img_paths:
        img = transform(Image.open(img_path).convert("RGB")).cuda()

        output = model(img.unsqueeze(0))
        print(f"Predicted Count {img_path}: ", int(output.detach().cpu().sum().numpy()))
        temp = np.asarray(
            output.detach()
            .cpu()
            .reshape(output.detach().cpu().shape[2], output.detach().cpu().shape[3])
        )
        plt.imshow(temp, cmap=c.jet)
        plt.show()
        # print("Original Image")
        plt.imshow(plt.imread(img_path))
        plt.show()
