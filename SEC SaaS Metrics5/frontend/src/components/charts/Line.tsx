import { ResponsiveLine } from "@nivo/line";
import { RiskData } from "../../types/data";

const Line = ({ data }: { data: RiskData[] }) => (
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

export default Line;
