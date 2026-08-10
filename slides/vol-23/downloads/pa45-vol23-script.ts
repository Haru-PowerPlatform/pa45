/**
 * PA45 第23回｜経費の合計を計算して「答え（合計）」を返すOfficeスクリプト
 * ------------------------------------------------------------------
 * ・ExpenseTable の Amount 列を合計する
 * ・見出しを緑、合計セルを黄色に整形（見た目の確認用）
 * ・合計を数値で return する ← ここが今日の肝。
 *   Power Automate の「スクリプトの実行」がこの戻り値(result)を受け取り、
 *   「条件」で 50000 より大きいか判定して行き先を振り分ける。
 */
function main(workbook: ExcelScript.Workbook): number {
  const sheet = workbook.getActiveWorksheet();
  const table = workbook.getTable("ExpenseTable");

  // Amount 列の位置を見出しから探す
  const header = table.getHeaderRowRange().getValues()[0] as string[];
  const amountIndex = header.indexOf("Amount");

  // 本文（データ行）の値を取り出して合計
  const body = table.getRangeBetweenHeaderAndTotal().getValues();
  let sum = 0;
  for (const row of body) {
    sum += Number(row[amountIndex]);
  }

  // 見出しを緑＋白太字に整形
  const headerRange = table.getHeaderRowRange();
  headerRange.getFormat().getFill().setColor("217346");
  const hf = headerRange.getFormat().getFont();
  hf.setColor("FFFFFF");
  hf.setBold(true);

  // 表の2つ下に「合計」ラベルと金額を書き出し（人が見て確認するため）
  const lastRow = table.getRange().getLastRow().getRowIndex(); // 0基点
  const labelCell = sheet.getCell(lastRow + 2, 0);
  labelCell.setValue("合計 Amount");
  labelCell.getFormat().getFont().setBold(true);
  const valueCell = sheet.getCell(lastRow + 2, 1);
  valueCell.setValue(sum);
  valueCell.getFormat().getFill().setColor("FFF3CD"); // 黄色
  valueCell.getFormat().getFont().setBold(true);

  // 合計を返す（フローの result になる）
  return sum;
}
