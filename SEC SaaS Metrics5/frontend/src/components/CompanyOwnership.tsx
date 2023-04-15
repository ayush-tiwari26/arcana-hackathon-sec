import axios from "axios";
import fuzzysort from "fuzzysort";
import { useEffect, useMemo, useState } from "react";
import { useParams, useSearchParams } from "react-router-dom";
import { Column } from "react-table";
import styled from "styled-components";
import { Filters, useSearchContext } from "../hooks/useSearchContext";
import { OwnershipData } from "../types/company";
import { BACKEND_URL } from "../utils/constants";
import { formatNumber } from "../utils/helpers";
import DownloadButton from "./DownloadButton";
import Table from "./StyledTable";

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

export default function CompanyOwnership() {
  const [mode, setMode] = useState<"direct" | "institutional">("direct");
  const [directData, setDirectData] = useState<OwnershipData[]>([]);
  const [institutionalData, setInstitutionalData] = useState<OwnershipData[]>([]);

  let params = useParams();
  let searchContext = useSearchContext();

  useEffect(() => {
    axios.get(`${BACKEND_URL}/ownership?cik=${params.id}`).then((response) => {
      setDirectData(response.data["Direct Holders"]);
      setInstitutionalData(response.data["Top Institutional Holders"]);
    });
  }, []);

  const columns: Column<OwnershipData>[] = useMemo(
    () => [
      {
        Header: "Holder",
        accessor: "Holder" as keyof OwnershipData
      },
      {
        Header: "Shares",
        accessor: "Shares" as keyof OwnershipData
      },
      {
        Header: "Date Reported",
        accessor: "Date Reported" as keyof OwnershipData
      },
      {
        Header: "% Out",
        accessor: "% Out" as keyof OwnershipData
      },
      {
        Header: "Value",
        accessor: "Value" as keyof OwnershipData
      }
    ],
    []
  );

  const queryFilter = (data: any[], query: string) => {
    if (query === "") return data;
    else return fuzzysort.go(query, data, { key: "Holder" }).map((item) => item.obj);
  };

  const dateFilter = (data: any[], dates: Filters) => {
    return data.filter((obj) => {
      const objDate = new Date(obj["Date Reported"]);
      const startDate = new Date(dates.startDate);
      const endDate = new Date(dates.endDate);
      return objDate >= startDate && objDate <= endDate;
    });
  };

  const formatData = (data: any[]) => {
    return data.map((obj) => {
      const newObj = { ...obj };
      newObj.Shares = new Intl.NumberFormat("en-US").format(parseInt(obj.Shares));
      newObj.Value = "$ " + formatNumber(parseInt(obj.Value));
      return newObj;
    });
  };

  const directdata = useMemo(
    () => [...dateFilter(queryFilter(formatData(directData), searchContext.query), searchContext.filters)],
    [directData, searchContext.query, searchContext.filters]
  );
  const institutionaldata = useMemo(
    () => [...dateFilter(queryFilter(formatData(institutionalData), searchContext.query), searchContext.filters)],
    [institutionalData, searchContext.query, searchContext.filters]
  );

  return (
    <div>
      <ButtonGroup>
        <ModeButton className={`${mode === "direct" ? "active" : ""}`} onClick={() => setMode("direct")}>
          Direct Holders
        </ModeButton>
        <ModeButton className={`${mode === "institutional" ? "active" : ""}`} onClick={() => setMode("institutional")}>
          Top Institutional Holders
        </ModeButton>
      </ButtonGroup>
      <Table data={mode === "direct" ? directdata : institutionaldata} columns={columns} />
      <DownloadButton
        fileName={`ownership-${mode}-${params.id}.csv`}
        data={mode === "direct" ? directdata : institutionaldata}
      />
    </div>
  );
}
