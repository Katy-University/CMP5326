# 实验设计：AI 时代为什么 Regex 依然重要（Regex vs GPT 日志取证对比）

目标读者：数字取证 / 网络安全方向本科高年级或研究生；时长 90–120 分钟；可扩展为 2 次课。



## 学习目标（Learning Objectives）

完成实验后，学生能够： 1. 用正则表达式（Regex）在多源日志中可复现地抽取关键证据（IP、URL、邮箱、信用卡号、电话、USB 事件、登录结果）。 2. 使用通用大模型（GPT/ChatGPT 等）对同一数据集进行抽取，总结其优缺点与不可重复性/概率性。 3. 以精确率（Precision）/召回率（Recall）/F1/运行时间/可解释性为指标，客观比较 Regex 与 GPT 的效果。 4. 形成法庭可解释的方法论：规则可描述、步骤可重现、证据可验证（hash）。



## 预备知识（Prerequisites）

基本命令行（bash 或 PowerShell），会使用 grep / ripgrep (rg) 或同类工具。

基本 Regex 语法：分组、量词、字符类、边界（\b）、转义。

（可选）会用 Python 的 re 或者 Autopsy 的正则搜索模块。



## 实验资源（Resources）

数据集（已提供）：regex_vs_gpt_lab_dataset.zip（3 个日志文件 + ground truth）。

logs/web.log（Apache 风格，含 URL/IP/邮箱/信用卡 + 若干“伪卡号”）

logs/auth.log（SSH 登录成败 + IP）

logs/app.log（邮箱、电话、USB 插拔事件等）

ground_truth.csv（金标准：类型、值、文件、行号）

工具：ripgrep (rg) 或 grep；任意文本编辑器；可选：Autopsy、Python、Excel/LibreOffice。

一个可访问的大模型界面（如 ChatGPT 网页），或学校提供的 API（非必需）。



## 任务设计（Workflow）

### Part A：Regex 管道（Deterministic Pipeline）

下载与解压数据集：

unzip regex_vs_gpt_lab_dataset.zip -d lab
cd lab/regex_vs_gpt_lab

为每类实体编写 Regex（建议学生先各自写，再小组合并）：

IPv4（简单版）：\b(?:25[0-5]|2[0-4]\d|1?\d?\d)(?:\.(?:25[0-5]|2[0-4]\d|1?\d?\d)){3}\b

URL（简化）：https?://[^\s\"]+

Email：[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}

电话（示例，含 + 与分隔符）：\+?\d[\d\-\s()]{6,}\d

信用卡（13–16 位，后续可加 Luhn）：\b(?:\d[ -]*?){13,16}\b

USB 插入事件（关键字触发）：usb\s+\d+-\d+:\s+new\s+high-speed\s+USB\s+device\b

SSH 登录：

成功：Accepted password for\s+(\w+)\s+from\s+(\d+\.\d+\.\d+\.\d+)

失败：Failed password for\s+(\w+)\s+from\s+(\d+\.\d+\.\d+\.\d+)

运行匹配并导出结果（示例用 ripgrep）：

rg -n "[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}" logs > out_email.txt
rg -n "https?://[^\s\"]+" logs > out_url.txt
rg -n "\\b(?:25[0-5]|2[0-4]\\d|1?\\d?\\d)(?:\\.(?:25[0-5]|2[0-4]\\d|1?\\d?\\d)){3}\\b" logs > out_ip.txt
rg -n "\\b(?:\\d[ -]*?){13,16}\\b" logs > out_cc_raw.txt
rg -n "usb\\s+\\d+-\\d+:\\s+new\\s+high-speed\\s+USB\\s+device\\b" logs/app.log > out_usb.txt
rg -n "Accepted password for\\s+(\\w+)\\s+from\\s+(\\d+\\.\\d+\\.\\d+\\.\\d+)" logs/auth.log > out_login_ok.txt
rg -n "Failed password for\\s+(\\w+)\\s+from\\s+(\\d+\\.\\d+\\.\\d+\\.\\d+)" logs/auth.log > out_login_fail.txt

（可选）二次过滤信用卡：Luhn 校验

目的：去除“伪卡号”（数据集中包含若干 Luhn 失败的近似串）。

可用 Python 小脚本对 out_cc_raw.txt 提取数字并做 Luhn 过滤，生成 out_cc.txt。

合并/去重/规范化：将每类结果整理成两列：value,file:line，保存为 CSV/TSV。

### Part B：GPT 抽取（Probabilistic Pipeline）

将 web.log、auth.log、app.log 逐份或分块粘贴给 GPT，提示词模板： > “你是日志抽取器。请严格输出 JSON 数组。字段：type（从 {ip,url,email,credit_card,phone,login_success,login_fail,usb_insert} 里选）、value、file、line。不要推测，不要补全未知。若不确定请忽略。每行只输出实际出现的实体和对应的行号。”

收集 GPT 输出，合并去重，保存为 gpt_output.json 或 CSV。

记录耗时、提示词与操作步骤（用于可重复性评估）。

### Part C：对比与评估（Evaluation）

使用助教提供的 ground_truth.csv 作为金标准。

对比指标：

Precision = 真阳性 / (真阳性 + 假阳性)

Recall = 真阳性 / (真阳性 + 假阴性)

F1 = 2PR/(P+R)

Runtime：统计从开始到得到结果的总时长（手工+计算）。

Reproducibility：换人/换时间是否得到相同结果？（Regex 应高度一致；GPT 可能波动）

Explainability：能否清晰说明“为什么命中”？（Regex 规则可展示；GPT 依赖自然语言描述）

观察点：

信用卡近似串（带空格/连字符/失败 Luhn）→ Regex 原始匹配会有假阳性，二次 Luhn 过滤后显著改善。

GPT 在长文本/重复样式中可能漏检或行号错配。

Regex 对特殊格式（电话、URL 边界）可能过宽或过窄，需要迭代改进。



## 评分建议（Rubric）

实现（40%）：Regex 管道可运行，输出规范化结果；（可选）完成 Luhn 过滤。

评估（30%）：与 ground_truth.csv 对齐，正确计算 Precision/Recall/F1，并分析误差来源。

复现性与文档（20%）：完整记录命令、正则、参数、脚本和时间；结果可复现。

讨论（10%）：对 Regex 与 GPT 各自的优势/局限做出有理有据的结论，引用本实验数据支持观点。



## 讲授提示（Teaching Notes）

先让学生各自写 Regex，再小组合并，体会模式设计的 trade-off（宽 vs 严）。

刻意保留干扰样本（例如“像卡号但未过 Luhn”），引导学生思考“二阶段规则”。

GPT 部分鼓励学生记录提示词微调对结果的影响，凸显概率性与可重复性问题。



## 拓展与变体（Extensions）

Autopsy 实作：把三份日志封装为案例证据，使用 Autopsy 的 Keyword/Regex Search 与 Timeline 模块。

内存/网络：加入一小段 pcap 与 volatility 的 IOC 抽取对比。

法律维度：要求提交方法可解释的报告片段，模拟专家证人陈述。



## 参考 Regex 片段（可发给学生的速查）

邮箱：[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}

URL：https?://[^\s\"]+

IPv4：\b(?:25[0-5]|2[0-4]\d|1?\d?\d)(?:\.(?:25[0-5]|2[0-4]\d|1?\d?\d)){3}\b

信用卡（13–16 位）：\b(?:\d[ -]*?){13,16}\b（建议二次做 Luhn）

电话（通用、宽松）：\+?\d[\d\-\s()]{6,}\d

USB 插入：usb\s+\d+-\d+:\s+new\s+high-speed\s+USB\s+device\b

SSH 成功登录：Accepted password for\s+(\w+)\s+from\s+(\d+\.\d+\.\d+\.\d+)

SSH 失败登录：Failed password for\s+(\w+)\s+from\s+(\d+\.\d+\.\d+\.\d+)



## （可选）评分脚手架脚本思路

Python 读取 ground_truth.csv 与学生提交的提取结果（CSV/JSON），按 type+value+file:line 对齐，计算 P/R/F1。

记录运行时间、版本信息与命令行，用于复现实验。



注：本实验数据为教学合成，包含近似欺骗样本，用于对比 Regex（确定性规则）与 GPT（概率性抽取）在规模、可复现性、可解释性上的差异。