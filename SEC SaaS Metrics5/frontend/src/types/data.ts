export type RiskData = {
  id: string;
  color: string;
  data: {
    x: string;
    y: number;
  }[];
};

export type SharePriceGraphData = {
  date: string;
  "10-K"?: string;
  "10-Q"?: string;
  "8-K"?: string;
  regular?: string;
  color?: string;
};

export type MDAGraphData = {
  id: string;
  data: {
    x: string;
    y: number;
  }[];
};
