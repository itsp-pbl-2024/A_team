<img width="1295" alt="image" src="https://github.com/user-attachments/assets/6f48677f-76e0-4bce-9212-c40ffe8b07ff">

![mv](https://github.com/user-attachments/assets/92982bd6-7de1-4bf3-9909-e0b782ee6e28)


# Meeting Maestro
Meeting Maestroは、会議参加者の発言量を可視化することで司会者の仕事をサポートするアプリケーションです。
Meeting Maestroでは以下の機能が提供されます。
- 発話ダイアライゼーションを使って自動で参加者の発言量をリアルタイムに可視化
- 最も発言量の少ない参加者を自動で検出
- 会議中に使用できるメモ機能やタイマー機能
[発表資料はこちらにあります。](https://docs.google.com/presentation/d/1nCsjjXkjdqz1Ndz6ZDLcE9_wWaB64gxSbdSgVm7BTLk/edit?usp=sharing)

# 動かし方
```bash
python3 backend/server.py
python3 interface/main.py
```

# 注意点
発話ダイアライゼーションに使用しているライブラリやモデルの都合上、雑音が多い環境や複数人が同時に話す環境での発話量のカウントが難しいです。
そう言う場合は、Meeting Maestroのマニュアル記録モードを用いることで発言量を手動で記録し、可視化することができます。

# デモ動画
[デモ動画はこちらにあります。](https://drive.google.com/file/d/1nISVwaqCVOp8dku06WlJtqgmqzTELS-S/view)
