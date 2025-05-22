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
  } else {
    log(`打卡按钮不存在`);
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
    capture();
  } else {
    log("打卡失败");
    capture();
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
  home();
  home();
  // text('锁屏').findOne().click();
  className("android.widget.TextView").text("一键锁屏").findOne().click();

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
/**
 * @description 发送自定义广播给Tasker
 */
function capture() {
  app.sendBroadcast({
    action: "net.dinglisch.android.taskerm.capture",
  });
  sleep(1000 * 10);
}

brightScreen(); // 唤醒屏幕
sleep(5000);
unlockScreen(); // 解锁屏幕
sleep(5000);

console.log("正在启动" + app.getAppName("com.tencent.wework") + "...");
app.launchApp("企业微信");
click_work_platform();
click_check_in_button();
log(`第一次点击下班打卡`);
delay_click("下班打卡");
checkState();

lockScreen(); // 关闭屏幕
