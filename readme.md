# これはなに？
danbooru　wikiに登録されているタグ（いわゆるdanbooru語）とe621 wikiに登録されているタグ(e621語)の相互変換を行うツールです。

インデックスタグとエイリアスタグをdanbooru,e621それぞれの辞書間で突合させることで機能を実現しています。

ユーザー辞書による任意の組み合わせにも対応しています。

# 起動方法
guiフォルダ下のgui.exeをダブルクリックで起動できます。  
python3.10以降の実行環境がある方はgui.pyから直接起動したほうが若干早いかも？

## gui.pyの制作環境
python 3.10.6  
pandas 2.2.2  
にて作成。ご自身の環境にpandas導入すれば多分動くはず。

# 基本的な使い方
![default.jpg](screenshot%2Fdefault.jpg)

danbooru語のタグを上の検索タグのボックス（以下danbooruフレームの検索ボックス）に貼り付けて、↓ Search e621ボタンを押すとe621語の対応するタグが得られます。

同様に、e621語のタグを下の検索ボックス（以下e621フレームの検索ボックス）に入力して、↑ Search danbooruボタンをクリックすることでdanbooruタグが得られます。

All Clearボタンを押すことで初期状態に戻します。danbooruフレームで検索してe621から検索する場合など、フレームをまたいで検索する場合もクリアを行ってください。

# 表示結果の詳細
## index or aliases
検索したタグがIndexタグか、Aliasesタグかを表示します。Index,Aliasesについては下の項目をご一読下さい。  
また、検索したタグがユーザー辞書に該当するかどうかのメッセージも表示します。

## jp tag
タグの日本語訳を表示します。

## post count
wikiでの投稿数を表示します。最新の数字ではないため目安程度に。

## link
wikiのタグページのリンクを表示します。クリックで移動も可能。

## jptagによる検索結果
基本の突合、ユーザー辞書による突合いずれも合致する結果が得られなかった場合、機械翻訳のjp tagによる突合を行います。
試験的に実装した機能のため、正確性が劣ることが考えられます。

![pervert.jpg](screenshot%2Fpervert.jpg)

# Index と Aliasesについて
danbooru,e621どちらも、IndexタグとAliasesタグというものが存在します。

danbooruの例  
index:1girl  
aliases:1girls,sole_female  

一つの状況（この場合、1人の女の子が表示されてる）を表すのにいくつかの表現が該当する場合があります。  
このいくつかの表現のうち、1個のタグを代表として、ほか全てのタグを言い換え表現として記載することで、danbooru,e621 wikiは記述の重複などを防いでいます。

当ツールでは代表となるタグをIndex(タグ)、言い換え表現としてまとめられているものをAliases（タグ）と便宜的に呼んでいます。

danbooru wiki と e621 wiki　それぞれでどの単語をIndexとし、何をAliasesとするかが異なるため、（日本語から見ると）同じ意味の単語が異なる表現でdanbooru,e621に登録されている場合があります。

当ツールでは入力されたタグからIndex,Aliasesを生成し、対となる辞書のIndex,Aliasesと突合することでdanbooru e621間の変換を行っています。

例:danbooru語ではfutanariがe621ではintersexと表示される

![moshikizu.jpg](screenshot%2Fmoshikizu.jpg)


# ユーザー辞書
userdict.csvを編集することで、検索結果を変更することができます。
![userdict.jpg](screenshot%2Fuserdict.jpg)
## ケース１：タグ同士のつながりを再定義する
danbooru_tagu,e621_tag,jp_tag　それぞれの項目に要素を入力することで検索結果を変更することができます。
上記画像ではdanbooru側で1girlを検索した際、e621の結果をsoloに書き換えています。

## ケース２：jptagを修正する
danbooru_tag,e621_tagのいずれか1つとjp_tagを入力することで、検索結果で表示されるjptagを変更できます。
上記画像ではfutanariのjptagをフタナリに修正しています。

## ケース３多対多対応の表記
danbooru_tag,e621_tag,jp_tagは""（ダブルクオーテーション）で囲むことで複数の要素を記述することができます。  
これを利用することでdanbooruではAとしか表現されていないものが、e621ではB1,B2,B3のように表現されている、といった状態を記述できます。

現状作者の技術力不足により各要素数が異なる場合、エラーとなります。強制終了などは起こさないと思いますが、多対多でユーザー辞書に記述する際はdanbooru_tag,e621_tag,jp_tagの要素数を同じにすることをオススメします。

![testcase.jpg](screenshot%2Ftestcase.jpg)

# Libraries usage
### pandas  
BSD 3-Clause License

Copyright (c) 2008-2011, AQR Capital Management, LLC, Lambda Foundry, Inc. and PyData Development Team
All rights reserved.

Copyright (c) 2011-2023, Open source contributors.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

### booru-japanese-tag  
https://github.com/boorutan/booru-japanese-tag  

danbooru-machine-jp.csv,danbooru-only-machine-jp.csv,danbooru-jp.csvを利用させていただきました。感謝。

MIT license  
https://github.com/boorutan/booru-japanese-tag/blob/main/LICENSE

### a1111-sd-webui-tagcomplete  

https://github.com/DominikDoom/a1111-sd-webui-tagcomplete

danbooru.csv,e621.csvを利用させていただきました。感謝。  

MIT License  
https://github.com/DominikDoom/a1111-sd-webui-tagcomplete/blob/main/LICENSE
