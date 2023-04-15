import { HeatMapCanvas } from "@nivo/heatmap";
import { MDAGraphData } from "../../types/data";

const Heatmap = ({ data }: { data: MDAGraphData[] }) => (
  <HeatMapCanvas
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
      legendOffset: 60
    }}
    axisRight={{
      tickSize: 10,
      tickPadding: 5,
      tickRotation: -15,
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
        anchor: "left",
        translateX: -50,
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
        titleAlign: "start",
        titleOffset: 4
      }
    ]}
    annotations={[]}
  />
);

export default Heatmap;
