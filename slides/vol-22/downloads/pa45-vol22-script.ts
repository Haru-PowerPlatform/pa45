/**
 * PA45 第22回 デモ用 Officeスクリプト「経費の集計」
 * ------------------------------------------------------------
 * やること：
 *   ① 表「ExpenseTable」の見出し行に色をつける（緑＋白字・太字）
 *   ② 「Amount」列の合計を計算する
 *   ③ 表の2つ下に「経費 合計」と数値を書き出す
 *   ④ 合計を "戻り値" として返す（← Power Automate の Teams通知で使う）
 *
 * 使い方：Excel（ブラウザ版）→「自動化」タブ →「新しいスクリプト」→
 *         このコードを貼り付け →「経費の集計」という名前で保存。
 *
 * ※ 講座では M365 Copilot にスクリプトを書かせる流れを見せます。
 *   Copilotの結果が動かない時の "お守り" が、この完成版です。
 */
function main(workbook: ExcelScript.Workbook): number {
  // 表「ExpenseTable」を取得（無ければ最初の表）
  let table = workbook.getTable("ExpenseTable");
  if (!table) {
    table = workbook.getTables()[0];
  }

  // ① 見出し行に色をつける
  const header = table.getHeaderRowRange();
  header.getFormat().getFill().setColor("#217346"); // Excelグリーン
  const headerFont = header.getFormat().getFont();
  headerFont.setColor("#FFFFFF");
  headerFont.setBold(true);

  // ②「Amount」列の合計を計算
  const headerValues = header.getValues()[0].map(v => String(v));
  const amountIndex = headerValues.indexOf("Amount");
  const bodyValues = table.getRangeBetweenHeaderAndTotal().getValues();
  let sum = 0;
  for (const row of bodyValues) {
    const n = Number(row[amountIndex]);
    if (!isNaN(n)) {
      sum += n;
    }
  }

  // ③ 表の2つ下に「経費 合計」＋数値を書き出す
  const below = table.getRange().getLastRow().getOffsetRange(2, 0);
  below.getCell(0, 0).setValue("経費 合計");
  const totalCell = below.getCell(0, 1);
  totalCell.setValue(sum);
  totalCell.getFormat().getFont().setBold(true);
  totalCell.getFormat().getFill().setColor("#FFF7ED");

  // ④ 合計を返す（Teams通知の本文で @{...['result']} として使える）
  return sum;
}
