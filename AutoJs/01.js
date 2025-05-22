/**
 * 企业微信 打卡脚本
 */

auto();
const PACKAGE_ID_DD = "com.tencent.wework"; // 企业微信
const PACKAGE_ID_WX = "com.tencent.mm"; // 微信
const PACKAGE_ID_WHITE_LIST = [PACKAGE_ID_WX];
const NOTIFICATIONS_FILTER = true;

const waitTime = 1000 * 3;

function delay_click(text) {
  if (null != textMatches(text).findOne(waitTime)) {
    sleep(100);
    click(text);
    log(`点击${text}`);
  } else {
    log(`${text}不存在`);
  }
}

function click_check_in_button() {
  if (null != text("打卡").findOne(waitTime)) {
    sleep(100);
    click("打卡");
  }
}

function click_work_platform() {
  while (!textContains("工作台").exists()) {
    sleep(100);
  }
  console.log("启动完成");
  click("工作台");
}

function checkState() {
  if (textContains("正常").exists()) {
    log("打卡成功");
  } else {
    log("打卡失败");
  }
}

// main();

function shangBan() {
  const btn = textContains("上班").clickable(false).findOne(waitTime);
  if (null != btn) {
    log(`点击${btn.text()}`);
    click(btn.text());
  }
}

function xiaBan() {
  const btn = textContains("下班").clickable(false).findOne(waitTime);
  if (null != btn) {
    log(`点击${btn.text()}`);
    click(btn.text());
  }
}

// 屏幕是否为锁定状态
function isDeviceLocked() {
  importClass(android.app.KeyguardManager);
  importClass(android.content.Context);
  var km = context.getSystemService(Context.KEYGUARD_SERVICE);
  return km.isKeyguardLocked();
}

/**
 * @description 锁屏
 */
function lockScreen() {
  console.log("关闭屏幕");
  back();
  sleep(500);
  home();
  home();
  sleep(1000);
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
  const suo_x = 280
  const suo_y = 400
  click(suo_x, suo_y)

  device.setBrightnessMode(1); // 自动亮度模式
  device.cancelKeepingAwake(); // 取消设备常亮

  sleep(3000); // 等待屏幕关闭
  if (isDeviceLocked()) {
    console.info("屏幕已关闭");
  } else {
    console.error("屏幕未关闭, 请尝试其他锁屏方案, 或等待屏幕自动关闭");
  }
}

/**
 * @description 唤醒设备
 */
function brightScreen() {
  console.log("唤醒设备");

  device.setBrightnessMode(0); // 手动亮度模式
  device.wakeUpIfNeeded(); // 唤醒设备
  device.keepScreenOn(); // 保持亮屏

  if (!device.isScreenOn()) {
    console.warn("设备未唤醒, 重试");
    device.wakeUpIfNeeded();
    brightScreen();
  } else {
    console.info("设备已唤醒");
  }
}

/**
 */
function unlockScreen() {
  // 上滑解锁
  swipe(
    device.width * 0.5,
    device.height * 0.8,
    device.width * 0.5,
    device.height * 0.2,
    1000
  );
}


brightScreen(); // 唤醒屏幕
sleep(5000);
unlockScreen(); // 解锁屏幕
sleep(5000);

console.log("正在启动" + app.getAppName("com.tencent.wework") + "...");
app.launchApp("企业微信");
click_work_platform();
click_check_in_button();
log(`第一次点击上班打卡`);
delay_click("上班打卡");
checkState();

lockScreen(); // 关闭屏幕
