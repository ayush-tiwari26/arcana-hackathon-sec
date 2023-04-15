import { Column } from "react-table";
import { MDAData, SpreadsheetData } from "./company";

export type Data = SpreadsheetData[] | MDAData[];

export type Columns = {
  Header: string;
  accessor: string;
}[];

export type TableProps = {
  data: Data;
  columns: Column<SpreadsheetData>[] | Column<MDAData>[];
};
