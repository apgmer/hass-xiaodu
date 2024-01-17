# homeassistant 自定义 integration 集成xiaodu

## 拉取xiaodu小度设备到ha中

[https://xiaodu.baidu.com/saiya/smarthome/index.html](https://xiaodu.baidu.com/saiya/smarthome/index.html)

![img1](https://i.tiecode.xyz/20221012/img1.52mnkqh0v740.webp)

## 用法：

clone 代码到 custom_components/xiaodu

configuration.yaml xiaodu:

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
2. **在厂商的app中操作开关状态后无法，小度不会获取最新状态** 
3. 边学边写可能有问题 

## 另
以上仅在小度接入了`南京物联`的设备中测试，其他厂商的设备尚不清楚

有能力的大佬可以自己开发，有什么不同的可以一起交流，本人也是菜鸡一枚

![IMG_0805](https://github.com/apgmer/hass-xiaodu/assets/9553342/9cbd450f-c2ba-41c3-9403-c5a4d576aa8f)
