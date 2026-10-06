# 当前 GitHub 源码版本

版本：TES-EES-SCIENTIFIC-V5-PRESENTATION-V9-20261006。科学模型为 2026 年 10 月 4 日的 V5，图稿呈现为 2026 年 10 月 6 日的 V9。

当前上游源码包为 TES_MT_upstream_source_only.zip，后处理源码包为 TES_MT_postprocess_source_only.zip。两者与本地 V9 完整交付包内的源码档案逐字节一致。运行 python VERIFY_SOURCES.py 可校验档案、文件清单和压缩包完整性。

把两个 ZIP 解压在同一个目录，使 upstream_reproducible_code 和 postprocess_reproducible_code 保持同级。使用 64 位 Python 3.12 和上游 requirements-lock.txt 安装依赖，再按 README.md 的入口运行。

完整投稿图稿还依赖集成包内 EES_Submission_Package/Analysis_Scripts 和 Active_Learning_Upgrade 的配套脚本及数据。仅解压这两个源码档案，不等于具备重建全部投稿图稿的所有输入。正文、补充信息和最终图稿以本地 V9 投稿包为准。

历史 V2.2.0 源码和原始使用说明位于 archive/TES-EES-V2.2.0-20260909。引用当前模型时注明本版本标识及实际使用的 Git 提交；既有 Zenodo DOI 不代表此 V9 已单独存档。
