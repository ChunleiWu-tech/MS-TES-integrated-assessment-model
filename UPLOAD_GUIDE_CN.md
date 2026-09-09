# GitHub 与 Zenodo 发布

本目录是本次准备上传的代码版本，尚未代为执行线上发布。不要上传整个投稿文件夹，也不要上传手稿、投稿信或 QA 作者核查记录。

1. 核对两份源码 ZIP、运行说明和第三方数据的再分发许可。
2. 在现有 MS-TES 仓库上传本目录文件并提交。旧 Release 和旧 DOI 对应的归档保持原样。
3. 新建 Release，使用未占用标签 `TES-EES-V2.2.0-20260909`，Target 选本次提交。标题填 MS-TES integrated assessment model。
4. 粘贴 RELEASE_DESCRIPTION.md。附加两个源码 ZIP、RUN_ALL.ps1、RECOMPUTE_NUMERICAL_AUDIT.py 和 SHA256SUMS.txt。
5. 在 Zenodo 打开新记录，核对版本标签、实际源码及校验和。同步开关本身不能证明新文件已经归档。
6. 取得并核对新版本 DOI 后，同步正文、独立 Data Availability Statement 和 CITATION.cff。旧版 DOI 22661577 不代表这次新增内容。

两份 ZIP 均小于 GitHub 网页单文件上传限额。公共归档不包含期刊全文或专有字体。运行说明和科学数据来源保留在源码包内。
