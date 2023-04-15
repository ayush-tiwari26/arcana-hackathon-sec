import axios from "axios";
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import styled from "styled-components";
import { Filters, useSearchContext } from "../hooks/useSearchContext";
import { ChartContainer } from "../styles/chart";
import { SharePriceGraphData } from "../types/data";
import { BACKEND_URL } from "../utils/constants";
import { formatNumber } from "../utils/helpers";
import { SharePriceBarCanvas } from "./charts/SharePriceBar";

const ChartWrapper = styled(ChartContainer)`
  height: 75vh;
  width: 95%;
  margin: 1rem;
  text-align: center;
  position: relative;
`;

const LegendList = styled.div`
  display: flex;
  flex-direction: column;
  position: absolute;
  top: 2rem;
  right: 2.5rem;
  text-align: left;
`;

const Legend = styled.div`
  display: flex;
  align-items: center;
`;

const Icon = styled.div`
  width: 20px;
  height: 20px;
  border-radius: 2px;
  background-color: ${(props) => props.color};
  margin-right: 5px;
`;

const legends = [
  {
    name: "10-K",
    color: "orange"
  },
  {
    name: "10-Q",
    color: "green"
  },
  {
    name: "8-Q",
    color: "black"
  }
];

const formatDate = (value: string) => {
  const options: Intl.DateTimeFormatOptions = { year: "numeric", month: "long", day: "numeric" };
  return new Date(value).toLocaleDateString(undefined, options);
};

const dateFilter = (date: any, dates: Filters) => {
  const objDate = new Date(date);
  const startDate = new Date(dates.startDate);
  const endDate = new Date(dates.endDate);
  return objDate >= startDate && objDate <= endDate;
};

export default function CompanySharePrice() {
  let params = useParams();
  let searchContext = useSearchContext();

  const [sharePriceData, setSharePriceData] = useState<SharePriceGraphData[]>([]);
  const [rawData, setRawData] = useState<any>();

  useEffect(() => {
    axios
      .get(`${BACKEND_URL}/share_price?cik=${params.id}`)
      .then((response) => {
        setRawData(response.data);
      })
      .catch((error) => console.log(error));
  }, []);

  useEffect(() => {
    const length = rawData ? rawData.date_list.length : 0;
    const sharePriceGraphData: SharePriceGraphData[] = [];
    for (var i = 0; i < length; i++) {
      if (!dateFilter(rawData.date_list[i], searchContext.filters)) continue;
      if (rawData.category[i] === "10-K") {
        sharePriceGraphData.push({
          date: formatDate(rawData.date_list[i]),
          "10-K": formatNumber(rawData.price_list[i]),
          color: "orange"
        });
      } else if (rawData.category[i] === "10-Q") {
        sharePriceGraphData.push({
          date: formatDate(rawData.date_list[i]),
          "10-Q": formatNumber(rawData.price_list[i]),
          color: "green"
        });
      } else if (rawData.category[i] === "8-K") {
        sharePriceGraphData.push({
          date: formatDate(rawData.date_list[i]),
          "8-K": formatNumber(rawData.price_list[i]),
          color: "black"
        });
      } else {
        sharePriceGraphData.push({
          date: formatDate(rawData.date_list[i]),
          regular: formatNumber(rawData.price_list[i]),
          color: "#83CAF8"
        });
      }
    }
    setSharePriceData(sharePriceGraphData);
  }, [rawData, searchContext.filters]);

  return (
    <ChartWrapper>
      Each SEC filing is stacked against company’s closing share price 

      {
        (sharePriceData.length !== 0) ? (
          <SharePriceBarCanvas data={sharePriceData} />
        )
        : (
          <div>Loading graph.....</div>
        )
      }
      <LegendList>
        <strong>Legend:</strong>
        <br />
        {legends.map((legend) => {
          return (
            <Legend>
              <Icon color={legend.color}></Icon>
              <div>{legend.name}</div>
            </Legend>
          );
        })}
      </LegendList>
    </ChartWrapper>
  );
}
