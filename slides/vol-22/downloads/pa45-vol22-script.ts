/**
 * PA45 第22回 デモ用 Officeスクリプト「満足度の集計」
 * ------------------------------------------------------------
 * やること：
 *   ① 表「アンケート」の見出し行に色をつける（緑＋白字・太字）
 *   ② 「満足度」列の平均を計算する
 *   ③ 表の2つ下に「平均 満足度」と数値を書き出す
 *   ④ 平均値を "戻り値" として返す（← Power Automate の Teams通知で使う）
 *
 * 使い方：Excel（ブラウザ版）→「自動化」タブ →「新しいスクリプト」→
 *         このコードを貼り付け →「満足度の集計」という名前で保存。
 *
 * ※ 講座では「操作を記録」で作る流れを見せます。フローに組み込む時だけ、
 *   平均を "返す" 必要があるので、この完成版を使います。
 */
function main(workbook: ExcelScript.Workbook): number {
  // 表「アンケート」を取得（無ければ最初の表）
  let table = workbook.getTable("アンケート");
  if (!table) {
    table = workbook.getTables()[0];
  }

  // ① 見出し行に色をつける
  const header = table.getHeaderRowRange();
  header.getFormat().getFill().setColor("#217346"); // Excelグリーン
  const headerFont = header.getFormat().getFont();
  headerFont.setColor("#FFFFFF");
  headerFont.setBold(true);

  // ②「満足度」列の平均を計算
  const headerValues = header.getValues()[0].map(v => String(v));
  const satIndex = headerValues.indexOf("満足度");
  const bodyValues = table.getRangeBetweenHeaderAndTotal().getValues();
  let sum = 0;
  let count = 0;
  for (const row of bodyValues) {
    const n = Number(row[satIndex]);
    if (!isNaN(n)) {
      sum += n;
      count++;
    }
  }
  const average = count > 0 ? Math.round((sum / count) * 10) / 10 : 0;

  // ③ 表の2つ下に「平均 満足度」＋数値を書き出す
  const below = table.getRange().getLastRow().getOffsetRange(2, 0);
  below.getCell(0, 0).setValue("平均 満足度");
  const avgCell = below.getCell(0, 1);
  avgCell.setValue(average);
  avgCell.getFormat().getFont().setBold(true);
  avgCell.getFormat().getFill().setColor("#FFF7ED");

  // ④ 平均値を返す（Teams通知の本文で @{...['result']} として使える）
  return average;
}
