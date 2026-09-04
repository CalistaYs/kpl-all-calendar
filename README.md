# KPL 全赛程订阅日历

把所有 KPL 队伍的官方比赛放进同一个可订阅日历，自动跟随官方赛程更新。无需按战队分别维护，也不会影响原有的 [成都 AG 专属日历](https://github.com/CalistaYs/kpl-ag-calendar)。

## 一键订阅

### 国内推荐（Gitee）

```text
https://gitee.com/CalistaYs/kpl-all-calendar/raw/main/kpl_all.ics
```

### GitHub 备用

```text
https://raw.githubusercontent.com/CalistaYs/kpl-all-calendar/main/kpl_all.ics
```

iPhone：打开 **设置 > 日历 > 账户 > 添加账户 > 其他 > 添加已订阅的日历**，粘贴上面的地址并保存。

日历名称为 **KPL 全赛程日历**。每场比赛包含：

- 对阵双方、官方开赛时间与比赛阶段
- BO 赛制、比赛地点（官方提供时）
- 完赛比分（连续两次读取一致后确认）
- 开赛前 1 小时和 30 分钟提醒

## 数据与更新

数据来自腾讯 KPL/TGA 官方结构化接口 `getSchedules`，不是网页表格。项目自动扫描当前年份前后各一年内的候选赛事，包括 KPL 春季赛、夏季赛、年度总决赛、挑战者杯及官方接口覆盖的王者荣耀国际赛事。

GitHub Actions 每 30 分钟触发一次：

- 每 6 小时完整扫描，发现新赛事、新比赛、改期或取消。
- 比赛临近、进行中和刚结束时提高比分刷新频率。
- 其他时间不请求接口，直接跳过。
- 更新先经过 UID、比分、时间、队名和场次数量校验；异常时保留上一版日历。
- GitHub 更新完成后，由 Gitee 仓库镜像自动拉取同一提交，供国内订阅。

## 文件结构

| 文件 | 用途 |
|---|---|
| `kpl_all.ics` | 对外订阅的 KPL 全赛程日历 |
| `fetch.py` | 调用官方接口并发现赛事 |
| `match_parser.py` | 标准化所有比赛字段和队名简称 |
| `validator.py` | 更新前的数据安全校验 |
| `ics_generator.py` | 生成、合并和解析 ICS |
| `update_calendar.py` | 完整更新入口 |
| `smart_update.py` | GitHub Actions 智能刷新入口 |

## 手动维护

日常不需要手动编辑 `kpl_all.ics`。赛季或队伍变动会从官方数据自动进入日历。

需要临时扩大历史范围时，可设置：

```text
SEASON_SCAN_YEARS=2024,2025,2026,2027
```

官方启用新的赛事代号时，可用逗号分隔的 `SEASON_ID_PATTERNS` 覆盖候选模板；模板中的 `{year}` 会自动替换为年份。

本地完整刷新：

```text
python update_calendar.py
```

本地测试：

```text
python -m unittest discover -v
```

官方赛事页面：https://pvp.qq.com/match/kpl/
