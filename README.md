# 教你用 Python 来玩微信跳一跳

## update
 > 使用了 ＠wangshub 的框架和 ＠moneyDboat 使用opencv找点的思路，保留了原始的代码。

## run
python my_wechat_jump.py

[＠wangshub](https://github.com/wangshub/wechat_jump_game)

手机机型:小米Mix2

## 待解决Debug
 * 加分音响和奶茶杯子边缘和内部的颜色不一样，阀值仍待调节。
 * 游戏截图的速度仍待调节。


## 弊端

 * 匹配模板依赖手机截屏的清晰度，需要自己根据原图来截取小人。
 * 对于加分音响，长方体音响，靠颜色识别，中心找不准；需要依赖上次跳到中心后出现的白点。

## Debug
 * 截图间隔太短时，会把跳到中心时出现的小人周围的圆环截图到，带来识别的麻烦。适当增加延时，减少识别的难度，还可以吃到额外的加分。
 * 开始向下扫描寻找最高点的高度不能太大，防止有的盒子出现位置太高。
 * 找中心白点时从上向下；找颜色相同的点和边缘实线从下向上。


## 增加功能1
 * 增加了my_wechat_jump.py　和　combine_opencv.py，使用opencv找点。
 * 可保存每一步的截图；
 * 可选择是否在图片上显示找出点的位置 ；


## 增加功能2
 * 找中心点更加准确，对小人的中心像素位置进行了修正；
 * 分数可以达到15000+;

## 增加功能3
 * 改变找小人的方法，除了可以使用模板匹配外，加入了小人紫色的颜色匹配。
 > 我们可以通过对比几个图发现，小人紫色的RGB并不均匀，中心处的紫色也与两侧的各有差异。但是放大小人底部像素，可以发现小人底部最下边几个紫色像素都是相同的（ａｍａｚｉｎｇ）。通过寻找底部的位置就可以找到小人。
