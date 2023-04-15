import { HeatMapCanvas } from "@nivo/heatmap";
import axios from "axios";
import { useEffect, useMemo, useState } from "react";
import { useParams } from "react-router-dom";
import { Column } from "react-table";
import styled from "styled-components";
import { MDAData } from "../types/company";
import { BACKEND_URL } from "../utils/constants";
import SentimentViewer from "./sentimentViewer";
import TableComponent from "./table";

type MDAGraphData = {
  id: string;
  data: {
    x: string;
    y: number;
  }[];
};

const GraphWrapper = styled.div`
  height: 80vh;
  display: flex;
  justify-content: center;
`;

const ButtonGroup = styled.div.attrs((props) => ({
  className: props.className
}))`
  display: flex;
  align-items: center;
  margin: 2rem;

  & .active {
    background-color: #fdb44b;
  }
`;

const ModeButton = styled.button`
  outline: none;
  margin: none;
  font-size: 1.5rem;
  margin: 0 1rem;
  padding: 0.8rem 1.2rem;
  border-radius: 10px;
  border: none;
`;

const Description = styled.div`
  margin: 2rem 3rem;
`;

const MyHeatMapCanvas = ({ data }: { data: MDAGraphData[] }) => (
  <HeatMapCanvas
    theme={{ fontSize: 15 }}
    height={2500}
    width={1500}
    data={data}
    margin={{ top: 70, right: 80, bottom: 20, left: 80 }}
    valueFormat=">-.2s"
    xInnerPadding={0.01}
    yInnerPadding={0.01}
    pixelRatio={2}
    axisTop={{
      tickSize: 5,
      tickPadding: 5,
      tickRotation: -90,
      legend: "years",
      legendPosition: "middle",
      legendOffset: -40
    }}
    axisRight={{
      tickSize: 0,
      tickPadding: 5,
      tickRotation: 0,
      legend: "words",
      legendPosition: "middle",
      legendOffset: 75
    }}
    axisLeft={null}
    colors={{
      type: "quantize",
      scheme: "blues",
      steps: 50,
      minValue: -100,
      maxValue: 100
    }}
    emptyColor="#555555"
    borderColor="#000000"
    enableLabels={false}
    legends={[
      {
        anchor: "top-left",
        translateX: -60,
        translateY: 0,
        length: 600,
        thickness: 10,
        direction: "column",
        tickPosition: "after",
        tickSize: 10,
        tickSpacing: 10,
        tickOverlap: false,
        tickFormat: ">-.2s",
        title: "Value →",
        titleAlign: "middle",
        titleOffset: 4
      }
    ]}
    annotations={[]}
  />
);

export default function CompanyMDA() {
  const [mode, setMode] = useState<"analysis" | "heatmap">("heatmap");
  const [mdaData, setMdaData] = useState<MDAData[]>([]);
  const [heatMapData, setHeatMapData] = useState<any[]>([]);
  const [sentimentIndex, setSentimentIndex] = useState<number>(-1);

  let params = useParams();

  useEffect(() => {
    axios
      .get(`${BACKEND_URL}/sentiment?cik=${params.id}`)
      .then((response) => {
        const tempData: MDAData[] = [];
        for (var i = 0; i < response.data.item.length; i++) {
          tempData.push({
            index: i,
            item: response.data.item[i],
            filing_date: response.data.filing_date[i],
            positive: JSON.parse(response.data.positive[i]),
            negative: JSON.parse(response.data.negative[i]),
            text: response.data.text[i]
          });
        }
        setMdaData(tempData);
      })
      .catch((error) => console.log(error));

    axios
      .get(`${BACKEND_URL}/heat_map?cik=${params.id}`)
      .then((response) => setHeatMapData(response.data))
      .catch((error) => console.log(error));
  }, []);

  const data = useMemo(() => [...mdaData], [mdaData]);

  const columns: Column<MDAData>[] = useMemo(
    () => [
      {
        Header: "Item",
        accessor: "item"
      },
      {
        Header: "Filing Date",
        accessor: "filing_date"
      },
      {
        Header: "Sentiment",
        accessor: "index",
        Cell: ({ cell: { value } }) => (
          <button className="button" onClick={() => setSentimentIndex(value)}>
            View Sentiment
          </button>
        )
      }
    ],
    []
  );

  return (
    <div>
      <ButtonGroup>
        <ModeButton className={`${mode === "analysis" ? "active" : ""}`} onClick={() => setMode("analysis")}>
          Sentiment Analysis
        </ModeButton>
        <ModeButton className={`${mode === "heatmap" ? "active" : ""}`} onClick={() => setMode("heatmap")}>
          Heatmap
        </ModeButton>
      </ButtonGroup>
      {mode === "heatmap" ? (
        <Description>
          The “MD&A” uses a “heat map” visualization of sort-able keywords. Also, hovering-over a block for a particular filing or amendment reveals the actual number of times that word was used. With this users can identify how the management’s focus has changed over years
        </Description>)
        : (
        <Description>
          It predicts the behavior and possible trend of stock markets by analyzing the sentiment the different sections of the SEC filings. 
          <br/><br/>
          In the document red highlight shows negative sentiment while green highlight shows positive sentiment
          <br/><br/>
          Item 7 : Management's Discussion and Analysis of Financial Condition and Results of Operations
          <br/>
          Item 7A : Quantitative and Qualitative Disclosures about Market Risks
          <br/>
          Item 8 : Financial Statements
          <br/>
          Item 9 : Changes in and Disagreements With Accountants on Accounting and Financial Disclosure
          <br/>
          Item 9A : Controls and Procedures
          <br/>
          Item 9B : Other Information
        </Description>
        )
      }
      {mode === "heatmap" ? (
        heatMapData.length !== 0 ? (
          <GraphWrapper>
            <MyHeatMapCanvas data={heatMapData}></MyHeatMapCanvas>
          </GraphWrapper>
        ) : (
          <div>Loading heatmap.....</div>
        )
      ) : (
        <div>
          {sentimentIndex >= 0 && (
            <SentimentViewer close={() => setSentimentIndex(-1)} data={mdaData[sentimentIndex]} />
          )}
          <TableComponent data={data} columns={columns} />
        </div>
      )}
    </div>
  );
}
