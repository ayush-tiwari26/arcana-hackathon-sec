import axios from "axios";
import { useEffect, useState } from "react";
import styled from "styled-components";
import BarCanvas from "../components/charts/Bar";
import Search from "../components/Search";
import Sidebar from "../components/Sidebar";
import { Company, SearchProvider, useSearchContext } from "../hooks/useSearchContext";
import { ChartContainer } from "../styles/chart";
import { BACKEND_URL } from "../utils/constants";

const StyledDashboard = styled.div`
  display: flex;
  height: 100vh;
`;

const VerticalContainer = styled.div`
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100vh;
`;

export default function Dashboard() {
  const [data, setData] = useState<any[]>([]);
  const [activeCompany, setActiveCompany] = useState<Company>({ name: "", id: "" });

  const { results, filters } = useSearchContext();

  // TODO: don't hardcode the cik, enable search and add cik in dependency array
  useEffect(() => {
    axios
      .get(`${BACKEND_URL}/derived_metrics?cik=${activeCompany.id}`)
      .then((response) => {
        setData(response.data);
      })
      .catch((error) => {
        console.log(error);
      });
  }, [activeCompany]);

  useEffect(() => {
    setData(data.filter((item) => item.filing_date > filters.startDate && item.filing_date < filters.endDate));
    console.log("filtered data", data);
  }, [filters]);

  return (
    <StyledDashboard>
      <Sidebar options={[]} />
      <VerticalContainer>
        <Search showFilters={true} showDropdown={true} />

        <ChartContainer>
          <BarCanvas data={data} indexBy="filing_date" />
        </ChartContainer>
      </VerticalContainer>
    </StyledDashboard>
  );
}
