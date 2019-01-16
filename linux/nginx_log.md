## nginx 直接在配置文件中切割日志

直接在nginx配置文件中，配置日志循环，而不需使用 `logrotate` 或配置 `cron` 任务。需要使用到 `$time_iso8601` 内嵌变量来获取时间。$time_iso8601格式如下：2016-01-05T18:12:02+02:00。然后使用正则表达式来获取所需时间的数据。

### 按天切割日志

```bash
if ($time_iso8601 ~ "^(\d{4})-(\d{2})-(\d{2})") {
    set $year $1;
    set $month $2;
    set $day $3;
}
access_log /data/logs/nginx/ng-$year-$month-$day-access.log;
```

或者使用perl语法

```bash
if ($time_iso8601 ~ "^(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2})") {}
access_log /data/logs/nginx/ng-$year-$month-$day-access.log;
```

### 按时、分、秒分割

```bash
if ($time_iso8601 ~ "^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})")
{
    set $year $1;
    set $month $2;
    set $day $3;
    set $hour $4;
    set $minutes $5;
    set $seconds $6;
}
```
