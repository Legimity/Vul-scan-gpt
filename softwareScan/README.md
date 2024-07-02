# 软件漏扫

## goby

goby 最后导出的全面的报告只能支持 pdf 格式

先放了一个http://cyber.seu.edu.cn 的资产报告
导出资产报告位置：goby 右侧栏--web 检测

再放一个最后综合的报告：202406201106297647.pdf
很多内容都是空的，没有显示应用风险

goby 也不是命令行工具，不能直接调用

## nikto

运行需要 perl 环境
对 cyberseu 扫描
结果在 test_log 中，将结果给 gpt 分析，分析结果在 test_gpt 中
感觉 nikto 功能还是类似资产扫描，也有可能是 cyberseu 没有漏洞
