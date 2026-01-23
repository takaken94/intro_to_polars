# Pandas と Polars の比較・検証

## 概要
本リポジトリは、Python によるデータ処理・ETL 処理を想定し、**Pandas** と **Polars** のパフォーマンスおよび使い勝手を比較・検証する学習用プロジェクトです。

特に以下の観点で、実務利用を意識した検証を行っています。
- CSVファイルの読み込み性能
- データ検索・フィルタリング・集計処理
- Polars の Lazy API による最適化効果

## 利用技術
- Python 3.12
- Pandas
- Polars
- Docker / Dev Containers

## 検証内容
### 1. CSV読み込み速度の比較
| 手法 | 実行時間 | 備考 |
| :--- | :--- | :--- |
| **Pandas (CSVファイル)**     | 0.467秒 | |
| **Polars (CSVファイル)**     | 0.026秒 | Pandas の約18倍高速 |
| **Polars (Parquetファイル)** | 0.073秒 | |

#### 考察
- **Polarsの優位性:** 単純なCSV読み込みにおいて、PolarsはPandasに対して圧倒的なパフォーマンスを発揮しました。
- **並列処理:** Polars の Rustベースの並列処理エンジンが、小中規模以上のデータセットに対して有効であることを確認しました。
- **Parquet:** 今回の検証では、Parquet 読み込みが CSV の約2.8倍の時間となりました。

#### データセット
静岡県の法人データ（12万7千行、30列）のCSVファイルを用いて、読み込み速度の計測を行いました。<br>
2025年12月26日時点のデータを使用しています。<br>
出典：国税庁法人番号公表サイト（国税庁）<a href="https://www.houjin-bangou.nta.go.jp" target="_blank" rel="noopener noreferrer">https://www.houjin-bangou.nta.go.jp</a>

### 2. データ操作（検索・集計）の比較
同一CSVデータに対して、Pandas と Polarsで、以下のデータ操作を実装・比較しました。

- 単一条件によるフィルタリング
- 複数条件（IN 検索）によるフィルタリング
- 日付条件による抽出
- グループ化＋件数集計

| 処理内容 | Pandas | Polars |
|---|---|---|
| CSV読み込み | read_csv | read_csv |
| 単一条件検索 | df[df[col] == value] | df.filter(pl.col == value) |
| IN検索 | isin | is_in |
| 日付条件 | Timestamp比較 | Date型比較 |
| 集計 | groupby + size | group_by + len |

#### 使用したコード
- Pandas 実装: practice_pandas.py
- Polars 実装: practice_polars.py

### 3. Polars Lazy API による最適化検証
Polars の特徴である Lazy API を用いて、検索・集計処理を「遅延評価」で実装しました。

- scan_csv() による CSV の遅延読み込み
- filter / group_by / sort を組み合わせたクエリ構築
- collect() 時点での実行
- explain() を用いて、クエリの実行計画を確認できる

#### 考察
- Lazy API により、不要な列・行の読み込みが抑制される
- 大容量CSVを扱うETL処理では、I/O削減の効果が期待できる

#### 使用したコード
- Polars Lazy API 実装: practice_polars_lazy.py

## 検証環境
- **OS:** Windows 11 + WSL2 (Ubuntu 24.04)
- **CPU:** Intel Core i7-1260P @ 2.10GHz (12コア/16スレッド)
- **メモリ:** 16GB

## 実行方法（Docker / Dev Containers 対応）
1. **事前準備:** Docker Engine または Docker Desktop と VS Code (拡張機能: Dev Containers) を用意します。
2. **プロジェクト起動:** 本リポジトリを VS Code で開き、右下のポップアップまたはコマンドパレットから `コンテナで再度開く (Reopen in Container)` を選択します。
3. **1. CSV読み込み速度の比較:** コンテナ内のターミナルで以下のコマンドを実行します。
```bash
   python io_benchmark.py
```

## 実務での活用想定
- 大容量CSVを扱うETL・バッチ処理
- Pandas から Polars への移行検討時の技術検証
