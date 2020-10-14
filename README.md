# 課題検索くん
- 大学の課題サイトをスクレイピングし、未修の課題をLineに通知してくれる。
- 作成の流れ等は[Qitaの記事](https://qiita.com/yokubarisanyuyu/items/2ef369dc02cf78747b29) にまとめています。

<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F432257%2F68eb4788-b730-ebba-92e7-2e7148d00bbe.jpeg?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&s=dffd1e8218cfc258343ddc9370a33baf" width="100px">

<!-- 画像がずれてるので配置とサイズ修正 -->
# アピールポイント
- スクレイピング 
- Dockerを使い、環境構築が簡単に
- 日常の課題解決
<!-- # 全体の構成・使用技術・ライブラリなど -->
# 全体の構成・使用技術・ライブラリなど

## 使用技術
- Python 
- Docker 
- Line API (Line Notify)
- AWS lambda(デプロイ環境)

## ライブラリ
- beautifulsoup4 （スクレイピング）
- requests （スクレイピング）
- selenium　（スクレイピング,サイトのログイン）
- lambci/lambda (https://github.com/lambci/docker-lambda lamdaの環境構築)




<!-- # 注意・補足 -->

# 作成者
増井　悠太

