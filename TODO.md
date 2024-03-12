1. 第一次进入小程序，可能会有权限请求弹窗。以下为最基本的位置信息请求界面。可能还会有其他请求弹窗，比如优惠券通知提醒这种的。常见于付费购买物品以后
```xml
<android.widget.RelativeLayout index="2" package="com.tencent.mm" class="android.widget.RelativeLayout" text="" checkable="false" checked="false" clickable="true" enabled="true" focusable="true" focused="false" long-clickable="false" password="false" scrollable="false" selected="false" bounds="[0,0][1080,2260]" displayed="true">
                  <android.widget.FrameLayout index="0" package="com.tencent.mm" class="android.widget.FrameLayout" text="" checkable="false" checked="false" clickable="true" enabled="true" focusable="true" focused="true" long-clickable="false" password="false" scrollable="false" selected="false" bounds="[0,1604][1080,2260]" displayed="true">
                    <android.widget.ScrollView index="0" package="com.tencent.mm" class="android.widget.ScrollView" text="" resource-id="com.tencent.mm:id/mcm" checkable="false" checked="false" clickable="false" enabled="true" focusable="true" focused="false" long-clickable="false" password="false" scrollable="false" selected="false" bounds="[0,1604][1080,2260]" displayed="true">
                      <android.widget.RelativeLayout index="0" package="com.tencent.mm" class="android.widget.RelativeLayout" text="" resource-id="com.tencent.mm:id/lzo" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" long-clickable="false" password="false" scrollable="false" selected="false" bounds="[0,1604][1080,2260]" displayed="true">
                        <android.widget.LinearLayout index="0" package="com.tencent.mm" class="android.widget.LinearLayout" text="" resource-id="com.tencent.mm:id/m00" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" long-clickable="false" password="false" scrollable="false" selected="false" bounds="[66,1659][1014,1739]" displayed="true">
                          <android.widget.ImageView index="0" package="com.tencent.mm" class="android.widget.ImageView" text="" resource-id="com.tencent.mm:id/lzs" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" long-clickable="false" password="false" scrollable="false" selected="false" bounds="[66,1666][132,1732]" displayed="true" />
                          <android.widget.LinearLayout index="1" package="com.tencent.mm" class="android.widget.LinearLayout" text="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" long-clickable="false" password="false" scrollable="false" selected="false" bounds="[154,1671][879,1727]" displayed="true">
                            <android.widget.TextView index="0" package="com.tencent.mm" class="android.widget.TextView" text="莉景天气" resource-id="com.tencent.mm:id/lzw" checkable="false" checked="false" clickable="false" enabled="true" focusable="true" focused="false" long-clickable="false" password="false" scrollable="false" selected="false" bounds="[154,1671][318,1727]" displayed="true" />
                            <android.widget.TextView index="1" package="com.tencent.mm" class="android.widget.TextView" text="申请" resource-id="com.tencent.mm:id/lzm" checkable="false" checked="false" clickable="false" enabled="true" focusable="true" focused="false" long-clickable="false" password="false" scrollable="false" selected="false" bounds="[346,1671][428,1727]" displayed="true" />
                          </android.widget.LinearLayout>
                          <android.widget.ImageView index="2" package="com.tencent.mm" class="android.widget.ImageView" text="" content-desc="说明" resource-id="com.tencent.mm:id/lzz" checkable="false" checked="false" clickable="true" enabled="true" focusable="true" focused="false" long-clickable="false" password="false" scrollable="false" selected="false" bounds="[901,1626][1047,1772]" displayed="true" />
                        </android.widget.LinearLayout>
                        <android.widget.TextView index="1" package="com.tencent.mm" class="android.widget.TextView" text="获取你的位置信息" resource-id="com.tencent.mm:id/lzq" checkable="false" checked="false" clickable="false" enabled="true" focusable="true" focused="false" long-clickable="false" password="false" scrollable="false" selected="false" bounds="[66,1794][1014,1857]" displayed="true" />
                        <android.widget.TextView index="2" package="com.tencent.mm" class="android.widget.TextView" text="将获取你的具体位置信息，用于获取用户所在地天气情况" resource-id="com.tencent.mm:id/mwy" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" long-clickable="false" password="false" scrollable="false" selected="false" bounds="[66,1879][1014,1993]" displayed="true" />
                        <android.widget.LinearLayout index="3" package="com.tencent.mm" class="android.widget.LinearLayout" text="" resource-id="com.tencent.mm:id/b3v" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" long-clickable="false" password="false" scrollable="false" selected="false" bounds="[185,2103][895,2213]" displayed="true">
                          <android.widget.Button index="0" package="com.tencent.mm" class="android.widget.Button" text="拒绝" resource-id="com.tencent.mm:id/lzn" checkable="false" checked="false" clickable="true" enabled="true" focusable="true" focused="false" long-clickable="false" password="false" scrollable="false" selected="false" bounds="[185,2103][515,2213]" displayed="true" />
                          <android.view.View index="1" package="com.tencent.mm" class="android.view.View" text="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" long-clickable="false" password="false" scrollable="false" selected="false" bounds="[515,2103][565,2213]" displayed="true" />
                          <android.widget.Button index="2" package="com.tencent.mm" class="android.widget.Button" text="允许" resource-id="com.tencent.mm:id/lzx" checkable="false" checked="false" clickable="true" enabled="true" focusable="true" focused="false" long-clickable="false" password="false" scrollable="false" selected="false" bounds="[565,2103][895,2213]" displayed="true" />
                        </android.widget.LinearLayout>
                      </android.widget.RelativeLayout>
                    </android.widget.ScrollView>
                  </android.widget.FrameLayout>
                </android.widget.RelativeLayout>
```
需要想办法点击允许/同意处理掉

发现：
1. 在最近使用界面，是可以通过wx.navigateToMiniProgram前往想要去的小程序的
2. 但是如果从小程序内部通过press_keycode退出来以后，没有办法通过wx.navigateToMiniProgram前往想要去的小程序，只能通过获取最近使用页面

1. 进入小程序时，可能会有倒计时类型的广告，需要点击跳过
2. **有的小程序进入以后会有广告弹窗，不点击掉则无法点击其他组件**。一种解决方法：观察当前webview界面中所有的组件的z-index，以此判断是否有组件覆盖在其他组件之上。有的话就说明存在弹窗 https://blog.51cto.com/haibo0668/5505488 
3. 有的小程序的页面比较长， 部分组件需要下滑以后才能点击到。但是将xpath路径转化为坐标以后就没法点击到这部分组件。
4. 不知道会不会有可能在遍历小程序的过程中出现权限请求弹窗。有没有一种办法能够在遍历小程序之前就同意所有权限请求？ --- 在进入一个新页面，点击之前先判断有没有弹窗，有就处理，没有就继续点击
5. 在进入首页之前，先检查隐私政策，点击掉隐私政策以后再检查广告弹窗
6. 广告弹窗种类多样，亚马逊的广告弹窗在源码里有wx-popup，但是麦当劳的没有

程序执行流程
1. 启动微信，点击发现，点击小程序，进入最近使用界面，方便在不小心退出小程序时自动回到刚刚退出的小程序。
2. 检查微信是否只有NATIVE_APP模式，如果只有这一种模式，kill微信并执行第一步
3. 通过appID启动指定小程序(TODO)(目前想到的实现方法：自己写一个小程序，里面只写跳转API，然后在动态测试目标小程序时，如果不慎退出，点击最近使用的小程序以回到原来的小程序)
4. 进入小程序以后，首先检查是否有广告（5s，可通过点击跳过进入）（TODO）
5. 检查是否有隐私政策界面，有则同意（有的小程序的隐私政策弹窗不在xml中，在webview里，比如掌上公交）
6. 检查是否有位置权限请求界面，有则同意
7. 检查是否有普通弹窗，比如通知类弹窗，底下有 类似我知道了 字样
8. 检查是否有广告弹窗（TODO），有则关闭
9. 获取小程序NATIVE_APP模式下的xml，获取该页面所有组件的坐标

[//]: # (8. 在执行点击之前，判断是否有广告弹窗/权限请求)
8. 根据坐标执行点击，点击后需要检查是否进入新页面，每进入一个新页面就将该新页面URL以及请求参数就添加到待跳转队列中。并判断该页面是否有弹窗/权限请求，有的话处理掉再然后回退到原页面，然后继续点击
9. 点击完一层以后，从刚才的新页面队列中取出新的页面URL以及请求参数，跳转到该页面，并重复执行7-9步