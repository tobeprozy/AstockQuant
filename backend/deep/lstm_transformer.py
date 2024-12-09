import torch.nn as nn
import torch

class LSTMTransformer(nn.Module):
    def __init__(self, input_dim, hidden_dim, transformer_nhead, num_layers, num_classes):
        super(LSTMTransformer, self).__init__()
        self.lstm = nn.LSTM(input_size=input_dim, hidden_size=hidden_dim, num_layers=num_layers, batch_first=True)
        transformer_layer = nn.TransformerEncoderLayer(d_model=hidden_dim, nhead=transformer_nhead, batch_first=True)
        self.transformer_encoder = nn.TransformerEncoder(transformer_layer, num_layers=num_layers)
        self.fc = nn.Linear(hidden_dim, num_classes)

    def forward(self, x):
        # LSTM 处理
        lstm_out, _ = self.lstm(x)  # lstm_out 形状: [batch_size, seq_len, hidden_dim]
        # Transformer 处理
        transformer_out = self.transformer_encoder(lstm_out)
        # 确保 transformer_out 是三维的
        if transformer_out.dim() == 2:
            transformer_out = transformer_out.unsqueeze(1)  # 添加 seq_len 维度
        # 取最后一个时间步的输出用于分类
        out = self.fc(transformer_out[:, -1, :])  # 取每个批次的最后一个时间步

        return torch.sigmoid(out)

from tqdm import tqdm
def train_model(model, train_loader, val_loader, criterion, optimizer, num_epochs=10):
    for epoch in tqdm(range(num_epochs)):
        model.train()
        total_loss = 0
        for batch in train_loader:
            features = batch['features'].to(device)
            labels = batch['labels'].to(device).unsqueeze(1)  # 保证标签的维度和输出维度匹配

            optimizer.zero_grad()
            outputs = model(features)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        print(f'Epoch {epoch+1}, Train Loss: {total_loss / len(train_loader)}')

        model.eval()
        val_loss = 0
        with torch.no_grad():
            for batch in val_loader:
                features = batch['features'].to(device)
                labels = batch['labels'].to(device).unsqueeze(1)
                outputs = model(features)
                loss = criterion(outputs, labels)
                val_loss += loss.item()

        print(f'Epoch {epoch+1}, Validation Loss: {val_loss / len(val_loader)}')

def test_model(model, test_loader, criterion):
    model.eval()
    test_loss = 0
    with torch.no_grad():
        for batch in test_loader:
            features = batch['features'].to(device)
            labels = batch['labels'].to(device).unsqueeze(1)
            outputs = model(features)
            loss = criterion(outputs, labels)
            test_loss += loss.item()

    print(f'Test Loss: {test_loss / len(test_loader)}')

import os
import sys

cur_dir = os.path.dirname(os.path.abspath(__file__))
root = os.path.abspath(os.path.join(cur_dir, '..'))
if root not in sys.path:
    sys.path.append(root)

from get_data.ak_data_fetch import FinancialDataFetcher


from utils.indictor import StockTAIndicatorsCalculator
import datetime
from torch.utils.data import Dataset
import numpy as np
from torch.utils.data import DataLoader
import torch.optim as optim

# 数据规范化
def min_max_scale(X):
    min_val = np.min(X, axis=0)
    max_val = np.max(X, axis=0)
    scaled_X = (X - min_val) / (max_val - min_val)
    return scaled_X, min_val, max_val


# 数据划分
def train_val_test_split(X, y, train_ratio=0.7, val_ratio=0.15):
    total_size = len(X)
    train_size = int(total_size * train_ratio)
    val_size = int(total_size * val_ratio)

    X_train = X[:train_size]
    y_train = y[:train_size]
    X_val = X[train_size:train_size + val_size]
    y_val = y[train_size:train_size + val_size]
    X_test = X[train_size + val_size:]
    y_test = y[train_size + val_size:]

    return X_train, X_val, X_test, y_train, y_val, y_test

<<<<<<< HEAD

=======
>>>>>>> 35607909919233883c751c8f36edad03046a2590
# 定义 PyTorch 数据集类
class TimeSeriesDataset(Dataset):
    def __init__(self, features, labels):
        self.features = features
        self.labels = labels
    
    def __len__(self):
        return len(self.features)
    
    def __getitem__(self, idx):
        return {
            'features': torch.tensor(self.features[idx], dtype=torch.float),
            'labels': torch.tensor(self.labels[idx], dtype=torch.float)
        }
    

if __name__ ==  "__main__":

    stock_index = '512200'

    s_date = (datetime.datetime.now() - datetime.timedelta(days=10000)).strftime('%Y%m%d')
    e_date = datetime.datetime.now().strftime('%Y%m%d')

    # 创建数据获取器
    fetcher = FinancialDataFetcher()
    # 获取股票数据
    fetcher.fetch_fund_info(symbol=stock_index, start_date=s_date, end_date=e_date)
    fetcher.fund_rename()

    df=fetcher.fund_info

    calculator = StockTAIndicatorsCalculator(df)

    calculator.cal_ma(5)
    calculator.cal_ma(10)
    calculator.cal_ma(20)
    calculator.cal_ma(150)
    calculator.cal_stoch(5)
    calculator.cal_macd(10)

    df=calculator.df

    print(df)

    # 填充可能的缺失值
    df.fillna(method='ffill', inplace=True)
    df.fillna(method='bfill', inplace=True)

    # 选择特征和标签
<<<<<<< HEAD
    # features = df[['open', 'high', 'low', 'vol', 'Turnover', 'Amplitude', 'ChangePercent', 'MA5', 'MA10', 'MA20', 'STOCH_SLOWK', 'STOCH_SLOWD', 'MACD', 'MACD_SIGNAL', 'MACD_HIST']]
    features = df[['open','close','high', 'low', 'vol', 'Turnover',  'MA5', 'MA10', 'MA20', 'MACD', 'MACD_SIGNAL', 'MACD_HIST']]
=======
    features = df[['open', 'high', 'low', 'vol', 'Turnover', 'Amplitude', 'ChangePercent', 'MA5', 'MA10', 'MA20', 'STOCH_SLOWK', 'STOCH_SLOWD', 'MACD', 'MACD_SIGNAL', 'MACD_HIST']]
>>>>>>> 35607909919233883c751c8f36edad03046a2590
    # 计算明天的价格相对于今天的变化
    df['next_close'] = df['close'].shift(-1)  # 创建一个新列，其中包含下一天的收盘价
    df['is_up'] = (df['next_close'] > df['close']).astype(int)  # 如果下一天的收盘价高于今天，则标签为1
    # 删除最后一行因为它没有下一天的数据
    df = df[:-1]
    # 更新标签选择
    labels = df['is_up'].values

    # 数据规范化
    scaled_features, min_val, max_val = min_max_scale(features.values)
    X_train, X_val, X_test, y_train, y_val, y_test = train_val_test_split(scaled_features, labels)

    # 创建数据集实例
    train_dataset = TimeSeriesDataset(X_train, y_train)
    val_dataset = TimeSeriesDataset(X_val, y_val)
    test_dataset = TimeSeriesDataset(X_test, y_test)

<<<<<<< HEAD
    batch_size = 32
=======
    batch_size = 4
>>>>>>> 35607909919233883c751c8f36edad03046a2590

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)



    # 设定模型参数
    input_dim = 12  # 输入特征的维度
    hidden_dim = 128  # LSTM 隐藏层维度
    transformer_nhead = 8  # Transformer 中的头数
    num_layers = 2  # LSTM 和 Transformer 的层数

    num_classes = 1  # 输出类别数，例如涨跌概率

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = LSTMTransformer(input_dim, hidden_dim, transformer_nhead, num_layers, num_classes)
    criterion = nn.BCELoss()

    optimizer = optim.Adam(model.parameters(), lr=0.0025)


    train_model(model, train_loader, val_loader, criterion, optimizer, num_epochs=100)
    
    test_model(model, test_loader, criterion)