# qplot

qplot是一个基于qdata的数据可视化插件，用于绘制股票的日K线图和分时图，支持实时数据更新。

## 功能特性

- 📈 **日K线图绘制**：支持各种技术指标（如均线）和成交量显示
- ⏱️ **分时图绘制**：展示股票的日内走势和均价线
- 🔄 **实时数据更新**：通过双线程机制实现数据的实时获取和图表的动态更新
- 📊 **自定义样式**：支持自定义图表样式、颜色和尺寸
- 💾 **数据缓存**：内置数据缓存机制，提高数据访问效率
- 📱 **可安装性**：作为Python包可通过pip安装

## 安装

### 从源码安装

```bash
# 克隆仓库
cd d:/codespace/AstockQuant

# 安装qplot（开发模式）
cd qplot
pip install -e .
```

### 依赖项

qplot依赖于以下Python库：
- pandas
- numpy
- matplotlib
- mplfinance
- qdata（请先安装qdata插件）

这些依赖会在安装qplot时自动安装。

## 快速开始

以下是使用qplot绘制K线图和分时图的简单示例：

```python
import qplot
import qdata
from datetime import datetime, timedelta

# 获取股票数据
stock_code = "600519"
end_date = datetime.now().strftime('%Y%m%d')
start_date = (datetime.now() - timedelta(days=180)).strftime('%Y%m%d')
df = qdata.get_daily_data(stock_code, start_date, end_date)

# 绘制K线图
qplot.plot_kline(
    df,
    title=f"{stock_code} 日K线图",
    style='charles',
    volume=True,
    indicators=['ma5', 'ma10', 'ma20']
)

# 绘制分时图
# 注意：实际使用时请用真实的分时数据替代示例数据
sample_minute_data = qplot.examples.generate_sample_minute_data(stock_code)
qplot.plot_minute_chart(
    sample_minute_data,
    title=f"{stock_code} 分时图",
    line_color='blue',
    show_avg_line=True
)
```

## 实时数据更新

qplot支持实时更新K线图和分时图，通过双线程机制实现：

```python
import qplot

# 创建数据管理器
stock_code = "600519"
data_manager = qplot.DataManager(stock_code=stock_code, data_type='minute')

# 生成初始数据（实际应用中应使用真实数据）
initial_data = qplot.examples.generate_sample_minute_data(stock_code)
data_manager.update_data(initial_data)

# 启动实时更新
# 数据更新线程（每10秒更新一次）
data_manager.start_realtime_updates(interval=10)

# 绘制实时分时图
qplot.plot_minute_chart_realtime(data_manager, update_interval=10)

# 使用完毕后停止更新
data_manager.stop_realtime_updates()
```

## 示例

qplot提供了完整的使用示例，您可以在`examples`目录下找到：

```bash
cd examples
python usage_example.py
```

示例代码包含以下内容：
1. 绘制基本的日K线图
2. 绘制基本的分时图
3. 绘制实时更新的日K线图
4. 绘制实时更新的分时图

## 核心模块说明

### 1. 绘图器（Plotters）

- **CandlestickPlotter**：日K线图绘图器，支持各种技术指标
- **MinutePlotter**：分时图绘图器，支持实时更新

### 2. 数据管理（DataManager）

- 负责从qdata获取数据、缓存数据、管理实时数据更新
- 支持数据库存储（可选）

### 3. API接口

- `plot_kline()`：绘制日K线图
- `plot_minute_chart()`：绘制分时图
- `plot_kline_realtime()`：绘制实时更新的日K线图
- `plot_minute_chart_realtime()`：绘制实时更新的分时图

## 配置选项

### 绘图配置

- **标题**：设置图表标题
- **样式**：选择图表样式（适用于K线图）
- **颜色**：自定义线条颜色
- **尺寸**：设置图表尺寸
- **技术指标**：添加均线等技术指标（适用于K线图）
- **成交量**：显示/隐藏成交量（适用于K线图）

### 实时更新配置

- **更新间隔**：设置数据更新和图表刷新的时间间隔
- **数据源**：选择数据来源
- **数据库存储**：配置是否使用数据库存储数据

## 注意事项

1. 使用实时功能时，请确保有可靠的数据来源
2. 实时数据更新会占用较多系统资源，请根据实际情况调整更新间隔
3. 本插件仅用于数据可视化，不构成投资建议
4. 使用前请确保已正确安装qdata插件

## 许可证

[MIT License](LICENSE)

## 贡献

欢迎提交问题和改进建议！如有任何问题，请在GitHub仓库中提交issue。