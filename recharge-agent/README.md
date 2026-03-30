# 虚拟充值智能体

## 功能
- 智能对话式产品推荐
- 分类浏览（视频/音乐/网盘/办公/外卖/游戏）
- 关键词搜索
- 一键跳转下单

## 如何修改商品数据

编辑 `index.html` 中的 `PRODUCTS` 数组：

```javascript
const PRODUCTS = [
  { 
    id: "txsp_month",              // 唯一标识（英文）
    name: "腾讯视频VIP",            // 商品名称
    category: "video",             // 分类ID（见下方CATEGORIES）
    price: 15,                     // 价格（元）
    desc: "月卡 - 官方直充",        // 描述
    tags: ["月卡", "官方直充"],    // 标签
    orderUrl: "https://..."        // 下单链接
  },
  // 添加更多商品...
];
```

## 分类ID对照表

| 分类ID | 分类名称 | 关键词 |
|--------|----------|--------|
| video | 视频会员 | 视频,腾讯,爱奇艺,优酷,芒果,b站,哔哩 |
| music | 音乐会员 | 音乐,网易云,qq音乐,酷狗,酷我 |
| cloud | 网盘下载 | 网盘,百度,迅雷,下载,云盘 |
| office | 办公学习 | 办公,wps,office,文档 |
| life | 外卖生活 | 外卖,美团,饿了么,生活 |
| game | 游戏充值 | 游戏,steam,充值,点卡 |

## 如何修改分类

编辑 `CATEGORIES` 数组：

```javascript
const CATEGORIES = [
  { id: "video", name: "视频会员", icon: "🎬", keywords: ["视频", "腾讯"] },
  // 添加更多分类...
];
```

## 如何部署

### GitHub Pages（免费）
1. 创建 GitHub 仓库
2. 上传 `index.html`
3. Settings → Pages → 选择分支 → 发布

### 本地预览
直接用浏览器打开 `index.html` 即可。

## 获取真实下单链接

目前商品使用占位符链接，你需要：

1. 登录 https://shop.yiquanyi.com
2. 找到每个商品的购买页面
3. 复制实际下单链接
4. 替换 `PRODUCTS` 中的 `orderUrl`

## 技术栈
- 纯 HTML/CSS/JavaScript（无需后端）
- 响应式设计，支持手机
- 智能关键词匹配
