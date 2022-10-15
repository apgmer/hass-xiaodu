# homeassistant 自定义 integration 集成xiaodu

## 拉取xiaodu小度设备到ha中

[https://xiaodu.baidu.com/saiya/smarthome/index.html](https://xiaodu.baidu.com/saiya/smarthome/index.html)

![img1](https://i.tiecode.xyz/20221012/img1.52mnkqh0v740.webp)

## 用法：

1. 添加继承 XiaoDu Api
2. 打开上述网站，登录百度账号，在接口调用中赋值request全部Cookie
3. 上述1中添加Cookie

## 支持设备类型

小度设备类型 对应 HA 设备类型

- [x] `SWITCH`, `OUTLET` 解析为 `Platform.SWITCH` 开关/插座
- [x] `SCENE_TRIGGER` 解析为 `Platform.BUTTON` 按钮
- [x] `CURTAIN` 解析为 `Platform.COVER` 窗帘 
  - 窗帘只能控制开/关/停 不能控制进度。 位置 > 50 执行关 否则执行开

## 其他

1. Cookie有失效时间
2. 边学边写可能有问题 
