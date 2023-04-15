import { Bar } from "@nivo/bar";
import axios from "axios";
import { useEffect, useState } from "react";
import styled from "styled-components";
import { isMetaProperty } from "typescript";
import BarCanvas from "../components/charts/Bar";
import Search from "../components/Search";
import Sidebar from "../components/Sidebar";
import { Company, useSearchContext } from "../hooks/useSearchContext";
import { ChartContainer } from "../styles/chart";
import { BACKEND_URL } from "../utils/constants";
import Select from "react-select";
import BenchmarkBarCanvas from "../components/charts/BenchmarkBar";
import { Label } from "../styles/form";

type option = {
  value: string;
  label: string;
};

const ChartWrapper = styled(ChartContainer)`
  height: 800px;
  width: 800px;
  margin-left: 2rem;
`;

const StyledBenchmarking = styled.div`
  display: flex;
  height: 100vh;
`;

const VerticalContainer = styled.div`
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100vh;
`;

const DatasetContainer = styled.div`
  display: flex;
  flex-direction: column;
  width: 250px;
  margin: 2rem;
`;

const getOptionIndex = (options: option[], selectedOption: option | null) => {
  if (selectedOption === null) return -1;
  for (var i = 0; i < options.length; i++) {
    if (options[i].value === selectedOption.value) return i;
  }
  return -1;
};

export default function Benchmarking() {
  const [data, setData] = useState<any[]>([]);
  const [dataSet, setDataSet] = useState<option[]>([]);
  const [activeDataSet, setActiveDataSet] = useState<number>(-1);

  const { results, selectedCompanies } = useSearchContext();

  useEffect(() => {
    axios
      .get(`${BACKEND_URL}/benchmarking?cik=${selectedCompanies.map((item) => item.id).join(",")}`)
      .then((response) => {
        console.log(response.data);
        setData(response.data);
        setDataSet(Object.keys(response.data).map((item) => ({ value: item, label: item })));
        setActiveDataSet(0);
      })
      .catch((error) => {
        console.log(error);
      });
  }, [selectedCompanies]);

  console.log(data[activeDataSet as any]);
  return (
    <StyledBenchmarking>
      <Sidebar options={[]} />
      <VerticalContainer>
        <Search showFilters={true} showDropdown={true} />

        {dataSet.length !== 0 && (
          <DatasetContainer>
            <Label>DataSets</Label>
            {/* {dataSet.map((item, index) => (
            <div key={index}>
              <input type="checkbox" checked={item === activeDataSet} onChange={() => setActiveDataSet(item)} />
              <label>{item}</label>
            </div>
          ))} */}
            <Select
              className="basic-single"
              classNamePrefix="select"
              options={dataSet}
              value={dataSet[activeDataSet]}
              onChange={(value) => setActiveDataSet(getOptionIndex(dataSet, value))}
            />
          </DatasetContainer>
        )}

        {Object.keys(data).length > 0 && activeDataSet !== -1 && (
          <ChartWrapper>
            <BenchmarkBarCanvas
              data={data[dataSet[activeDataSet].value as any]}
              keys={selectedCompanies.map((item) => item.name)}
              indexBy={"year"}
            />
          </ChartWrapper>
        )}

        {/* {Object.keys(data).length > 0 && activeDataSet !== -1 && dataSet.map((dataItem) => {
          console.log(data[dataItem.value as any])
          return(
            <ChartWrapper>
              <BarCanvas
                data={data[dataItem.value as any]}
                keys={selectedCompanies.map((item) => item.name)}
                indexBy={"year"}
              />
            </ChartWrapper>
          )
        })} */}
      </VerticalContainer>
    </StyledBenchmarking>
  );
}
