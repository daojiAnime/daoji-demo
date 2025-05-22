
// 发送自定义广播给Tasker
app.sendBroadcast({
    action: 'net.dinglisch.android.taskerm.capture',
    extras: {
      from: 'Autojs',
      version: '3.1.0 Beta',
      info: 'You got me :)',
    },
  });