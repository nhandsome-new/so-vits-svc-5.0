## Original Code 解析
### Preprocess data
#### Timbre
- Model for Speaker Embedding
    - いらない：Speaker EmbeddingはX -Vecgtorでとってくる
- speaker folder 
    - *.spk.npy
#### Whisper
- Model for Phoneme?
    - 使ってみようかな。。。
#### hubert soft model
- Model for Content
    - いらない：すでにHubert jpを使ったzcontent Vectorがある
#### Crepe 
- Model for Pitch(F0)
    - 使ってみようかな
#### Pretrain model
- Model for so-vits-5
    - 使ってみたいけど。。できるかな？
#### 結論
- いらない：Timbre / Hubert 
- すぐにはいらない：Whisper / Crepe
    - Whisper : 精度向上に効果があるかも
    - Crepe : 現在Pitchデータがあってなさそうだったら

### 確認すること
#### 22050に変えたとき変更するもの
- 
