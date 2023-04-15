import { ResponsiveBarCanvas } from "@nivo/bar";

export const SharePriceBarCanvas = ({ data }: { data: any[] }) => (
  <ResponsiveBarCanvas
    theme={{ fontSize: 16 }}
    data={data}
    keys={["10-K", "10-Q", "8-K", "regular"]}
    indexBy="date"
    margin={{ top: 50, right: 1, bottom: 50, left: 60 }}
    pixelRatio={1}
    padding={0.15}
    innerPadding={0}
    minValue="auto"
    maxValue="auto"
    groupMode="stacked"
    layout="vertical"
    reverse={false}
    valueScale={{ type: "linear" }}
    indexScale={{ type: "band", round: true }}
    colors={({ id, data }) => String(data[`color`])}
    borderWidth={0}
    borderRadius={0}
    borderColor={{
      from: "color",
      modifiers: [["darker", 1.6]]
    }}
    axisBottom={{
      tickSize: 5,
      tickPadding: 5,
      tickRotation: 0,
      legend: "Date",
      legendPosition: "middle",
      legendOffset: 36,
      format: () => ""
    }}
    axisLeft={{
      tickSize: 5,
      tickPadding: 5,
      tickRotation: 0,
      legend: "Price ($)",
      legendPosition: "middle",
      legendOffset: -50
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
  />
);
