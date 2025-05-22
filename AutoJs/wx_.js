const PACKAGE_ID_WW = 'com.tencent.wework';
/**
 * @description 处理通知
 */
function notificationHandler(n) {
  try {
    var packageId = n.getPackageName(); // 获取通知包名
    var abstracts = n.tickerText; // 获取通知摘要
    var text = n.getText(); // 获取通知文本
    // var title = n.getTitle()
    // 过滤 PackageId 白名单之外的应用所发出的通知
    if (!text || !filterNotification(packageId, abstracts, text)) {
      return;
    }
    if (text.indexOf('晚上') >= 0 && text.indexOf('游泳') >= 0) {
      brightScreen(); // 唤醒屏幕
      unlockScreen(); // 解锁屏幕
      sleep(5000);
      opendd();
      clockOut('ding51283e6f2093cabe');
      sleep(5000);
      lockScreen(); // 关闭屏幕
    } else if (
      text.indexOf('今天') >= 0 &&
      text.indexOf('游泳') >= 0
    ) {
      brightScreen(); // 唤醒屏幕
      unlockScreen(); // 解锁屏幕
      sleep(5000);
      opendd();
      clockIn('ding51283e6f2093cabe');
      sleep(5000);
      lockScreen(); // 关闭屏幕
    } else if (text.includes('daoji') && text.includes('解锁')) {
      brightScreen(); // 唤醒屏幕
      unlockScreen(); // 解锁屏幕
      //sleep(3000);
      n.delete();
      lockScreen(); // 关闭屏幕
    } else if (text.includes('daoji') && text.includes('退出')) {
      toast('已关闭脚本！');
      log('已关闭脚本！');
      engines.myEngine().forceStop();
    }
  } catch (e) {
    console.log(e);
    return
    //send_dd('打卡出错，请重试！');
    back();
    home();
    lockScreen();
  }
}

/**
 * @description 锁屏
 */
function lockScreen() {
  console.log('关闭屏幕');
  back();
  home();
  // text('锁屏').findOne().click();
  className('android.widget.RelativeLayout').desc('锁屏').findOne().click();

  device.setBrightnessMode(1); // 自动亮度模式
  device.cancelKeepingAwake(); // 取消设备常亮

  sleep(3000); // 等待屏幕关闭
  if (isDeviceLocked()) {
    console.info('屏幕已关闭');
  } else {
    console.error('屏幕未关闭, 请尝试其他锁屏方案, 或等待屏幕自动关闭');
  }
}

/**
 * @description 唤醒设备
 */
function brightScreen() {
  console.log('唤醒设备');

  device.setBrightnessMode(0); // 手动亮度模式
  device.wakeUpIfNeeded(); // 唤醒设备
  device.keepScreenOn(); // 保持亮屏
  sleep(1000); // 等待屏幕亮起

  if (!device.isScreenOn()) {
    console.warn('设备未唤醒, 重试');
    device.wakeUpIfNeeded();
    brightScreen();
  } else {
    console.info('设备已唤醒');
  }
}

/**
 * @description 解锁屏幕
 */
function unlockScreen() {
  console.log('解锁屏幕');

  if (isDeviceLocked()) {
    gesture(
      320, // 滑动时间：毫秒
      [
        device.width * 0.5, // 滑动起点 x 坐标：屏幕宽度的一半
        device.height * 0.7, // 滑动起点 y 坐标：距离屏幕底部 10% 的位置, 华为系统需要往上一些
      ],
      [
        device.width / 2, // 滑动终点 x 坐标：屏幕宽度的一半
        device.height * 0.1, // 滑动终点 y 坐标：距离屏幕顶部 10% 的位置
      ],
    );
    sleep(1000);
    password_input();
    sleep(1000); // 等待解锁动画完成
    home();
    sleep(1000); // 等待返回动画完成
  }

  if (isDeviceLocked()) {
    console.error('上滑解锁失败, 请按脚本中的注释调整 gesture(time, [x1,y1], [x2,y2]) 方法的参数!');
    return;
  }
  console.info('屏幕已解锁');
}
// 屏幕是否为锁定状态
function isDeviceLocked() {
  importClass(android.app.KeyguardManager);
  importClass(android.content.Context);
  var km = context.getSystemService(Context.KEYGUARD_SERVICE);
  return km.isKeyguardLocked();
}

/**
 * @description 启动并登陆钉钉
 */
function opendd() {
  //app.launchPackage(PACKAGE_ID_DD)
  app.launchApp('钉钉');
  console.log('正在启动' + app.getAppName(PACKAGE_ID_DD) + '...');
  setVolume(0); // 设备静音
  sleep(10000); // 等待钉钉启动
  if (
    currentPackage() == PACKAGE_ID_DD &&
    currentActivity() != 'com.alibaba.android.user.login.SignUpWithPwdActivity'
  ) {
    console.info('账号已登录');
    sleep(1000);
  }
}
function setVolume(volume) {
  device.setMusicVolume(volume);
  device.setNotificationVolume(volume);
  console.verbose('媒体音量:' + device.getMusicVolume());
  console.verbose('通知音量:' + device.getNotificationVolume());
}
function password_input() {
  sleep(1000);
  click(300, 1380);
  sleep(500);
  click(780, 1380);
  sleep(500);
  click(780, 1500);
  sleep(500);
  click(575, 1380);
  sleep(500);
  click(540, 1800);
  sleep(500);
  click(780, 1650);
}
/**
 * @description 使用 URL Scheme 进入考勤界面
 */
function attendKaoqin(corp_id) {
  var url_scheme =
    'dingtalk://dingtalkclient/page/link?url=https://attend.dingtalk.com/attend/index.html';

  if (corp_id != '') {
    url_scheme = url_scheme + '?corpId=' + corp_id;
  }

  var a = app.intent({
    action: 'VIEW',
    data: url_scheme,
    //flags: [Intent.FLAG_ACTIVITY_NEW_TASK]
  });
  app.startActivity(a);
  console.log('正在进入考勤界面...');
  console.info('已进入考勤界面');
  sleep(1000);
}
/**
 * @description 下班打卡
 */
function clockOut(corp_id) {
  console.log('下班打卡...');
  console.log('等待连接到考勤机...');
  attendKaoqin(corp_id);
  sleep(5000);
  if (null != textMatches('下班打卡').clickable(true).findOne(1000)) {
    btn_clockout = textMatches('下班打卡').clickable(true).findOnce();
    btn_clockout.click();
    console.log('按下打卡按钮');
    sleep(5000);
    if (null != textMatches('继续打卡').clickable(true).findOne(1000)) {
      btn_clockout = textMatches('继续打卡').clickable(true).findOnce();
      btn_clockout.click();
      console.log('按下打卡按钮');
    }
  } else {
    click(device.width / 2, device.height * 0.56);
    console.log('点击打卡按钮坐标');
    if (null != textMatches('继续打卡').clickable(true).findOne(1000)) {
      btn_clockout = textMatches('继续打卡').clickable(true).findOnce();
      btn_clockout.click();
      console.log('按下打卡按钮');
    }
  }
  sleep(10000);
  back();
  sleep(500);
  back();
  sleep(500);
  home();
}

/**
 * @description 上班打卡
 */
function clockIn(corp_id) {
  console.log('上班打卡...');
  console.log('等待连接到考勤机...');
  attendKaoqin(corp_id);
  sleep(5000);
  if (null != textMatches('上班打卡').clickable(true).findOne(1000)) {
    btn_clockout = textMatches('上班打卡').clickable(true).findOnce();
    btn_clockout.click();
    console.log('按下打卡按钮');
    sleep(5000);
    if (null != textMatches('继续打卡').clickable(true).findOne(1000)) {
      sleep(1000);
      btn_clockout = textMatches('继续打卡').clickable(true).findOnce();
      btn_clockout.click();
      console.log('按下打卡按钮');
    }
  } else {
    click(device.width / 2, device.height * 0.56);
    console.log('点击打卡按钮坐标');
    if (null != textMatches('继续打卡').clickable(true).findOne(1000)) {
      btn_clockout = textMatches('继续打卡').clickable(true).findOnce();
      btn_clockout.click();
      console.log('按下打卡按钮');
    }
  }
  sleep(10000);
  back();
  sleep(500);
  back();
  sleep(500);
  home();
}
