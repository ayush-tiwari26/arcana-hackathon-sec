import { ResponsiveBarCanvas } from "@nivo/bar";
import styled from "styled-components";
import { formatNumber } from "../../utils/helpers";

// make sure parent container have a defined height when using
// responsive component, otherwise height will be 0 and
// no chart will be rendered.
// website examples showcase many properties,
// you'll often use just a few of them.

const Tooltip = styled.div`
  font-size: 1.2rem;
  background-color: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(2px);
  padding: 0.4rem 0.8rem;
  border-radius: 5px;
`;

// TODO: added types to data
export default function BarCanvas({ data, keys, indexBy }: { data: any[]; keys?: string[]; indexBy: string }) {
  return (
    <ResponsiveBarCanvas
      theme={{ fontSize: 15 }}
      data={data}
      keys={keys}
      indexBy={indexBy}
      margin={{ top: 50, right: 60, bottom: 50, left: 60 }}
      pixelRatio={1}
      padding={0.15}
      innerPadding={0}
      minValue="auto"
      maxValue="auto"
      groupMode="grouped"
      layout="vertical"
      reverse={false}
      valueScale={{ type: "linear" }}
      indexScale={{ type: "band", round: true }}
      colors={["#3785B9", "#44A1DF", "#78BBE6", "#83CAF8", "#C5DBFC", "#D8E7FE", "#F1F7F8"]}
      borderWidth={0}
      borderRadius={10}
      axisTop={{
        tickSize: 2,
        tickPadding: 5,
        tickRotation: -45
      }}
      axisLeft={{
        tickSize: 5,
        tickPadding: 5,
        tickRotation: 0,
        format: (value) => formatNumber(value)
      }}
      axisBottom={{
        tickSize: 0,
        tickPadding: 5,
        tickRotation: 0,
        legendPosition: "middle",
        legendOffset: 40,
        format: () => ""
      }}
      enableGridX={false}
      enableGridY={false}
      enableLabel={false}
      labelSkipWidth={12}
      labelSkipHeight={12}
      labelTextColor={{
        from: "color",
        modifiers: [["darker", 1.6]]
      }}
      isInteractive={true}
      tooltip={(input) => {
        return (
          <div>
            {input.data.source === "text" ? (
              <Tooltip>
                <strong>Source: </strong>
                text
                <br />
                <strong>Filing Date: </strong>
                {input.indexValue}
                <br />
                <strong>Value: </strong>
                {input.formattedValue}
                <br />
                <strong>Confidence Score: </strong>
                {typeof input.data.score === "string"
                  ? formatNumber(parseInt(input.data.score))
                  : formatNumber(input.data.score)}
                <br />
                <strong>Sentence: </strong>
                {input.data.sentence}
              </Tooltip>
            ) : (
              <Tooltip>
                <strong>Filing Date: </strong>
                {input.indexValue}
                <br />
                <strong>Value: </strong>
                {input.formattedValue}
              </Tooltip>
            )}
          </div>
        );
      }}
      // legends={[
      //   {
      //     dataFrom: "keys",
      //     anchor: "top-right",
      //     direction: "column",
      //     justify: false,
      //     translateX: 90,
      //     translateY: 0,
      //     itemsSpacing: 2,
      //     itemWidth: 100,
      //     itemHeight: 20,
      //     itemDirection: "left-to-right",
      //     itemOpacity: 0.85,
      //     symbolSize: 20,
      //     effects: [
      //       {
      //         on: "hover",
      //         style: {
      //           itemOpacity: 1
      //         }
      //       }
      //     ]
      //   }
      // ]}
    />
  );
}
