import { ResponsiveLine } from "@nivo/line";
import axios from "axios";
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import styled from "styled-components";
import { ChartContainer } from "../styles/chart";
import { RiskData } from "../types/data";
import { BACKEND_URL } from "../utils/constants";
import Line from "./charts/Line";

const ChartWrapper = styled(ChartContainer)`
  height: 75vh;
  width: 95%;
  margin: 1rem;
  text-align: center;
  position: relative;
`;

const Description = styled.div`
  margin: 2rem 3rem;
`;

const MyResponsiveLine = ({ data }: { data: RiskData[] }) => (
  <ResponsiveLine
    data={data}
    theme={{ fontSize: 16 }}
    margin={{ top: 50, right: 160, bottom: 50, left: 60 }}
    xScale={{ type: "point" }}
    yScale={{ type: "linear", stacked: false, min: 0, max: 15 }}
    yFormat=" >-.2f"
    curve="monotoneX"
    axisTop={{
      tickValues: "every 1 year",
      tickSize: 5,
      tickPadding: 10,
      tickRotation: 0,
      legend: "Year",
      legendOffset: -40,
      legendPosition: "middle"
    }}
    axisBottom={null}
    axisLeft={{
      tickValues: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
      tickSize: 5,
      tickPadding: 10,
      tickRotation: 0,
      format: ".2s",
      legend: "Risk Sentiment",
      legendOffset: -50,
      legendPosition: "middle"
    }}
    enableGridX={false}
    colors={(d) => d.color}
    lineWidth={2}
    pointSize={10}
    pointColor={{ theme: "background" }}
    pointBorderWidth={2}
    pointBorderColor={{ from: "serieColor" }}
    pointLabelYOffset={-12}
    useMesh={true}
    gridYValues={[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]}
    legends={[
      {
        anchor: "top-right",
        direction: "column",
        justify: false,
        translateX: 140,
        translateY: 0,
        itemsSpacing: 2,
        itemDirection: "left-to-right",
        itemWidth: 100,
        itemHeight: 20,
        itemOpacity: 1,
        symbolSize: 15,
        symbolShape: "circle",
        symbolBorderColor: "rgba(0, 0, 0, .5)",
        effects: [
          {
            on: "hover",
            style: {
              itemBackground: "rgba(0, 0, 0, .03)",
              itemOpacity: 1
            }
          }
        ]
      }
    ]}
  />
);

export default function CompanyRisk() {
  let params = useParams();

  const [riskData, setRiskData] = useState<RiskData[]>([]);

  useEffect(() => {
    axios
      .get(`${BACKEND_URL}/risk_metric?cik=${params.id}`)
      .then((response) => {
        const tempRiskData: RiskData[] = [
          {
            id: "Financial",
            data: [],
            color: "#12364D"
          },
          {
            id: "Idiosyncratics",
            data: [],
            color: "#2E719E"
          },
          {
            id: "Legal",
            data: [],
            color: "#44A1DF"
          },
          {
            id: "Tax",
            data: [],
            color: "#78BBE6"
          },
          {
            id: "Systematic",
            data: [],
            color: "#83CAF8"
          }
        ];
        for (var i = 0; i < response.data.Year.length; i++) {
          tempRiskData[0].data.push({
            x: response.data.Year[i],
            y: response.data.Financial[i]
          });
          tempRiskData[1].data.push({
            x: response.data.Year[i],
            y: response.data.Idiosyncratics[i]
          });
          tempRiskData[2].data.push({
            x: response.data.Year[i],
            y: response.data.Legal[i]
          });
          tempRiskData[3].data.push({
            x: response.data.Year[i],
            y: response.data.Tax[i]
          });
          tempRiskData[4].data.push({
            x: response.data.Year[i],
            y: response.data.Systematic[i]
          });
        }
        setRiskData(tempRiskData);
      })
      .catch((error) => console.log(error));
  }, []);

  const theme = {
    axis: {
      textColor: "#eee",
      fontSize: "14px",
      tickColor: "#eee"
    },
    grid: {
      stroke: "#888",
      strokeWidth: 1
    }
  };

  return (
    <div>
      <Description>
        Which sections are used?
        <br/>
        The text from the 10-K filings are processed to generate appropriate counting measures that objectively quantify firms risk disclosures
        <br/><br/>
        Approach:
        <br/>
        A list of keywords indicative of risks has been identified from prior literature and document clustering approaches like Latent Dirichlet Allocation (LDA).  These keywords have been then classified into five subcategories
        <br/>
        Financial Risk
        <br/>
        Litigation Risk
        <br/>
        Tax Risk 
        <br/>
        Systematic Risk
        <br/> 
        Idiosyncratic Risk
        <br/><br/>
        To quantify the risk term frequencies (natural logarithm of the count of the words) have been calculated on a year over year basis. The results are plotted and this process is repeated for all five categories of risks. A spike in the plots for multiple risk categories can be investigated further for any ambiguous behavior or fraud by the company.

      </Description>
      <ChartWrapper>
        <MyResponsiveLine data={riskData}></MyResponsiveLine>
      </ChartWrapper>
    </div>
  );
}
