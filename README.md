國立臺灣大學學生會簡明法規彙編
==============================

產生方便閱讀版本的[國立臺灣大學學生會法規彙編](https://github.com/ntu-student-congress/tortue)。

這支程式能夠解析純文字格式的法規與學生法院解釋，轉換成文件物件模型 (DOM) 後，再以不同的格式輸出。
支援的格式除了 Markdown 以外，也能藉由 [CSS3 分頁媒體模組](https://www.w3.org/TR/css3-page/)
產生即可列印 (print-ready) 的 HTML 文件。

---

Generates an easier-reading version of [Code of NTU Student Association](https://github.com/ntu-student-congress/tortue).

This application parses acts and Student Judiciary interpretations in plain-text
format, converts them into Document Object Model, and renders them in different
formats respectively. Apart from Markdown, print-ready HTML documents are also
supported through the [CSS3 Paged Media Module](https://www.w3.org/TR/css3-page/) technique.

系統需求 / Prerequisite
-----------------------

[Python 3.4+](https://www.python.org/downloads/)

由於 CSS `@page` 與 `list-style: cjk-decimal` 各瀏覽器支援還未標準化，因此目前暫時使用
[Prince](http://princexml.com/) 作為產生 PDF 的排版軟體。在支援部份功能的瀏覽器裡（例如
Firefox 52+ 或是 Chrome 56+）直接選擇 [列印] 應已能看到頁面或項目符號之效果。

程式碼授權 / License
--------------------

[GNU 通用公眾授權，第三版](LICENSE.md)。
