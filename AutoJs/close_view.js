// text('锁屏').findOne().click();
// className("android.widget.RelativeLayout").desc("锁屏").findOne().click();




// runtime.accessibilityBridge.getService().performGlobalAction(AccessibilityService.GLOBAL_ACTION_LOCK_SCREEN)

// 请求无障碍服务权限
auto.waitFor();

// 下拉通知栏
// 获取屏幕宽度和高度
let { width, height } = device;
// 计算滑动起始点和结束点 (从顶部中间向下滑动一段距离)
let startX = width / 2;
let startY = 0;
let endX = width / 2;
let endY = height / 1; // 向下滑动屏幕高度的三分之一，可以根据需要调整
let duration = 300; // 滑动持续时间 (毫秒)

// 执行下拉滑动
swipe(startX, startY, endX, endY, duration);

// 等待通知栏动画完成
sleep(1000); // 等待1秒，可以根据设备性能调整

// 尝试查找并点击 "锁屏" 按钮
// 优先通过文本查找
// let lockButton = text("锁屏").findOne(2000); // 查找超时设置为2秒

// if (!lockButton) {
//     // 如果通过文本找不到，尝试通过描述查找
//     lockButton = desc("锁屏").findOne(2000);
// }

// // 如果找到了按钮，则点击
// if (lockButton) {
//     log("找到了锁屏按钮，尝试点击");
//     lockButton.click();
// }

const suo_x = 280
const suo_y = 400

click(suo_x, suo_y)




