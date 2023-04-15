import { useEffect, useMemo, useState } from "react";
import axios from "axios";
import { BACKEND_URL } from "../utils/constants";
import { Column } from "react-table";
import { useParams } from "react-router-dom";
import { Filters, useSearchContext } from "../hooks/useSearchContext";
import { formatNumber } from "../utils/helpers";
import DownloadButton from "./DownloadButton";
import Table from "./StyledTable";
import { SpreadsheetData } from "../types/company";
import fuzzysort from "fuzzysort";

export default function CompanySpreadsheet() {
  const [companyData, setCompanyData] = useState<SpreadsheetData[]>([]);
  const [filteredCompanyData, setFilteredCompanyData] = useState<SpreadsheetData[]>([]);

  let params = useParams();
  const searchContext = useSearchContext();

  useEffect(() => {
    searchContext.setQuery("");

    axios
      .get(`${BACKEND_URL}/derived_metrics?cik=${params.id}`)
      .then((response) => {
        setCompanyData(response.data);
      })
      .catch((error) => console.log(error));
  }, []);

  useEffect(() => {
    const temp = companyData.filter((company) => {
      return company.tag.toLowerCase().includes(searchContext.query.toLowerCase()) || searchContext.isQueryEmpty();
    });
    setFilteredCompanyData(temp);
  }, [companyData, searchContext.query]);

  const queryFilter = (data: any[], query: string) => {
    if (query === "") return data;
    else return fuzzysort.go(query, data, { key: "tag" }).map((item) => item.obj);
  };

  const dateFilter = (data: any[], dates: Filters) => {
    return data.filter((obj) => {
      const objDate = new Date(obj["filing_date"]);
      const startDate = new Date(dates.startDate);
      const endDate = new Date(dates.endDate);
      return objDate >= startDate && objDate <= endDate;
    });
  };

  const formFilter = (data: any[]) => {
    console.log(searchContext.selectedFilings);
    return data.filter((obj) => {
      return searchContext.selectedFilings.map((item) => item.value).includes(obj.form_type);
    });
  };

  const sourceFilter = (data: any[]) => {
    console.log(searchContext.selectedSource);
    return data.filter((obj) => {
      return searchContext.selectedSource.map((item) => item.value).includes(obj.source);
    });
  };

  const data = useMemo(
    () => [
      ...sourceFilter(
        formFilter(dateFilter(queryFilter(filteredCompanyData, searchContext.query), searchContext.filters))
      )
    ],
    [
      filteredCompanyData,
      searchContext.query,
      searchContext.filters,
      searchContext.selectedFilings,
      searchContext.selectedSource
    ]
  );

  const columns: Column<SpreadsheetData>[] = useMemo(
    () => [
      {
        Header: "Metric",
        accessor: "tag" as keyof SpreadsheetData
      },
      {
        Header: "Value",
        accessor: "value" as keyof SpreadsheetData,
        Cell: ({ cell }: { cell: { value: any } }) => <div>{formatNumber(cell.value)}</div>
      },
      {
        Header: "Form Type",
        accessor: "form_type" as keyof SpreadsheetData
      },
      {
        Header: "Filing Date",
        accessor: "filing_date" as keyof SpreadsheetData
      }
    ],
    []
  );

  return (
    <div>
      <DownloadButton fileName={`sheet-${params.id}.csv`} data={data} />
      <Table data={data} columns={columns} />
    </div>
  );
}
