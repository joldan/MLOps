import torch
import torch.nn as nn
import torch.nn.functional as F

class MLP_Model(nn.Module):
  def __init__(self,name="MLP_MODEL", vocab_size=260, embedding_dim=4, num_classes=4):
    super().__init__()
    self.name = name
    self.embedding = nn.Embedding(num_embeddings=vocab_size,embedding_dim=embedding_dim)
    self.conv1 = nn.Conv2d(3, 64, 4, stride=2, padding=1, bias=False)
    self.bn1 = nn.BatchNorm2d(64)
    self.conv2 = nn.Conv2d(64, 128, 4, stride=2, padding=1, bias=False)
    self.bn2 = nn.BatchNorm2d(128)
    self.conv3 = nn.Conv2d(128, 256, 4, stride=2, padding=1, bias=False)
    self.bn3 = nn.BatchNorm2d(256)
    self.conv4 = nn.Conv2d(256, 64, 4, stride=2, padding=1, bias=False)
    self.bn4 = nn.BatchNorm2d(64)
    self.linear1 = nn.Linear(64*16*12+5+(embedding_dim-1), 1024)
    self.linear2 = nn.Linear(1024, 512)
    self.linear3 = nn.Linear(512, 128)
    self.linear4 = nn.Linear(128, 64)
    self.out = nn.Linear(64, num_classes)


  def forward(self, x,tabulars):
    # entrada de 256*192
    emb_Location = self.embedding(tabulars[:,4])
    #plt.imshow(x[0])
    x = x.view(x.size(0), 3, 256, 192)
    x = torch.round(x).to(torch.float32)
    x = F.relu(self.bn1(self.conv1(x)))
    x = F.relu(self.bn2(self.conv2(x)))
    x = F.relu(self.bn3(self.conv3(x)))
    x = F.relu(self.bn4(self.conv4(x)))
    x = x.view(x.size(0), -1)
    x = torch.concat([x, tabulars[:,0:4], emb_Location], -1)
    x = F.relu(self.linear1(x))
    x = F.relu(self.linear2(x))
    x = F.relu(self.linear3(x))
    x = F.relu(self.linear4(x))
    x = torch.sigmoid(self.out(x))
    return x