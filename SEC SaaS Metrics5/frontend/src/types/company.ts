export type Metadata = {
  cik: string | undefined;
  name: string;
  category: string;
  overview: string;
  ticker: string;

};

export type SidebarOption = {
  name: String;
  icon: string;
  link: string;
};

export type KPICardDetail = {
  name: string;
  value: number;
  isPrevAvailable: boolean;
  
  valuePrev: number;
};

export type Finance = {
  year: string;
  data: {
    tablename: string;
    table_data: string;
  }[];
}[];

export type MDAData = {
  index: number;
  item: string;
  filing_date: string;
  positive: number[][];
  negative: number[][];
  text: string;
};

export type SpreadsheetData = {
  tag: string;
  company: number;
  value: string;
  decimel: string;
  unit: string;
  form_type: string;
  accession_no: string;
  start_date: string;
  end_date: string;
  filling_date: string;
  source: string;
};

export type OwnershipData = {
  Holder: string;
  Shares: string;
  "Date Reported": string;
  "% out": string;
  Value: string;
};
