import CompanyMetadata from "../components/CompanyMetadata";
import styled from "styled-components";
import Sidebar from "../components/Sidebar";
import Search from "../components/Search";
import { useEffect, useState } from "react";
import { Metadata, SidebarOption } from "../types/company";
import CompanyOwnership from "../components/CompanyOwnership";
import { Link, Routes, useParams, Route } from "react-router-dom";
import axios from "axios";
import { BACKEND_URL } from "../utils/constants";
import { Company, useSearchContext } from "../hooks/useSearchContext";
import CompanySharePrice from "../components/CompanySharePrice";
import CompanyMDA from "../components/CompanyMDA";
import CompanyFinance from "../components/CompanyFinance";
import CompanyCharts from "../components/CompanyCharts";
import CompanyRisk from "../components/CompanyRisk";
import CompanySpreadsheet from "../components/CompanySpreadsheet";

const Container = styled.div`
  display: flex;
  flex-direction: row;
  height: 100vh;
  width: 100vw;
`;

const ColumnContainer = styled.div`
  display: flex;
  flex-direction: column;
`;

const TitleContainer = styled.div`
  display: flex;
  align-items: center;
  padding: 1rem 1.5rem;
`;

const VerticalContainer = styled.div`
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100vh;
`;

const Title = styled.div`
  padding: 0 1rem;
  font-size: 2.8rem;
  font-weight: bold;
`;

const CompanyID = styled.div`
  margin: 1rem;
  padding: 0.5rem 1rem;
  background-color: #d5eeff;
  border-radius: 10px;
`;

const ListView = styled.div`
  margin: 2rem;
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr;
  text-transform: uppercase;

  a {
    display: inline-block;
    margin: 0.8rem 1.2rem;
    color: #333;
    text-decoration: none;

    &::before {
      border-bottom: 0.2rem solid transparent;
      font-weight: 500;
    }

    &:hover {
      border-bottom: 0.2rem solid #2e719e;
      font-weight: 500;
    }
  }
`;

const sidebarOptions: SidebarOption[] = [
  {
    name: "Overview",
    icon: "overview",
    link: ""
  },
  {
    name: "Financials",
    icon: "financials",
    link: "financials"
  },
  {
    name: "Share price vs Filings",
    icon: "share",
    link: "share-price"
  },
  {
    name: "Metrics",
    icon: "influence",
    link: "spreadsheet"
  },
  {
    name: "Ownership",
    icon: "ownership",
    link: "ownership"
  },
  {
    name: "MDA & Sentiment",
    icon: "mda",
    link: "mda"
  },
  {
    name: "Risks associated",
    icon: "risk",
    link: "risks"
  }
];

export default function CompanyPage() {
  const { results } = useSearchContext();
  const [selectedSidebarIndex, setSelectedSidebarIndex] = useState<number>(0);

  const [metadata, setMetadata] = useState<Metadata>({
    cik: undefined,
    // Lmao
    name: "Loading",
    category: "Loading",
    overview: "Loading",
    ticker: "Loading"
  });

  let params = useParams();

  useEffect(() => {
    if (params.id !== undefined) {
      axios
        .get(`${BACKEND_URL}/companies?cik=${params.id}`)
        .then((response) => {
          const companyMetadata: Metadata = response.data[0];
          setMetadata(companyMetadata);
        })
        .catch((error) => console.log(error));
    }
  }, [params.id]);

  return (
    <VerticalContainer>
      {params.id === undefined ? (
        <Container>
          <Sidebar />
          <ColumnContainer>
            <Search showFilters={false} showDropdown={false} />
            <ListView>
              {results.map((company, index) => {
                return (
                  <Link key={index} to={`/companies/${company.id}`}>
                    {company.name}
                  </Link>
                );
              })}
            </ListView>
          </ColumnContainer>
        </Container>
      ) : (
        <Container>
          <Sidebar
            options={sidebarOptions}
            selectedOption={selectedSidebarIndex}
            onOptionChange={(index: Number) => setSelectedSidebarIndex(Number(index))}
            companyID={params.id}
          />
          <VerticalContainer>
            <Search showFilters={true} showDropdown={false} />
            <TitleContainer>
              <Title>{metadata.name}</Title>
              <CompanyID>{metadata.ticker.split("'")[1]}</CompanyID>
            </TitleContainer>
            <Routes>
              <Route index element={<CompanyMetadata {...metadata} />} />
              <Route path="/financials" element={<CompanyFinance />} />
              <Route path="/share-price" element={<CompanySharePrice />} />
              <Route path="/spreadsheet" element={<CompanySpreadsheet />} />
              <Route path="/ownership" element={<CompanyOwnership />} />
              <Route path="/mda" element={<CompanyMDA />} />
              <Route path="/risks" element={<CompanyRisk />} />
            </Routes>
          </VerticalContainer>
        </Container>
      )}
    </VerticalContainer>
  );
}
