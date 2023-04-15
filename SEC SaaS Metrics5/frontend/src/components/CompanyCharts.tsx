import axios from "axios";
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import ReactTooltip from "react-tooltip";
import styled from "styled-components";
import { Filters, useSearchContext } from "../hooks/useSearchContext";
import { ChartContainer } from "../styles/chart";
import { BACKEND_URL } from "../utils/constants";
import { formatDate, formatNumber } from "../utils/helpers";
import BarCanvas from "./charts/Bar";

const Container = styled.div`
  display: flex;
  flex-wrap: wrap;
`;

const ChartWrapper = styled(ChartContainer)`
  height: 400px;
  width: 40%;
  margin: 4rem 1rem 1rem 1rem;
`;

const ChartTitle = styled.div`
  text-align: center;
  margin-bottom: 1.5rem;
`;

const Tooltip = styled.div`
  font-size: 1.2rem;
`;

export default function CompanyCharts() {
  const [tags, setTags] = useState<any[]>([]);
  const [data, setData] = useState<any[]>([]);
  const [filteredData, setFilteredData] = useState<any[]>([]);
  const params = useParams();

  const searchContext = useSearchContext();

  const dateFilter = (data: any[], dates: Filters) => {
    return data.filter((obj) => {
      const objDate = new Date(obj["filing_date"]);
      const startDate = new Date(dates.startDate);
      const endDate = new Date(dates.endDate);
      console.log(objDate, startDate);
      return objDate >= startDate && objDate <= endDate;
    });
  };

  useEffect(() => {
    if (params.id) {
      axios
        .get(`${BACKEND_URL}/unique_metrics?cik=${params.id}`)
        .then((response) => {
          setTags(response.data);
          console.log("tags", response.data);
        })
        .catch((error) => {
          console.log(error);
        });

      axios
        .get(`${BACKEND_URL}/derived_metrics?cik=${params.id}`)
        .then((response) => {
          const tempData: any[] = response.data;
          setData(
            tempData.map((item) => {
              item.color = "#2E719E";
              return item;
            })
          );
        })
        .catch((error) => {
          console.log(error);
        });
    }
  }, []);

  useEffect(() => {
    const temp: any[] = dateFilter(data, searchContext.filters);
    setFilteredData(
      temp.map((item) => {
        const newObj = { ...item };
        newObj.filing_date = formatDate(newObj.filing_date);
        return newObj;
      })
    );
  }, [data, searchContext.filters]);

  return (
    <Container>
      {tags.map((tag, index) => (
        <ChartWrapper data-tip data-for={tag.tag}>
          {tag.source === "xbrl" && (
            <ReactTooltip place="bottom" type="light" id={tag.tag}>
              <Tooltip>
                <strong>Source: </strong>xbrl
                <br />
                <strong>Description: </strong>
                {tag.description}
                <br />
                <strong>Formula: </strong>
                {tag.formula}
              </Tooltip>
            </ReactTooltip>
          )}
          <ChartTitle>{tag.tag}</ChartTitle>
          <BarCanvas
            key={index}
            keys={["value"]}
            data={filteredData.filter((item) => item.tag === tag.tag)}
            indexBy="filing_date"
          />
        </ChartWrapper>
      ))}
    </Container>
  );
}
