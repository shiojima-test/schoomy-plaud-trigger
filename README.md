# schoomy-plaud-trigger

> **AIへの引き渡し用ドキュメント**
> このREADMEをそのままAIチャットに貼り付けるだけで、開発を継続できます。
> 機能追加・変更のたびに「## 更新履歴」と該当セクションを更新してください。

---

## システム概要

スクーミーボード（ブルーボード）のスイッチ押下をトリガーに、macOS上でPLAUDの録音を自動開始・停止するシステムです。

- スイッチ1回目 → PLAUD録音開始
- スイッチ2回目 → 録音停止
- ブルーボード未接続時は接続待機して自動復帰
- Mac起動時にログイン項目で自動起動

**リポジトリ:** `https://github.com/shiojima-test/schoomy-plaud-trigger.git`
**言語:** Python 3
**対応OS:** macOS

---

## ファイル構成

```
~/schoomy-plaud-trigger/
├── plaud_trigger.py       # メインスクリプト
└── start_trigger.command  # ダブルクリックで起動するシェルスクリプト
```

---

## 仕組み

```
スクーミーボード（スイッチ押下）
  → シリアル通信で "RECORD_START" を送信
  → plaud_trigger.py がシリアルを監視
  → 録音開始: open "plaud://record" + cliclick で録音ボタンをクリック
  → 録音停止: cliclick で停止ボタンをクリック
```

---

## ブルーボード側プログラム（スクーミーIDE）

```cpp
#include <SchooMyUtilities.h>
SchooMyUtilities scmUtils = SchooMyUtilities();

void setup() {
  Serial.begin(9600);
  pinMode(19, INPUT);
}

bool lastState = false;

void loop() {
  bool pressed = !digitalRead(19);
  if (pressed && !lastState) {
    Serial.println("RECORD_START");
    delay(50);
  }
  lastState = pressed;
}
```

- **ピン:** 19番
- **ボーレート:** 9600
- スイッチを押した瞬間だけ `RECORD_START` を送信（チャタリング防止）

---

## Mac側セットアップ

### 必要なもの

- Python 3（Anaconda推奨）
- pyserial: `pip install pyserial`
- cliclick: `brew install cliclick`
- PLAUDデスクトップアプリ（`/Applications/Plaud.app`）

### PLAUDのURLスキーム

PLAUDアプリは `plaud://` URLスキームに対応しています。

```bash
open "plaud://record"  # 録音画面を開く
```

### 座標設定

`plaud_trigger.py` 内の座標は環境によって異なります。

```python
CLICLICK = "/opt/homebrew/bin/cliclick"  # cliclickのパス
```

```python
subprocess.run([CLICLICK, "c:1319,111"])   # 録音開始ボタン
subprocess.run([CLICLICK, "c:1593,357"])   # 録音停止ボタン
```

座標の調べ方：

```bash
cliclick p  # マウスを乗せた状態で実行すると座標が表示される
```

### シリアルポート

```python
ser.port = '/dev/cu.SLAB_USBtoUART'  # ブルーボードのポート
```

ポートの確認：

```bash
ls /dev/cu.*
```

---

## アクセシビリティ権限

「システム設定」→「プライバシーとセキュリティ」→「アクセシビリティ」で以下をオンにする：

- ターミナル
- python

---

## 起動方法

### 手動起動

```bash
open ~/schoomy-plaud-trigger/
```

Finderで `start_trigger.command` をダブルクリック。

### Mac起動時に自動起動

「システム設定」→「一般」→「ログイン項目」→ `+` で `start_trigger.command` を追加。

---

## 更新履歴

| 日付 | 変更内容 |
|------|----------|
| 2026-04 | 初期リリース（スイッチで録音開始・停止） |
